"""
cluster_configs.py — Clustering analysis of unavoidable-set configurations.

Extracts feature vectors from degree patterns, computes pairwise distances,
and applies hierarchical + k-means clustering to identify families of
"structurally similar" configurations.

Goal: find parameterized families — large clusters sharing a common
reducibility argument pattern.  If one cluster covers >= 50 patterns,
that family can potentially be collapsed into a single parameterized lemma.

Agent 1520-M3 / Sub-task S3
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from framework import (
    DegreePattern,
    DischargingEngine,
    DischargingRule,
    build_basic_rules,
    build_standard_rules,
    build_extended_rules,
)

try:
    from scipy.cluster.hierarchy import linkage, fcluster
    from scipy.spatial.distance import pdist
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ======================================================================
# Feature extraction
# ======================================================================

FEATURE_NAMES = [
    "n_major", "n_minor", "min_nbr", "max_nbr", "mean_nbr",
    "deg6_count", "deg7_count", "deg8p_count",
    "max_minor_run", "deg_variance",
]


def extract_features(p: DegreePattern) -> np.ndarray:
    hist = Counter(p.neighbors)
    nbrs = np.array(p.neighbors, dtype=float)
    return np.array([
        p.count_major(),
        p.count_minor(),
        min(p.neighbors),
        max(p.neighbors),
        nbrs.mean(),
        hist.get(6, 0),
        hist.get(7, 0),
        sum(v for k, v in hist.items() if k >= 8),
        p.consecutive_minor_run(),
        nbrs.var(),
    ], dtype=float)


def feature_matrix(patterns: List[DegreePattern]) -> np.ndarray:
    return np.vstack([extract_features(p) for p in patterns])


# ======================================================================
# Clustering
# ======================================================================

def hierarchical_cluster(X: np.ndarray,
                         n_clusters: int = 5) -> np.ndarray:
    """Ward-linkage hierarchical clustering. Returns label array."""
    if not SCIPY_AVAILABLE:
        raise RuntimeError("scipy required for hierarchical clustering")
    if len(X) < 2:
        return np.zeros(len(X), dtype=int)
    # Normalize features to [0,1]
    mn, mx = X.min(axis=0), X.max(axis=0)
    rng = mx - mn
    rng[rng == 0] = 1.0
    Xn = (X - mn) / rng
    Z = linkage(Xn, method="ward")
    labels = fcluster(Z, t=n_clusters, criterion="maxclust")
    return labels


def kmeans_simple(X: np.ndarray, k: int, max_iter: int = 100,
                  seed: int = 42) -> np.ndarray:
    """Minimal k-means (no sklearn dependency)."""
    rng = np.random.RandomState(seed)
    n = len(X)
    if n <= k:
        return np.arange(n)
    # Normalize
    mn, mx = X.min(axis=0), X.max(axis=0)
    diff = mx - mn
    diff[diff == 0] = 1.0
    Xn = (X - mn) / diff
    # Random init
    idx = rng.choice(n, size=k, replace=False)
    centers = Xn[idx].copy()
    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        dists = np.linalg.norm(Xn[:, None, :] - centers[None, :, :], axis=2)
        new_labels = dists.argmin(axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for c in range(k):
            mask = labels == c
            if mask.any():
                centers[c] = Xn[mask].mean(axis=0)
    return labels


# ======================================================================
# Cluster analysis
# ======================================================================

def cluster_summary(patterns: List[DegreePattern],
                    labels: np.ndarray,
                    X: np.ndarray) -> List[Dict[str, Any]]:
    """Summarize each cluster."""
    summaries: List[Dict[str, Any]] = []
    for cid in sorted(set(labels)):
        mask = labels == cid
        members = [patterns[i] for i in range(len(patterns)) if mask[i]]
        feats = X[mask]
        summaries.append({
            "cluster_id": int(cid),
            "size": len(members),
            "mean_features": {FEATURE_NAMES[j]: round(float(feats[:, j].mean()), 2)
                              for j in range(feats.shape[1])},
            "std_features": {FEATURE_NAMES[j]: round(float(feats[:, j].std()), 2)
                             for j in range(feats.shape[1])},
            "example_patterns": [str(m) for m in members[:5]],
        })
    return summaries


def natural_grouping(patterns: List[DegreePattern]) -> Dict[int, List[DegreePattern]]:
    """Group by number of major neighbours (the dominant discriminator)."""
    groups: Dict[int, List[DegreePattern]] = defaultdict(list)
    for p in patterns:
        groups[p.count_major()].append(p)
    return dict(groups)


# ======================================================================
# RSST configuration estimation
# ======================================================================

def estimate_rsst_configs(patterns: List[DegreePattern]) -> Dict[str, Any]:
    """Estimate the number of full RSST-style configurations per degree pattern.

    Each degree pattern (d; d_1,...,d_k) can be realized by many near-
    triangulations with different internal structures.  The count grows
    with ring size and the number of internal vertices.  We estimate
    using the formula:  configs(p) ~ Product_{i=1}^{k} (d_i - 4)
    which counts the rough number of ways to triangulate the interior.
    """
    total = 0
    per_pattern: List[Tuple[DegreePattern, int]] = []
    for p in patterns:
        est = 1
        for d in p.neighbors:
            est *= max(1, d - 4)
        per_pattern.append((p, est))
        total += est
    per_pattern.sort(key=lambda x: -x[1])
    return {
        "total_estimated_configs": total,
        "top_patterns": [(str(p), e) for p, e in per_pattern[:10]],
        "bottom_patterns": [(str(p), e) for p, e in per_pattern[-5:]],
    }


# ======================================================================
# Main
# ======================================================================

def main() -> None:
    print("=" * 60)
    print("CLUSTERING ANALYSIS — Unavoidable Set Configurations")
    print("Agent 1520-M3 / Sub-task S3")
    print("=" * 60)

    # We analyze multiple rule sets for comparison
    rule_sets = {
        "Basic (1 rule)": build_basic_rules(),
        "Standard (6 rules)": build_standard_rules(),
        "Extended (12 rules)": build_extended_rules(),
    }

    all_results: Dict[str, Any] = {}

    for name, rules in rule_sets.items():
        print(f"\n{'─' * 60}")
        print(f"Rule set: {name}")
        print(f"{'─' * 60}")

        engine = DischargingEngine(rules, min_deg=5, max_deg=12)
        unavoidable = engine.compute_unavoidable_set(center_degrees=[5])
        print(f"Unavoidable set size: {len(unavoidable)}")

        if len(unavoidable) < 2:
            print("  Too few patterns for clustering; skipping.")
            all_results[name] = {
                "unavoidable_count": len(unavoidable),
                "note": "too few for clustering",
            }
            continue

        X = feature_matrix(unavoidable)

        # --- Natural grouping (by # major) ---
        groups = natural_grouping(unavoidable)
        print(f"\n  Natural grouping (by major-neighbour count):")
        for k in sorted(groups):
            print(f"    {k} major:  {len(groups[k]):>5d} patterns")

        # --- RSST config estimation ---
        est = estimate_rsst_configs(unavoidable)
        print(f"\n  Estimated RSST-style full configurations: {est['total_estimated_configs']}")
        print(f"  Top-5 degree patterns by config count:")
        for pat_str, cnt in est["top_patterns"][:5]:
            print(f"    {pat_str:>30s}  →  ~{cnt} configs")

        # --- Hierarchical clustering ---
        n_clust = min(5, len(unavoidable))
        if SCIPY_AVAILABLE and len(unavoidable) >= 2:
            h_labels = hierarchical_cluster(X, n_clusters=n_clust)
            h_summary = cluster_summary(unavoidable, h_labels, X)
            print(f"\n  Hierarchical clustering (k={n_clust}):")
            for cs in h_summary:
                print(f"    Cluster {cs['cluster_id']:>2d}:  "
                      f"{cs['size']:>5d} patterns,  "
                      f"avg_major={cs['mean_features']['n_major']:.1f},  "
                      f"avg_mean_nbr={cs['mean_features']['mean_nbr']:.1f}")
        else:
            h_labels = np.zeros(len(unavoidable), dtype=int)
            h_summary = []
            print("  (scipy not available; using k-means only)")

        # --- K-means clustering ---
        k_labels = kmeans_simple(X, k=n_clust)
        k_summary = cluster_summary(unavoidable, k_labels, X)
        print(f"\n  K-means clustering (k={n_clust}):")
        for cs in k_summary:
            print(f"    Cluster {cs['cluster_id']:>2d}:  "
                  f"{cs['size']:>5d} patterns,  "
                  f"avg_major={cs['mean_features']['n_major']:.1f},  "
                  f"avg_mean_nbr={cs['mean_features']['mean_nbr']:.1f}")

        # --- Largest cluster analysis ---
        largest = max(k_summary, key=lambda c: c["size"])
        print(f"\n  Largest cluster: #{largest['cluster_id']} "
              f"with {largest['size']} patterns")
        print(f"    Mean features: {largest['mean_features']}")

        all_results[name] = {
            "unavoidable_count": len(unavoidable),
            "natural_groups": {str(k): len(v) for k, v in groups.items()},
            "estimated_rsst_configs": est["total_estimated_configs"],
            "hierarchical_clusters": h_summary,
            "kmeans_clusters": k_summary,
            "largest_cluster_size": largest["size"],
        }

    # --- Cross-rule-set comparison ---
    print(f"\n{'=' * 60}")
    print("CROSS-RULE-SET COMPARISON")
    print(f"{'=' * 60}")
    print(f"{'Rule set':<25s} {'|U|':>6s} {'~Configs':>9s} {'Largest':>8s}")
    print("-" * 52)
    for name, res in all_results.items():
        u = res["unavoidable_count"]
        cfg = res.get("estimated_rsst_configs", "—")
        lg = res.get("largest_cluster_size", "—")
        print(f"{name:<25s} {u:>6d} {str(cfg):>9s} {str(lg):>8s}")
    print(f"\nRSST reference: 633 configurations, ring sizes 5–14")

    # --- Export ---
    out_path = Path(__file__).resolve().parent / "cluster_results.json"
    # Make JSON-serializable
    safe = {}
    for name, res in all_results.items():
        safe[name] = json.loads(json.dumps(res, default=str))
    with open(out_path, "w") as f:
        json.dump(safe, f, indent=2)
    print(f"\nResults → {out_path}")


if __name__ == "__main__":
    main()

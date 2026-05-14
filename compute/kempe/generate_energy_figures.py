"""
generate_energy_figures.py — Agent 1443-M3-S1

Generate publication-quality matplotlib figures from the counterexample
energy analysis results.

Figures:
1. Bar chart: safe vs unsafe path energy metrics
2. Energy barrier profile: Magic Gem energy along BFS path
3. Electrostatic potential heatmap on graph nodes
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import networkx as nx

from triangulation_db import generate_triangulations
from kempe_ops import enumerate_colourings, num_colours, get_kempe_chain
from physical_analogies import compute_electrostatic_potential, _nx_to_adj

DELIVERABLES = os.path.join(os.path.dirname(__file__), '..', '..',
                             'backgroundMaterial', 'agent1443', 'deliverables')

plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0',
    'text.color': '#e0e0e0',
    'xtick.color': '#e0e0e0',
    'ytick.color': '#e0e0e0',
    'legend.facecolor': '#16213e',
    'legend.edgecolor': '#e0e0e0',
    'grid.color': '#2a2a4a',
    'grid.alpha': 0.5,
    'font.size': 11,
    'figure.dpi': 150,
})

SAFE_COLOR = '#00d4aa'
UNSAFE_COLOR = '#ff6b6b'
ACCENT = '#4ecdc4'
HIGHLIGHT = '#ffe66d'


def load_results():
    path = os.path.join(DELIVERABLES, 'targeted_energy_results.json')
    with open(path) as f:
        return json.load(f)


def fig1_safe_vs_unsafe_bars(data, graph_key='T_9_25'):
    """Bar chart comparing energy metric means for safe vs unsafe paths."""
    gd = data[graph_key]
    agg = gd['aggregates']

    metrics = [
        ('global_magic_gem', 'Magic Gem\nEnergy'),
        ('potts_energy', 'Potts\nEnergy'),
        ('local_entropy_v', 'Local\nEntropy'),
        ('electrostatic_v', 'Electrostatic\nPotential'),
        ('chain_ruggedness', 'Chain\nRuggedness'),
        ('chain_tension', 'Surface\nTension'),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle(f'Energy Metrics: Safe vs Unsafe Paths — {graph_key}\n'
                 f'(v={gd["vertex"]}, degree {gd["degree"]}, '
                 f'{gd["num_true_counterexamples"]} counterexample colorings)',
                 fontsize=14, fontweight='bold')

    for idx, (key, label) in enumerate(metrics):
        ax = axes[idx // 3][idx % 3]
        u = agg['unsafe'].get(key, {'mean': 0, 'std': 0, 'n': 0})
        s = agg['safe'].get(key, {'mean': 0, 'std': 0, 'n': 0})

        bars = ax.bar(['Unsafe\nPaths', 'Safe\nPaths'],
                       [u['mean'], s['mean']],
                       yerr=[u['std'], s['std']],
                       color=[UNSAFE_COLOR, SAFE_COLOR],
                       edgecolor='white', linewidth=0.5,
                       capsize=5, width=0.5)

        ax.set_title(label, fontsize=11, fontweight='bold')
        ax.set_ylabel('Mean value')
        ax.grid(axis='y', alpha=0.3)

        for bar, val in zip(bars, [u['mean'], s['mean']]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + u['std'] * 0.1,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9, color='white')

    plt.tight_layout()
    out = os.path.join(DELIVERABLES, f'safe_vs_unsafe_energy_bars_{graph_key}.png')
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out}")


def fig2_energy_barrier_profile(data, graph_key='T_9_25'):
    """Energy along BFS path: safe vs unsafe overlay."""
    gd = data[graph_key]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Energy Barrier Profiles — {graph_key}\n'
                 f'Unsafe (opt dist=2) vs Safe (dist=3) paths',
                 fontsize=14, fontweight='bold')

    metric_keys = [
        ('magic_gem', 'Magic Gem Energy', r'$E_{\mathrm{MG}}$'),
        ('potts', 'Potts Energy', r'$H_{\mathrm{Potts}}$'),
        ('entropy', 'Local Entropy at $v$', r'$H(v)$'),
        ('color5_count', 'Color-5 Vertex Count', r'$|V_5|$'),
    ]

    unsafe_profiles = []
    safe_profiles = []
    for ce in gd['counterexample_analyses']:
        if 'unsafe_profile' in ce:
            unsafe_profiles.append(ce['unsafe_profile'])
        if 'safe_profile' in ce:
            safe_profiles.append(ce['safe_profile'])

    for idx, (key, title, ylabel) in enumerate(metric_keys):
        ax = axes[idx // 2][idx % 2]

        for up in unsafe_profiles[:8]:
            vals = up[key]
            ax.plot(range(len(vals)), vals, color=UNSAFE_COLOR, alpha=0.15, linewidth=1)

        for sp in safe_profiles[:8]:
            vals = sp[key]
            ax.plot(range(len(vals)), vals, color=SAFE_COLOR, alpha=0.15, linewidth=1)

        if unsafe_profiles:
            mean_u = np.mean([up[key] for up in unsafe_profiles], axis=0)
            ax.plot(range(len(mean_u)), mean_u, color=UNSAFE_COLOR,
                    linewidth=2.5, marker='o', markersize=6, label='Unsafe (mean)')

        if safe_profiles:
            all_safe_arrs = [sp[key] for sp in safe_profiles]
            max_len = max(len(a) for a in all_safe_arrs)
            padded = []
            for a in all_safe_arrs:
                if len(a) < max_len:
                    padded.append(a + [a[-1]] * (max_len - len(a)))
                else:
                    padded.append(a)
            mean_s = np.mean(padded, axis=0)
            ax.plot(range(len(mean_s)), mean_s, color=SAFE_COLOR,
                    linewidth=2.5, marker='s', markersize=6, label='Safe (mean)')

        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('BFS Step')
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(DELIVERABLES, f'energy_barrier_profile_{graph_key}.png')
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out}")


def fig3_electrostatic_heatmap(graph_key_idx=25):
    """Electrostatic potential heatmap on graph nodes."""
    db = generate_triangulations(9)
    T = db[9][graph_key_idx]
    target_v = 3 if graph_key_idx == 25 else 6
    name = T.graph.get('name', f'T_9_{graph_key_idx}')

    all_cols = enumerate_colourings(T, 5)
    v5_cols = [c for c in all_cols if c[target_v] == 5 and num_colours(c) == 5]
    col = v5_cols[0]

    adj = _nx_to_adj(T)
    pot = compute_electrostatic_potential(adj, col)

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fig.suptitle(f'Electrostatic Potential — {name}\n'
                 f'(v={target_v} colored 5, shown as charge source)',
                 fontsize=14, fontweight='bold')

    pos = nx.spring_layout(T, seed=42, k=2.0)

    pot_vals = [pot[v] for v in sorted(T.nodes())]
    vmin, vmax = min(pot_vals), max(pot_vals)
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.RdYlBu_r

    nx.draw_edges = nx.draw_networkx_edges(T, pos, ax=ax,
                                            edge_color='#555577', width=1.5, alpha=0.6)

    for v in sorted(T.nodes()):
        x, y = pos[v]
        color = cmap(norm(pot[v]))
        size = 600 if v == target_v else 400
        marker = '*' if v == target_v else 'o'
        edgecolor = HIGHLIGHT if v == target_v else 'white'
        ax.scatter(x, y, c=[color], s=size, marker=marker,
                   edgecolors=edgecolor, linewidths=2, zorder=5)
        ax.annotate(f'{v}\n({pot[v]:.3f})', (x, y),
                    textcoords='offset points', xytext=(0, 15),
                    ha='center', fontsize=8, color='white',
                    fontweight='bold' if v == target_v else 'normal')

    color_labels = {v: col[v] for v in T.nodes()}
    for v in sorted(T.nodes()):
        x, y = pos[v]
        ax.annotate(f'c={color_labels[v]}', (x, y),
                    textcoords='offset points', xytext=(0, -18),
                    ha='center', fontsize=7, color='#aaaacc')

    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label('Electrostatic Potential $V$', color='#e0e0e0')
    cbar.ax.yaxis.set_tick_params(color='#e0e0e0')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#e0e0e0')

    ax.set_xlim(ax.get_xlim()[0] - 0.3, ax.get_xlim()[1] + 0.3)
    ax.set_ylim(ax.get_ylim()[0] - 0.3, ax.get_ylim()[1] + 0.3)
    ax.axis('off')

    plt.tight_layout()
    out = os.path.join(DELIVERABLES, f'electrostatic_heatmap_{name}.png')
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out}")


if __name__ == '__main__':
    print("Generating figures for Agent 1443-M3...")
    os.makedirs(DELIVERABLES, exist_ok=True)

    data = load_results()

    print("\nFigure 1: Safe vs Unsafe Energy Bars")
    fig1_safe_vs_unsafe_bars(data, 'T_9_25')

    print("\nFigure 2: Energy Barrier Profiles")
    fig2_energy_barrier_profile(data, 'T_9_25')

    print("\nFigure 3: Electrostatic Potential Heatmap")
    fig3_electrostatic_heatmap(25)

    print("\n--- Also generating for T_9_35 ---")
    fig1_safe_vs_unsafe_bars(data, 'T_9_35')
    fig2_energy_barrier_profile(data, 'T_9_35')
    fig3_electrostatic_heatmap(35)

    print("\nAll figures generated successfully.")

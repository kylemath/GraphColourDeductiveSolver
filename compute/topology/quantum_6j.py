"""
Quantum 6j-symbol computation for U_q(sl_2) at q = e^{iπ/r}.

At level r, admissible representations have spin j = 0, 1/2, 1, ..., (r-2)/2.
The quantum 6j-symbols (Racah-Wigner coefficients) are central to the
Turaev-Viro state sum invariant.

For the TQFT approach to 4CT (Kauffman 1990), we need r=3 specifically:
  - Admissible spins: j = 0, 1/2, 1
  - q = e^{iπ/3} (6th root of unity)

Sign patterns of 6j-symbols determine whether the Turaev-Viro state sum
can yield a positivity proof of Pen(G) > 0.
"""

from __future__ import annotations
import numpy as np
from typing import List, Tuple, Dict, Optional
from fractions import Fraction
from itertools import product
import json
import sys


def quantum_integer(n: int, q: complex) -> complex:
    """Compute [n]_q = (q^n - q^{-n}) / (q - q^{-1})."""
    if abs(q - 1.0) < 1e-12:
        return complex(n)
    num = q**n - q**(-n)
    den = q - q**(-1)
    if abs(den) < 1e-15:
        return complex(n)
    return num / den


def quantum_factorial(n: int, q: complex) -> complex:
    """Compute [n]_q! = [1]_q * [2]_q * ... * [n]_q."""
    if n < 0:
        return complex(0)
    result = complex(1.0)
    for k in range(1, n + 1):
        result *= quantum_integer(k, q)
    return result


def admissible_spins(r: int) -> List[float]:
    """Return admissible spins at level r: j = 0, 1/2, ..., (r-2)/2."""
    return [k / 2.0 for k in range(r - 1)]


def triangle_admissible(j1: float, j2: float, j3: float, r: int) -> bool:
    """Check triangle inequality and admissibility for a triple (j1, j2, j3).
    
    Conditions:
    1. |j1 - j2| <= j3 <= j1 + j2 (triangle inequality)
    2. j1 + j2 + j3 is an integer
    3. j1 + j2 + j3 <= r - 2 (level truncation)
    """
    if j3 < abs(j1 - j2) - 1e-10 or j3 > j1 + j2 + 1e-10:
        return False
    s = j1 + j2 + j3
    if abs(s - round(s)) > 1e-10:
        return False
    if s > r - 2 + 1e-10:
        return False
    return True


def quantum_delta(j1: float, j2: float, j3: float, q: complex) -> complex:
    """Compute the quantum triangle coefficient Δ(j1, j2, j3).
    
    Δ(a,b,c) = sqrt( [a+b-c]! [a-b+c]! [-a+b+c]! / [a+b+c+1]! )
    where arguments are integers after converting from half-integers.
    """
    a, b, c = int(2 * j1), int(2 * j2), int(2 * j3)
    n1 = (a + b - c) // 2
    n2 = (a - b + c) // 2
    n3 = (-a + b + c) // 2
    n4 = (a + b + c) // 2 + 1

    num = quantum_factorial(n1, q) * quantum_factorial(n2, q) * quantum_factorial(n3, q)
    den = quantum_factorial(n4, q)
    if abs(den) < 1e-30:
        return complex(0)
    return np.sqrt(num / den)


def quantum_6j(j1: float, j2: float, j3: float,
               j4: float, j5: float, j6: float,
               q: complex, r: int) -> complex:
    """Compute the quantum 6j-symbol {j1 j2 j3; j4 j5 j6}_q.
    
    Uses the Racah sum formula generalized to quantum groups.
    The 6j-symbol couples four angular momenta with the tetrahedron
    having edges (j1,...,j6) and four triangular faces:
      (j1,j2,j3), (j1,j5,j6), (j2,j4,j6), (j3,j4,j5)
    """
    triads = [
        (j1, j2, j3), (j1, j5, j6), (j2, j4, j6), (j3, j4, j5)
    ]
    for triad in triads:
        if not triangle_admissible(*triad, r):
            return complex(0)

    delta_product = complex(1.0)
    for triad in triads:
        delta_product *= quantum_delta(*triad, q)

    a, b, c, d, e, f = (int(2 * x) for x in [j1, j2, j3, j4, j5, j6])

    z_min_candidates = [
        (a + b + c) // 2,
        (a + e + f) // 2,
        (b + d + f) // 2,
        (c + d + e) // 2,
    ]
    z_max_candidates = [
        (a + b + d + e) // 2,
        (b + c + e + f) // 2,
        (a + c + d + f) // 2,
    ]
    z_min = max(z_min_candidates)
    z_max = min(z_max_candidates)

    result = complex(0)
    for z in range(z_min, z_max + 1):
        num = quantum_factorial(z + 1, q)
        args = [
            z - (a + b + c) // 2,
            z - (a + e + f) // 2,
            z - (b + d + f) // 2,
            z - (c + d + e) // 2,
            (a + b + d + e) // 2 - z,
            (b + c + e + f) // 2 - z,
            (a + c + d + f) // 2 - z,
        ]
        den = complex(1.0)
        for arg in args:
            den *= quantum_factorial(arg, q)
        if abs(den) < 1e-30:
            continue
        sign = (-1) ** z
        result += sign * num / den

    return delta_product * result


def quantum_dimension(j: float, q: complex) -> complex:
    """Quantum dimension d_j = [2j+1]_q."""
    return quantum_integer(int(2 * j) + 1, q)


def compute_all_6j_symbols(r: int) -> Dict:
    """Compute all admissible 6j-symbols at level r.
    
    Returns a dictionary with:
    - 'r': level
    - 'q': quantum parameter
    - 'spins': admissible spins
    - 'symbols': list of (j-tuple, value) for all non-zero 6j-symbols
    - 'sign_pattern': summary of signs
    """
    q = np.exp(1j * np.pi / r)
    spins = admissible_spins(r)

    print(f"\n{'='*60}")
    print(f"Level r = {r}")
    print(f"q = e^(iπ/{r})")
    print(f"Admissible spins: {spins}")
    print(f"Quantum dimensions:", end=" ")
    for j in spins:
        d = quantum_dimension(j, q)
        print(f"d_{j} = {d:.4f}", end="  ")
    print()

    symbols = []
    all_positive = True
    all_nonnegative = True
    has_negative = False
    has_positive = False
    sign_counts = {'+': 0, '-': 0, '0': 0}

    for j1, j2, j3, j4, j5, j6 in product(spins, repeat=6):
        val = quantum_6j(j1, j2, j3, j4, j5, j6, q, r)
        real_part = val.real
        imag_part = val.imag

        if abs(val) < 1e-10:
            continue

        if abs(imag_part) > 1e-8:
            print(f"  WARNING: Non-real 6j at ({j1},{j2},{j3};{j4},{j5},{j6}): {val}")

        symbols.append({
            'spins': (j1, j2, j3, j4, j5, j6),
            'value': val,
            'real': real_part,
        })

        if real_part > 1e-10:
            sign_counts['+'] += 1
            has_positive = True
        elif real_part < -1e-10:
            sign_counts['-'] += 1
            has_negative = True
            all_positive = False
            all_nonnegative = False
        else:
            sign_counts['0'] += 1
            all_positive = False

    print(f"\nNon-zero 6j-symbols: {len(symbols)}")
    print(f"Sign pattern: {sign_counts['+']}/{sign_counts['-']}/{sign_counts['0']} (+/-/0)")
    print(f"All positive: {all_positive}")
    print(f"All non-negative: {all_nonnegative}")
    print(f"Has negative: {has_negative}")

    if all_nonnegative:
        print("★ ALL 6j-symbols are non-negative → TV state sum manifestly positive!")
    elif has_negative:
        print("✗ Mixed signs → manifestly positive state sum NOT possible at this level")

    return {
        'r': r,
        'q_str': f"e^(iπ/{r})",
        'spins': spins,
        'symbols': symbols,
        'sign_counts': sign_counts,
        'all_positive': all_positive,
        'all_nonnegative': all_nonnegative,
        'has_negative': has_negative,
    }


def print_6j_table(result: Dict) -> str:
    """Format 6j-symbol results as a readable table."""
    lines = []
    lines.append(f"## 6j-Symbols at r = {result['r']}")
    lines.append(f"q = {result['q_str']}")
    lines.append(f"Admissible spins: {result['spins']}")
    lines.append(f"Non-zero symbols: {len(result['symbols'])}")
    lines.append(f"Signs: {result['sign_counts']['+']}/{result['sign_counts']['-']}/{result['sign_counts']['0']} (+/-/0)")
    lines.append("")

    lines.append("| j1 | j2 | j3 | j4 | j5 | j6 | Value (real) | Sign |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for s in sorted(result['symbols'], key=lambda x: abs(x['real']), reverse=True)[:50]:
        j = s['spins']
        v = s['real']
        sign = '+' if v > 0 else ('-' if v < 0 else '0')
        lines.append(f"| {j[0]} | {j[1]} | {j[2]} | {j[3]} | {j[4]} | {j[5]} | {v:.6f} | {sign} |")

    if len(result['symbols']) > 50:
        lines.append(f"... and {len(result['symbols']) - 50} more entries")

    return "\n".join(lines)


def main():
    """Compute 6j-symbols at r = 3, 4, 5, 6 and analyze sign patterns."""
    all_results = {}
    all_tables = []

    for r in [3, 4, 5, 6]:
        result = compute_all_6j_symbols(r)
        all_results[r] = result
        all_tables.append(print_6j_table(result))

    print("\n" + "=" * 60)
    print("SUMMARY OF SIGN PATTERNS")
    print("=" * 60)
    for r in [3, 4, 5, 6]:
        res = all_results[r]
        status = "✓ Non-negative" if res['all_nonnegative'] else "✗ Mixed signs"
        print(f"  r = {r}: {res['sign_counts']}  →  {status}")

    print("\n" + "=" * 60)
    print("VIABILITY ASSESSMENT")
    print("=" * 60)
    if all_results[3]['all_nonnegative']:
        print("r = 3 has all non-negative 6j-symbols.")
        print("→ Turaev-Viro state sum at r=3 is manifestly positive.")
        print("→ TQFT positivity approach is VIABLE at this level.")
    else:
        print("r = 3 has mixed-sign 6j-symbols.")
        print("→ Manifest positivity of TV state sum FAILS at r=3.")
        viable = [r for r in [4, 5, 6] if all_results[r]['all_nonnegative']]
        if viable:
            print(f"→ But levels {viable} have non-negative 6j-symbols — try there.")
        else:
            print("→ No tested level has manifest positivity.")
            print("→ Need alternative: unitarity argument or web basis approach.")

    return all_results, "\n\n".join(all_tables)


if __name__ == "__main__":
    results, tables = main()
    
    output_dir = "/Users/kylemathewson/GraphColour/backgroundMaterial/agent1520/coordinator/manager_M4/sub_S1"
    with open(f"{output_dir}/6j_raw_output.txt", "w") as f:
        for r_val, res in results.items():
            f.write(f"\n=== r = {r_val} ===\n")
            for s in res['symbols']:
                j = s['spins']
                f.write(f"  {{{j[0]} {j[1]} {j[2]}; {j[3]} {j[4]} {j[5]}}} = {s['real']:.10f}\n")
    
    with open(f"{output_dir}/6j_tables.md", "w") as f:
        f.write("# Quantum 6j-Symbol Computation Results\n\n")
        f.write(tables)

"""
Lightweight ARBS shell builder: only A, D, L (no incidence/Dirac matrices,
which are unnecessary for C-004F and too large to build densely beyond
n~5). Reuses the identical construction rules from build_arbs.py.
"""
import numpy as np


def build_shells(n):
    shells = []
    offset = 0
    for k in range(n + 1):
        size = 2 ** k
        L_off = offset
        offset += size
        R_off = offset
        offset += size
        shells.append((L_off, size, R_off, size))
    N = offset

    edges = set()
    for k in range(n + 1):
        L_off, L_sz, R_off, R_sz = shells[k]
        for i in range(L_sz):
            u = L_off + i
            for j in range(R_sz):
                v = R_off + j
                edges.add((u, v) if u < v else (v, u))
    for k in range(1, n + 1):
        _, _, Rprev_off, Rprev_sz = shells[k - 1]
        Lk_off, Lk_sz, _, _ = shells[k]
        for i in range(Rprev_sz):
            u = Rprev_off + i
            for j in range(Lk_sz):
                v = Lk_off + j
                edges.add((u, v) if u < v else (v, u))
    edges = sorted(edges)
    return N, edges, shells


def analyze_light(n):
    N, edges, shells = build_shells(n)
    A = np.zeros((N, N), dtype=np.float64)
    for (u, v) in edges:
        A[u, v] = 1.0
        A[v, u] = 1.0
    d = A.sum(axis=1)
    D = np.diag(d)
    L = D - A
    E = len(edges)
    return {"n": n, "N": N, "E": E, "A": A, "D": D, "L": L, "d": d, "shells": shells, "edges": edges}

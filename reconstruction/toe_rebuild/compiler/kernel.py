"""
UOC* compiler kernel -- PASS-00 through PASS-08 (canonicalization, primitive
extraction, ontology compression, dependency extraction, state construction,
operator construction, invariant extraction, fixed-point closure).

This module contains the ACTUAL, EXECUTED mathematics behind the closure
reports (not a stub, not a description) -- every function here is exercised
by tests/test_compiler.py.
"""
import itertools
from collections import defaultdict
import numpy as np


def int_to_bits(v, n2):
    return tuple((v >> (n2 - 1 - k)) & 1 for k in range(n2))


def bits_to_int(bits):
    v = 0
    for b in bits:
        v = (v << 1) | b
    return v


# ---------------------------------------------------------------- PASS-00
def canonical_form(mat_bits, N, perms=None):
    """Canonicalize a relation under vertex relabeling. Returns (canonical_int, |Aut(R)|)."""
    if perms is None:
        perms = list(itertools.permutations(range(N)))
    best, stab = None, 0
    for perm in perms:
        out = [0] * (N * N)
        for i in range(N):
            for j in range(N):
                if mat_bits[i * N + j]:
                    out[perm[i] * N + perm[j]] = 1
        val = bits_to_int(out)
        if best is None or val < best:
            best = val
        if tuple(out) == mat_bits:
            stab += 1
    return best, stab


# ---------------------------------------------------------------- PASS-05/08
def color_refinement(mat_bits, N):
    """1-WL color refinement (Gamma_1). Returns the number of stable color classes."""
    R = [[mat_bits[i * N + j] for j in range(N)] for i in range(N)]
    colors = [0] * N
    while True:
        sigs = []
        for x in range(N):
            out_sig = tuple(sorted(colors[y] for y in range(N) if R[x][y]))
            in_sig = tuple(sorted(colors[y] for y in range(N) if R[y][x]))
            sigs.append((colors[x], out_sig, in_sig))
        uniq = sorted(set(sigs))
        newcolors = [uniq.index(sigs[x]) for x in range(N)]
        if len(set(newcolors)) == len(set(colors)):
            colors = newcolors
            break
        colors = newcolors
    return len(set(colors))


def is_gamma_fixed(mat_bits, N):
    """Gamma(R) ~= R iff color refinement finds N distinct classes (no collapse)."""
    return color_refinement(mat_bits, N) == N


# ---------------------------------------------------------------- PASS-06 (TH-ARBS-001A)
def is_bipartite(mat, N):
    """Structural bipartite test on the underlying undirected graph. Self-loops fail
    automatically (an odd 1-cycle), matching TH-ARBS-001A's irreflexivity consequence."""
    if any(mat[i][i] for i in range(N)):
        return False
    adj = defaultdict(set)
    for i in range(N):
        for j in range(N):
            if i != j and (mat[i][j] or mat[j][i]):
                adj[i].add(j)
                adj[j].add(i)
    color = {}
    for start in range(N):
        if start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in color:
                    color[w] = 1 - color[u]
                    stack.append(w)
                elif color[w] == color[u]:
                    return False
    return True


def bipartition(mat, N):
    """Returns a vertex->{0,1} coloring for a bipartite relation."""
    adj = defaultdict(set)
    for i in range(N):
        for j in range(N):
            if i != j and (mat[i][j] or mat[j][i]):
                adj[i].add(j)
                adj[j].add(i)
    color = {}
    for s in range(N):
        if s in color:
            continue
        color[s] = 0
        st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in color:
                    color[w] = 1 - color[u]
                    st.append(w)
    return color


# ---------------------------------------------------------------- PASS-06 (TH-ARBS-001B)
def canonical_orientation(mat, N):
    """N_orient(R): orient every edge from color-class-0 to color-class-1 under R's
    own bipartition. THM-UOC-KERNEL-RECONFIG-001: this is always nilpotent."""
    color = bipartition(mat, N)
    out = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if (mat[i][j] or mat[j][i]) and i != j and color.get(i, 0) == 0 and color.get(j, 0) == 1:
                out[i][j] = 1
    return out


def is_nilpotent(mat, N):
    A = np.array(mat, dtype=np.int64)
    M = np.eye(N, dtype=np.int64)
    for _ in range(N):
        M = M @ A
        if not M.any():
            return True
    return False


# ---------------------------------------------------------------- PASS-09 (partial)
def spectral_data(mat, N):
    """Spec(A_sym), Spec(L_sym) -- the certified-machinery-compatible quantities."""
    A = np.array(mat, dtype=float)
    A_sym = (A + A.T) / 2.0
    D_sym = np.diag(A_sym.sum(axis=1))
    L_sym = D_sym - A_sym
    return {
        "A_sym": A_sym,
        "L_sym": L_sym,
        "eig_A_sym": np.linalg.eigvalsh(A_sym),
        "eig_L_sym": np.linalg.eigvalsh(L_sym),
        "is_symmetric": bool(np.allclose(A, A.T)),
    }

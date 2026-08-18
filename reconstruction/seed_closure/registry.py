"""
UOC-C0-SEED-CANONICALITY-002
Full candidate registry + filter/selector lattice + spectral/persistence closure.
"""
import itertools, json, math
from collections import defaultdict
import numpy as np
import sympy as sp

def int_to_bits(v, n2):
    return tuple((v >> (n2 - 1 - k)) & 1 for k in range(n2))

def color_refinement(mat_bits, N):
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

def canonical_form(mat_bits, N, perms):
    best, stab = None, 0
    for perm in perms:
        out = [0] * (N * N)
        for i in range(N):
            for j in range(N):
                if mat_bits[i * N + j]:
                    out[perm[i] * N + perm[j]] = 1
        val = 0
        for b in out:
            val = (val << 1) | b
        if best is None or val < best:
            best = val
        if tuple(out) == mat_bits:
            stab += 1
    return best, stab

def is_bipartite_underlying(mat, N):
    """TH-ARBS-001A test: does the UNDIRECTED underlying simple graph admit a proper
    2-coloring (V=V0 u V1, all edges cross)? Self-loops always fail this (odd 1-cycle)."""
    adj = defaultdict(set)
    has_self_loop = any(mat[i][i] for i in range(N))
    if has_self_loop:
        return False
    for i in range(N):
        for j in range(N):
            if i != j and (mat[i][j] or mat[j][i]):
                adj[i].add(j); adj[j].add(i)
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

def is_nilpotent_directed(mat, N):
    """TH-ARBS-001B test (as applied to an ALREADY-directed R): A_R nilpotent
    <=> the digraph (including self-loops as length-1 cycles) has no directed
    cycle at all, i.e. is a DAG. Tested directly via matrix powers AND via
    cycle detection, cross-checked against each other."""
    A = np.array(mat, dtype=np.int64)
    M = np.eye(N, dtype=np.int64)
    nilpotent_by_power = False
    for _ in range(N):
        M = M @ A
        if not M.any():
            nilpotent_by_power = True
            break
    # cross-check via cycle detection (DFS)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * N
    def dfs(u):
        color[u] = GRAY
        for v in range(N):
            if mat[u][v]:
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE and dfs(v):
                    return True
        color[u] = BLACK
        return False
    has_cycle = any(dfs(u) for u in range(N) if color[u] == WHITE)
    acyclic = not has_cycle
    assert nilpotent_by_power == acyclic, "nilpotency/acyclicity mismatch -- bug"
    return nilpotent_by_power

def full_invariants(bits, N, aut):
    mat = [[bits[i * N + j] for j in range(N)] for i in range(N)]
    A = np.array(mat, dtype=float)
    A_sym = (A + A.T) / 2.0
    out_deg = [sum(mat[i]) for i in range(N)]
    in_deg = [sum(mat[i][j] for i in range(N)) for j in range(N)]
    n_loops = sum(mat[i][i] for i in range(N))
    n_edges = int(A.sum())
    is_symmetric = all(mat[i][j] == mat[j][i] for i in range(N) for j in range(N))
    is_antisymmetric = all(not (i != j and mat[i][j] == 1 and mat[j][i] == 1) for i in range(N) for j in range(N))
    is_reflexive = all(mat[i][i] == 1 for i in range(N))
    is_irreflexive = all(mat[i][i] == 0 for i in range(N))
    is_functional = all(out_deg[i] == 1 for i in range(N))
    is_injective_as_map = is_functional and len(set(
        [j for i in range(N) for j in range(N) if mat[i][j]]
    )) == N if is_functional else False
    is_surjective_as_map = is_functional and set(
        j for i in range(N) for j in range(N) if mat[i][j]
    ) == set(range(N)) if is_functional else False
    # transitivity: R(x,y) & R(y,z) => R(x,z)
    is_transitive = all(
        (not (mat[x][y] and mat[y][z])) or mat[x][z]
        for x in range(N) for y in range(N) for z in range(N)
    )
    # weak/strong connectivity
    adj_und = defaultdict(set)
    for i in range(N):
        for j in range(N):
            if mat[i][j] and i != j:
                adj_und[i].add(j); adj_und[j].add(i)
    seen = set([0]); stack=[0]
    while stack:
        u = stack.pop()
        for w in adj_und[u]:
            if w not in seen:
                seen.add(w); stack.append(w)
    weakly_connected = (len(seen) == N)
    def reachable_from(s):
        seen2=set([s]); st=[s]
        while st:
            u=st.pop()
            for w in range(N):
                if mat[u][w] and w not in seen2:
                    seen2.add(w); st.append(w)
        return seen2
    strongly_connected = all(len(reachable_from(s)) == N for s in range(N))
    # weakly-connected component count
    comp_seen=set(); n_components=0
    for s in range(N):
        if s in comp_seen: continue
        n_components+=1
        st=[s]; comp_seen.add(s)
        while st:
            u=st.pop()
            for w in adj_und[u]:
                if w not in comp_seen:
                    comp_seen.add(w); st.append(w)
    acyclic = is_nilpotent_directed(mat, N)
    bipartite = is_bipartite_underlying(mat, N)

    # spectra
    eig_A_sym = np.linalg.eigvalsh(A_sym)
    D = np.diag([sum(mat[i]) for i in range(N)])  # out-degree diagonal for directed L
    D_sym = np.diag(A_sym.sum(axis=1))
    L_sym = D_sym - A_sym
    eig_L_sym = np.linalg.eigvalsh(L_sym)
    deg_for_norm = A_sym.sum(axis=1)
    with np.errstate(divide='ignore'):
        dinv_sqrt = np.array([1/np.sqrt(d) if d > 0 else 0.0 for d in deg_for_norm])
    L_norm = np.eye(N) - (dinv_sqrt[:,None]*A_sym*dinv_sqrt[None,:])
    eig_L_norm = np.linalg.eigvalsh(L_norm)
    A_complex_eig = np.linalg.eigvals(A)
    real_spectrum_A = bool(np.allclose(A_complex_eig.imag, 0, atol=1e-9))

    Asym_matrix = sp.Matrix(A_sym.tolist())
    charpoly = str(sp.factor(Asym_matrix.charpoly().as_expr()))
    # A_sym is real symmetric => always diagonalizable => minimal polynomial has no
    # repeated roots => it is the product (x - lambda) over DISTINCT eigenvalues.
    x = sp.Symbol('x')
    distinct_eigs = sorted(set(round(e, 6) for e in eig_A_sym.tolist()))
    minpoly_expr = sp.prod([x - sp.nsimplify(e, rational=False) for e in distinct_eigs])
    minpoly = str(sp.expand(minpoly_expr))
    rank = int(np.linalg.matrix_rank(A))
    rank_sym = int(np.linalg.matrix_rank(A_sym))
    nullity_sym = N - rank_sym
    spectral_gap_sym = float(sorted(eig_L_sym)[1] - sorted(eig_L_sym)[0]) if N > 1 else 0.0
    laplacian_nullity = int(sum(1 for e in eig_L_sym if abs(e) < 1e-9))

    return {
        "adjacency_matrix": mat, "n_edges": n_edges, "in_degree_seq": in_deg, "out_degree_seq": out_deg,
        "degree_multiset": sorted(in_deg) + sorted(out_deg), "n_loops": n_loops,
        "weakly_connected": weakly_connected, "strongly_connected": strongly_connected,
        "n_weak_components": n_components,
        "functional": is_functional, "injective_as_map": is_injective_as_map, "surjective_as_map": is_surjective_as_map,
        "symmetric": is_symmetric, "antisymmetric": is_antisymmetric,
        "reflexive": is_reflexive, "irreflexive": is_irreflexive,
        "transitive": is_transitive, "acyclic_nilpotent": acyclic,
        "bipartite_TH_ARBS_001A": bipartite, "nilpotent_TH_ARBS_001B": acyclic,
        "aut_group_order": aut, "rigid": (aut == 1),
        "adjacency_spectrum_real_part": sorted(A_complex_eig.real.round(8).tolist()),
        "adjacency_spectrum_is_real": real_spectrum_A,
        "symmetrized_adjacency_spectrum": sorted(eig_A_sym.round(8).tolist()),
        "laplacian_spectrum_symmetrized": sorted(eig_L_sym.round(8).tolist()),
        "normalized_laplacian_spectrum_symmetrized": sorted(eig_L_norm.round(8).tolist()),
        "spectral_gap_symmetrized_laplacian": spectral_gap_sym,
        "laplacian_nullity_symmetrized": laplacian_nullity,
        "rank_A": rank, "rank_A_sym": rank_sym, "nullity_A_sym": nullity_sym,
        "characteristic_polynomial_A_sym": charpoly,
        "minimal_polynomial_A_sym": minpoly,
    }

def build_registry(N):
    verts = list(range(N))
    perms = list(itertools.permutations(verts))
    n2 = N * N
    canon_map = {}
    for v in range(2 ** n2):
        bits = int_to_bits(v, n2)
        k = color_refinement(bits, N)
        if k != N:
            continue
        canon, aut = canonical_form(bits, N, perms)
        if canon not in canon_map:
            canon_map[canon] = {"bits": bits, "aut": aut}
    registry = []
    for i, (canon, info) in enumerate(sorted(canon_map.items())):
        inv = full_invariants(info["bits"], N, info["aut"])
        inv["seed_id"] = f"N{N}-{i:04d}"
        inv["N"] = N
        registry.append(inv)
    return registry

if __name__ == "__main__":
    all_registry = {}
    for N in [2, 3, 4]:
        print(f"Building full registry for N={N} ...")
        reg = build_registry(N)
        all_registry[N] = reg
        print(f"  {len(reg)} records built.")

    with open("/home/user/URSP/reconstruction/seed_candidate_full_registry.json", "w") as f:
        json.dump(all_registry, f, indent=2)
    print("saved seed_candidate_full_registry.json")

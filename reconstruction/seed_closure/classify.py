"""
Full classification catalog of Gamma-fixed relations (N=1..4), per section 8/20's
required labels, plus explicit small (N=1,2) examples printed symbolically.
Builds on compute.py's helper functions.
"""
import itertools, json
from collections import defaultdict

src = open("compute.py").read()
helpers = src.split("results_by_N = {}")[0]
exec(helpers)


def classify_relation(bits, N):
    mat = [[bits[i * N + j] for j in range(N)] for i in range(N)]
    n_edges = sum(bits)
    is_empty = (n_edges == 0)
    is_universal = (n_edges == N * N)
    is_identity = all(mat[i][j] == (1 if i == j else 0) for i in range(N) for j in range(N))
    is_symmetric = all(mat[i][j] == mat[j][i] for i in range(N) for j in range(N))
    is_asymmetric_strict = all(not (mat[i][j] == 1 and mat[j][i] == 1) for i in range(N) for j in range(N) if i != j)
    is_functional = all(sum(mat[i]) == 1 for i in range(N))
    has_self_loop = any(mat[i][i] for i in range(N))
    # connectivity (weakly connected, treating R as directed graph, underlying undirected)
    adj = defaultdict(set)
    for i in range(N):
        for j in range(N):
            if mat[i][j] and i != j:
                adj[i].add(j); adj[j].add(i)
    seen = set()
    if N > 0:
        stack = [0]
        seen.add(0)
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); stack.append(y)
    is_connected = (len(seen) == N)
    # cyclicity (directed cycle of length >=1, i.e. self-loop counts as a cycle too)
    def has_directed_cycle():
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
        return any(dfs(u) for u in range(N) if color[u] == WHITE)
    is_cyclic = has_directed_cycle()
    return {
        "n_vertices": N, "n_edges": n_edges,
        "empty": is_empty, "universal": is_universal, "identity": is_identity,
        "symmetric": is_symmetric, "asymmetric_strict": is_asymmetric_strict,
        "functional": is_functional, "self_looped": has_self_loop,
        "connected": is_connected, "cyclic": is_cyclic,
        "nontrivial": not (is_empty or is_universal or is_identity),
    }


catalog = {}
for N in range(1, 5):
    verts = list(range(N))
    perms = list(itertools.permutations(verts))
    n2 = N * N
    fixed_reps = []
    seen_canon = set()
    for v in range(2 ** n2):
        bits = int_to_bits(v, n2)
        classes, quot_bits, k, eq_ok = color_refinement(bits, N)
        if k == N:
            canon, aut = canonical_form(bits, N, perms)
            if canon not in seen_canon:
                seen_canon.add(canon)
                cls = classify_relation(bits, N)
                cls["aut_size"] = aut
                cls["adjacency_matrix"] = [list(bits[i * N:(i + 1) * N]) for i in range(N)]
                fixed_reps.append(cls)
    # counts by label
    label_counts = defaultdict(int)
    for r in fixed_reps:
        for k2 in ["empty", "universal", "identity", "nontrivial", "symmetric",
                   "asymmetric_strict", "functional", "self_looped", "connected", "cyclic"]:
            if r[k2]:
                label_counts[k2] += 1
    catalog[N] = {
        "N": N,
        "total_relations_raw": 2 ** n2,
        "total_isomorphism_classes_all_relations": None,  # filled from compute.py's JSON separately
        "fixed_point_isomorphism_classes": len(fixed_reps),
        "label_counts_among_fixed_classes": dict(label_counts),
        "all_fixed_reps": fixed_reps,
    }
    print(f"N={N}: {len(fixed_reps)} fixed iso-classes; label counts: {dict(label_counts)}")

with open("/home/user/URSP/reconstruction/seed_fixed_point_full_catalog.json", "w") as f:
    json.dump(catalog, f, indent=2)
print("saved seed_fixed_point_full_catalog.json")

# print N=1,2 fully explicit for the report
print("\n--- N=1 fixed points (all) ---")
for r in catalog[1]["all_fixed_reps"]:
    print(r["adjacency_matrix"], {k: r[k] for k in ["empty","universal","identity","self_looped","nontrivial"]})
print("\n--- N=2 fixed points (all 6) ---")
for r in catalog[2]["all_fixed_reps"]:
    print(r["adjacency_matrix"], {k: r[k] for k in ["empty","universal","identity","symmetric",
          "asymmetric_strict","functional","self_looped","connected","cyclic","nontrivial","aut_size"]})

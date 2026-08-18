"""
Runs the semantic-functor bridge test (compiler/ncg_bridge.py) over every
seed in F_N^derived_v2 for N=2,3,4,5, and reports honest, aggregate results.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compiler import kernel, enumerate_admissible_seeds
from compiler import ncg_bridge

def get_n5_candidates():
    """Reuse the N=5 bipartite construction from n5_bipartite.py to get the
    actual adjacency matrices (not just counts)."""
    N = 5
    import numpy as np
    from collections import defaultdict
    verts = list(range(N))
    perms = list(itertools.permutations(verts))

    def gen_bipartite_relations():
        seen_raw = set()
        for a_size in range(1, N):
            for A in itertools.combinations(verts, a_size):
                A = set(A)
                B = [v for v in verts if v not in A]
                Al = sorted(A)
                edge_slots = [(i, j) for i in Al for j in B] + [(i, j) for i in B for j in Al]
                n_slots = len(edge_slots)
                for mask in range(2 ** n_slots):
                    bits = [0] * (N * N)
                    for k, (i, j) in enumerate(edge_slots):
                        if (mask >> k) & 1:
                            bits[i * N + j] = 1
                    seen_raw.add(tuple(bits))
        return seen_raw

    raw = gen_bipartite_relations()
    fixed_canon = {}
    for bits in raw:
        k = kernel.color_refinement(bits, N)
        if k != N:
            continue
        canon, aut = kernel.canonical_form(bits, N, perms)
        if canon not in fixed_canon:
            mat = [list(bits[i*N:(i+1)*N]) for i in range(N)]
            if kernel.is_bipartite(mat, N):
                fixed_canon[canon] = mat
    return list(fixed_canon.values())


all_results = {}
for N in [2, 3, 4, 5]:
    print(f"=== N={N} ===")
    if N <= 4:
        seeds = enumerate_admissible_seeds(N)
        mats = [s.adjacency_matrix for s in seeds]
    else:
        mats = get_n5_candidates()
    print(f"  {len(mats)} candidates")

    n_phase1_ok = 0
    ko_class_counts = {}
    n_order_zero_ok = {True: 0, False: 0}
    n_first_order_ok = {True: 0, False: 0}

    for mat in mats:
        res = ncg_bridge.full_bridge_test(mat, N)
        p1 = res["phase1"]
        if all(p1.values()):
            n_phase1_ok += 1
        for same_sign in [True, False]:
            r = res[f"phase2_3_same_sign={same_sign}"]
            for ko in r["matched_KO_dimensions_mod_8"]:
                ko_class_counts.setdefault((same_sign, ko), 0)
                ko_class_counts[(same_sign, ko)] += 1
            if r["order_zero_holds_for_diagonal_algebra"]:
                n_order_zero_ok[same_sign] += 1
            if r["first_order_holds_for_diagonal_algebra"]:
                n_first_order_ok[same_sign] += 1

    result = {
        "N": N, "n_candidates": len(mats),
        "n_phase1_structural_axioms_pass": n_phase1_ok,
        "ko_class_matches": {f"same_sign={k[0]}_KO={k[1]}": v for k, v in ko_class_counts.items()},
        "n_order_zero_pass_same_sign": n_order_zero_ok[True],
        "n_order_zero_pass_opposite_sign": n_order_zero_ok[False],
        "n_first_order_pass_same_sign": n_first_order_ok[True],
        "n_first_order_pass_opposite_sign": n_first_order_ok[False],
    }
    all_results[N] = result
    print(json.dumps(result, indent=2))

with open("/home/user/URSP/reconstruction/uoc_semantic_functor_bridge_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("\nsaved uoc_semantic_functor_bridge_results.json")

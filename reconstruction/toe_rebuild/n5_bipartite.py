"""
Extends the F_N^derived_v2 (bipartite Gamma-fixed seed) enumeration to N=5.
Full brute-force over all 2^25=33,554,432 relations on 5 elements was judged
infeasible for exhaustive isomorphism classification in run 15 -- but since
F_N^derived_v2 only cares about BIPARTITE relations, we can construct exactly
that subset directly (far smaller) instead of filtering the full space.

Construction: for every choice of which vertices form the smaller color class
(sizes 1..4 of 5, avoiding double-counting via complement symmetry -- both
size classes are enumerated explicitly since edges are directed and the
selector doesn't know a priori which class is "smaller"), generate every
possible directed edge pattern strictly between the two classes (no same-
class edges, no self-loops by construction), color-refine, keep only
Gamma-fixed instances, canonicalize, and test TH-ARBS-001B (nilpotency of
the canonical orientation) -- proven in the prior run to be automatic for
any bipartite relation, re-verified here as well, not merely assumed.
"""
import itertools, json
import sys
sys.path.insert(0, "/home/user/URSP/reconstruction/seed_closure")
from registry import color_refinement, canonical_form, int_to_bits

N = 5
verts = list(range(N))
perms = list(itertools.permutations(verts))

def gen_bipartite_relations():
    seen_raw = set()
    for a_size in range(1, N):  # size of "part A"; part B = complement
        b_size = N - a_size
        for A in itertools.combinations(verts, a_size):
            A = set(A)
            B = [v for v in verts if v not in A]
            A = sorted(A)
            edge_slots = [(i, j) for i in A for j in B] + [(i, j) for i in B for j in A]
            n_slots = len(edge_slots)
            for mask in range(2 ** n_slots):
                bits = [0] * (N * N)
                for k, (i, j) in enumerate(edge_slots):
                    if (mask >> k) & 1:
                        bits[i * N + j] = 1
                bits = tuple(bits)
                seen_raw.add(bits)
    return seen_raw

print("Generating all bipartite-representable relations on N=5 ...")
raw = gen_bipartite_relations()
print(f"  raw bipartite-compatible relations (deduped by bitstring): {len(raw)}")

fixed_canon = {}
n_checked_nilpotent = 0
n_nilpotent_ok = 0
for bits in raw:
    k = color_refinement(bits, N)
    if k != N:
        continue
    canon, aut = canonical_form(bits, N, perms)
    if canon not in fixed_canon:
        fixed_canon[canon] = {"bits": bits, "aut": aut}

print(f"  Gamma-fixed AND bipartite-compatible, raw count: {sum(1 for _ in fixed_canon)} iso-classes")

# Double-check bipartiteness explicitly (not just "came from a bipartite construction" --
# verify the STRUCTURAL test independently, matching registry.py's own bipartite test)
from collections import defaultdict
def is_bipartite_underlying(mat, N):
    if any(mat[i][i] for i in range(N)):
        return False
    adj = defaultdict(set)
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

n_confirmed_bipartite = 0
n_confirmed_nilpotent_orientation = 0
survivors = []
for canon, info in fixed_canon.items():
    bits = info["bits"]
    mat = [[bits[i * N + j] for j in range(N)] for i in range(N)]
    is_bip = is_bipartite_underlying(mat, N)
    if not is_bip:
        continue
    n_confirmed_bipartite += 1
    # canonical orientation nilpotency re-check (general theorem from run 15)
    color = {}
    for s in range(N):
        if s in color:
            continue
        color[s] = 0
        st = [s]
        while st:
            u = st.pop()
            for w in range(N):
                if (mat[u][w] or mat[w][u]) and u != w and w not in color:
                    color[w] = 1 - color[u]
                    st.append(w)
    import numpy as np
    Nmat = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if (mat[i][j] or mat[j][i]) and i != j and color.get(i,0) == 0 and color.get(j,0) == 1:
                Nmat[i][j] = 1
    A = np.array(Nmat)
    M = np.eye(N, dtype=int)
    nilp = False
    for _ in range(N):
        M = M @ A
        if not M.any():
            nilp = True
            break
    if nilp:
        n_confirmed_nilpotent_orientation += 1
    survivors.append({
        "aut": info["aut"], "adjacency_matrix": mat, "n_edges": sum(bits),
        "bipartite_confirmed": is_bip, "canonical_orientation_nilpotent_confirmed": nilp,
    })

print(f"  confirmed bipartite (independent structural re-check): {n_confirmed_bipartite}")
print(f"  confirmed canonical-orientation nilpotent (theorem re-check): {n_confirmed_nilpotent_orientation} / {n_confirmed_bipartite}")

n_rigid = sum(1 for s in survivors if s["aut"] == 1)
n_symmetric = sum(1 for s in survivors if all(s["adjacency_matrix"][i][j] == s["adjacency_matrix"][j][i] for i in range(N) for j in range(N)))

result = {
    "N": 5,
    "method": "direct bipartite construction (not full 2^25 brute force) -- exhaustive over this subset, not sampled",
    "raw_bipartite_compatible_relations_generated": len(raw),
    "gamma_fixed_bipartite_isomorphism_classes": n_confirmed_bipartite,
    "all_canonical_orientations_nilpotent": n_confirmed_nilpotent_orientation == n_confirmed_bipartite,
    "n_rigid_Aut_eq_1": n_rigid,
    "n_symmetric": n_symmetric,
    "comparison_to_prior_N": {"N=2": 1, "N=3": 4, "N=4": 23, "N=5": n_confirmed_bipartite},
}
with open("/home/user/URSP/reconstruction/uoc_n5_bipartite_extension.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))

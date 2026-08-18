"""
UOC-C0-SEED-CANONICALITY-002
Independent recomputation and cross-validation of the C0 fixed-point family,
using a DIFFERENT isomorphism method (networkx VF2 exact isomorphism on
DiGraphs with self-loops) than the original permutation-minimization
canonicalization, per Rule 0.2 (recompute before using, do not blindly trust).
"""
import itertools, json, sys
import networkx as nx

sys.path.insert(0, "/home/user/URSP/reconstruction/seed_closure")
# Re-derive (not import-trust) the color-refinement machinery inline, fresh.

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
    k = len(set(colors))
    return k

def bits_to_digraph(bits, N):
    G = nx.DiGraph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(N):
            if bits[i * N + j]:
                G.add_edge(i, j)
    return G

results = {}
for N in range(2, 5):
    n2 = N * N
    total = 2 ** n2
    fixed_bits_list = []
    for v in range(total):
        bits = int_to_bits(v, n2)
        k = color_refinement(bits, N)
        if k == N:
            fixed_bits_list.append(bits)
    print(f"N={N}: raw fixed relations (all labelings) = {len(fixed_bits_list)}")

    # Independent isomorphism classification via networkx VF2 (exact, not WL-hash approx)
    # Bucket first by a cheap WL hash to avoid O(n^2) pairwise VF2 on the full raw list,
    # then confirm exact isomorphism within each bucket with nx.is_isomorphic (VF2) --
    # the WL hash is only a SPEED filter, never itself the isomorphism decision.
    buckets = {}
    for bits in fixed_bits_list:
        G = bits_to_digraph(bits, N)
        h = nx.weisfeiler_lehman_graph_hash(G)
        buckets.setdefault(h, []).append((bits, G))

    n_classes = 0
    class_sizes = []
    for h, items in buckets.items():
        # within this WL-hash bucket, partition further by EXACT isomorphism (VF2)
        reps = []  # list of (representative_graph, count)
        for bits, G in items:
            placed = False
            for rep_G, count_holder in reps:
                if nx.is_isomorphic(rep_G, G):
                    count_holder[0] += 1
                    placed = True
                    break
            if not placed:
                reps.append((G, [1]))
        n_classes += len(reps)
        class_sizes.extend(count_holder[0] for _, count_holder in reps)

    print(f"N={N}: independent (networkx VF2) isomorphism classes among fixed relations = {n_classes}")
    assert sum(class_sizes) == len(fixed_bits_list), "class size sum mismatch -- bug"
    results[N] = {
        "N": N,
        "raw_fixed_relations": len(fixed_bits_list),
        "independent_isomorphism_classes_networkx_VF2": n_classes,
        "class_sizes_sum_check": sum(class_sizes) == len(fixed_bits_list),
    }

with open("/home/user/URSP/reconstruction/seed_recompute_crosscheck.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nsaved seed_recompute_crosscheck.json")
print(json.dumps(results, indent=2))

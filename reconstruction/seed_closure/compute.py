"""
UOC-C0-MINIMAL-SEED-CLOSURE-001
Exact/exhaustive combinatorial computation backing the seed-closure derivation.

No physical-target values (32, N_H, CKM, PMNS, etc.) appear anywhere in this
file or are used to select any object. Every selection criterion below is
either an explicit isomorphism-invariance/canonicality argument or an
exhaustive/brute-force computation over finite combinatorial objects.
"""
import itertools, json, math
from collections import defaultdict

OUT = "/home/user/URSP/reconstruction"

# ============================================================
# PART A -- CANDIDATE A: bare distinction Delta = (X, ~)
#   Represent ~ as a set partition of X = {0,...,N-1}.
#   End(Delta) = {f: X->X : x~y => f(x)~f(y)}
#   Aut(Delta) = bijective elements of End(Delta) whose inverse is also in End(Delta)
# ============================================================

def set_partitions(collection):
    """Yield all set partitions of a list, as list-of-frozensets."""
    collection = list(collection)
    if len(collection) == 1:
        yield [frozenset(collection)]
        return
    first = collection[0]
    for smaller in set_partitions(collection[1:]):
        # insert `first` into each existing block
        for i in range(len(smaller)):
            new_partition = smaller[:i] + [smaller[i] | {first}] + smaller[i+1:]
            yield new_partition
        # or `first` as its own block
        yield [frozenset([first])] + smaller

def brute_end_aut(partition, X):
    """Brute-force End/Aut by testing every function X->X. Only for tiny N (validation)."""
    block_of = {}
    for b in partition:
        for x in b:
            block_of[x] = b
    n = len(X)
    end_count = 0
    aut_count = 0
    for f_tuple in itertools.product(X, repeat=n):
        f = dict(zip(X, f_tuple))
        preserves = all(block_of[f[x]] == block_of[f[y]] for b in partition for x in b for y in b)
        if preserves:
            end_count += 1
            if len(set(f_tuple)) == n:  # bijective
                # check inverse also preserves ~ : bijective + preserves forward => it's an automorphism
                # (forward preservation of a bijection between finite equal-size sets already forces
                #  block-to-block bijection, hence backward preservation too -- verified explicitly below)
                inv = {f[x]: x for x in X}
                inv_preserves = all(block_of[inv[x]] == block_of[inv[y]] for b in partition for x in b for y in b)
                if inv_preserves:
                    aut_count += 1
    return end_count, aut_count

def formula_end_aut(block_sizes):
    """Closed-form |End(Delta)| and |Aut(Delta)| from block-size multiset (see derivation in report)."""
    k = len(block_sizes)
    end_total = 0
    for sigma in itertools.product(range(k), repeat=k):
        term = 1
        for i in range(k):
            term *= block_sizes[sigma[i]] ** block_sizes[i]
        end_total += term
    # Aut: sigma must be a permutation of [k] with block_sizes[sigma(i)] == block_sizes[i] for all i
    aut_total = 0
    for sigma in itertools.permutations(range(k)):
        if all(block_sizes[sigma[i]] == block_sizes[i] for i in range(k)):
            term = 1
            for s in block_sizes:
                term *= math.factorial(s)
            aut_total += term
    return end_total, aut_total

delta_results = []
for N in range(1, 7):
    X = list(range(N))
    seen_shapes = set()
    for partition in set_partitions(X):
        block_sizes = tuple(sorted((len(b) for b in partition), reverse=True))
        if block_sizes in seen_shapes:
            continue
        seen_shapes.add(block_sizes)
        end_f, aut_f = formula_end_aut(block_sizes)
        entry = {
            "N": N,
            "block_sizes": list(block_sizes),
            "num_blocks": len(block_sizes),
            "End_size_formula": end_f,
            "Aut_size_formula": aut_f,
        }
        if N <= 4:
            end_b, aut_b = brute_end_aut(partition, X)
            entry["End_size_bruteforce"] = end_b
            entry["Aut_size_bruteforce"] = aut_b
            entry["formula_matches_bruteforce"] = (end_b == end_f and aut_b == aut_f)
        delta_results.append(entry)

# General theorem check: for N>=2, is Aut(Delta) always > 1 (i.e. never rigid)?
delta_never_rigid_for_N_geq_2 = all(
    e["Aut_size_formula"] > 1 for e in delta_results if e["N"] >= 2
)

print("=== CANDIDATE A: bare distinction Delta ===")
print(f"  Partition shapes tested: {len(delta_results)} (N=1..6)")
print(f"  All formula==bruteforce checks (N<=4) pass: "
      f"{all(e.get('formula_matches_bruteforce', True) for e in delta_results)}")
print(f"  Aut(Delta) > 1 for EVERY partition with N>=2: {delta_never_rigid_for_N_geq_2}")

# ============================================================
# PART B -- CANDIDATE C/D: pure relation R subset X x X, isomorphism
#   classification, automorphism groups, functionality, rigidity,
#   and the canonical Gamma operator (color refinement / 1-WL quotient).
# ============================================================

def all_perms_bitpermute(mat_bits, N, perm):
    """Given relation as N*N bit tuple (row-major), apply vertex permutation `perm`
    (perm[i] = new position of old vertex i) and return new bit tuple."""
    out = [0] * (N * N)
    for i in range(N):
        for j in range(N):
            if mat_bits[i * N + j]:
                ni, nj = perm[i], perm[j]
                out[ni * N + nj] = 1
    return tuple(out)

def bits_to_int(bits):
    v = 0
    for b in bits:
        v = (v << 1) | b
    return v

def int_to_bits(v, n2):
    return tuple((v >> (n2 - 1 - k)) & 1 for k in range(n2))

def canonical_form(mat_bits, N, perms):
    best = None
    stab = 0
    for perm in perms:
        permuted = all_perms_bitpermute(mat_bits, N, perm)
        val = bits_to_int(permuted)
        if best is None or val < best:
            best = val
        if permuted == mat_bits:
            stab += 1
    return best, stab  # stab = |Aut(R)| (stabilizer size under this perm action)

def color_refinement(mat_bits, N):
    """1-WL color refinement. Returns (classes: list of frozensets of vertices,
    quotient_bits: tuple for the quotient relation, verified_equitable: bool)."""
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
    classes = [frozenset(x for x in range(N) if colors[x] == c) for c in range(k)]
    # Build quotient relation; verify equitability (constant edge-count per class-pair)
    equitable_ok = True
    quot = [[0] * k for _ in range(k)]
    for ci, cls_i in enumerate(classes):
        for cj, cls_j in enumerate(classes):
            counts = set()
            for x in cls_i:
                cnt = sum(1 for y in cls_j if R[x][y])
                counts.add(cnt)
            if len(counts) != 1:
                equitable_ok = False
                # fallback (should never trigger if color refinement is correct): record "any edge"
                quot[ci][cj] = 1 if any(c > 0 for c in counts) else 0
            else:
                quot[ci][cj] = 1 if next(iter(counts)) > 0 else 0
    quot_bits = tuple(quot[i][j] for i in range(k) for j in range(k))
    return classes, quot_bits, k, equitable_ok

def gamma_iterated(bits, N):
    """Gamma_infty: repeatedly (color-refine, build quotient) until the size stops
    shrinking. This is the operator that is actually provably idempotent -- see
    THM-SEED-FIXEDPOINT-001 in the report. One-shot color refinement (Gamma_1) is
    NOT idempotent in general (discovered by the numerical test below): the
    quotient graph, re-refined from a blank initial coloring, can collapse further
    whenever the quotient graph itself has a nontrivial automorphism, since 1-WL
    color refinement can never break symmetry that a fresh run has no way to see."""
    cur_bits, cur_N = bits, N
    steps = 0
    history = [cur_N]
    while True:
        classes, quot_bits, k, eq_ok = color_refinement(cur_bits, cur_N)
        steps += 1
        if k == cur_N:
            return cur_bits, cur_N, steps, history
        cur_bits, cur_N = quot_bits, k
        history.append(cur_N)
        if steps > 50:  # safety valve; cannot trigger since N is finite and strictly decreasing
            raise RuntimeError("gamma_iterated failed to converge")

results_by_N = {}
for N in range(1, 5):
    verts = list(range(N))
    perms = list(itertools.permutations(verts))
    n2 = N * N
    total_relations = 2 ** n2
    canon_map = {}   # canonical_int -> {"reps":.., "class_size":.., "aut":..}
    functional_count = 0
    for v in range(total_relations):
        bits = int_to_bits(v, n2)
        # functional check: each row has exactly one 1
        is_functional = all(sum(bits[i*N:(i+1)*N]) == 1 for i in range(N))
        if is_functional:
            functional_count += 1
        canon, aut = canonical_form(bits, N, perms)
        if canon not in canon_map:
            canon_map[canon] = {"aut": aut, "class_size": 0, "rep_bits": bits}
        canon_map[canon]["class_size"] += 1
    # sanity check: orbit-stabilizer: class_size * aut == N!
    orbit_stab_ok = all(
        info["class_size"] * info["aut"] == math.factorial(N) for info in canon_map.values()
    )
    # rigidity: how many iso-classes have Aut=1
    rigid_classes = sum(1 for info in canon_map.values() if info["aut"] == 1)
    # functional relations with Aut=1 (rigid functional graphs) -- need per-class functional flag
    rigid_functional_classes = 0
    for canon, info in canon_map.items():
        bits = info["rep_bits"]
        is_functional = all(sum(bits[i*N:(i+1)*N]) == 1 for i in range(N))
        info["is_functional_rep"] = is_functional
        if is_functional and info["aut"] == 1:
            rigid_functional_classes += 1

    # Gamma operator (color refinement quotient) + fixed point classification, on EVERY relation
    fixed_count = 0
    fixed_reps = []
    quotient_size_hist = defaultdict(int)
    equitable_failures = 0
    idempotence_failures = 0
    for canon, info in canon_map.items():
        bits = info["rep_bits"]
        classes, quot_bits, k, eq_ok = color_refinement(bits, N)
        if not eq_ok:
            equitable_failures += 1
        quotient_size_hist[k] += info["class_size"]
        is_fixed = (k == N)
        if is_fixed:
            fixed_count += info["class_size"]
            fixed_reps.append({
                "canon_int": canon, "aut": info["aut"],
                "class_size": info["class_size"], "is_functional": info["is_functional_rep"],
            })
        # idempotence check: applying Gamma to the quotient itself must not shrink it further
        if k < N:
            _, _, k2, _ = color_refinement(quot_bits, k)
            if k2 != k:
                idempotence_failures += 1
        else:
            # k==N: quotient relation should equal (up to relabeling) the original -- check same canon
            qcanon, _ = canonical_form(quot_bits, k, perms)
            if qcanon != canon:
                idempotence_failures += 1

    # Gamma_infty analysis: iterate to a TRUE fixed point, verify idempotence properly.
    gamma_infty_final_size_hist = defaultdict(int)   # raw relation count, by final size
    gamma_infty_steps_hist = defaultdict(int)
    gamma_infty_idempotence_failures = 0
    gamma_infty_primitively_fixed_classes = 0   # iso-classes with final_size == N (no collapse at all)
    gamma_infty_final_size_by_class = {}
    for canon, info in canon_map.items():
        bits = info["rep_bits"]
        final_bits, final_N, steps, history = gamma_iterated(bits, N)
        gamma_infty_final_size_hist[final_N] += info["class_size"]
        gamma_infty_steps_hist[steps] += info["class_size"]
        gamma_infty_final_size_by_class[canon] = final_N
        if final_N == N:
            gamma_infty_primitively_fixed_classes += 1
        # verify TRUE idempotence: applying gamma_iterated again to the output must
        # return immediately (1 step, unchanged size)
        _, final_N2, steps2, _ = gamma_iterated(final_bits, final_N)
        if not (final_N2 == final_N and steps2 == 1):
            gamma_infty_idempotence_failures += 1

    results_by_N[N] = {
        "N": N,
        "total_relations_raw": total_relations,
        "total_isomorphism_classes": len(canon_map),
        "orbit_stabilizer_identity_verified_for_all_classes": orbit_stab_ok,
        "functional_relations_raw_count": functional_count,
        "functional_relations_raw_count_formula_N_pow_N": N ** N,
        "functional_count_matches_formula": functional_count == N ** N,
        "rigid_isomorphism_classes_Aut_eq_1": rigid_classes,
        "rigid_functional_isomorphism_classes": rigid_functional_classes,
        "color_refinement_equitability_failures": equitable_failures,
        "gamma1_onestep_idempotence_failures": idempotence_failures,
        "gamma1_fixed_relations_raw_count": fixed_count,
        "gamma1_fixed_isomorphism_classes": len(fixed_reps),
        "quotient_size_histogram_raw_count": dict(quotient_size_hist),
        "fixed_reps_sample": fixed_reps[:8],
        "gamma_infty_final_size_histogram_raw_count": dict(gamma_infty_final_size_hist),
        "gamma_infty_steps_histogram_raw_count": dict(gamma_infty_steps_hist),
        "gamma_infty_idempotence_failures": gamma_infty_idempotence_failures,
        "gamma_infty_primitively_fixed_isomorphism_classes": gamma_infty_primitively_fixed_classes,
    }
    print(f"=== N={N}: relations ===")
    print(f"  total raw={total_relations}, iso-classes={len(canon_map)}, "
          f"orbit-stabilizer check passed={orbit_stab_ok}")
    print(f"  functional raw count={functional_count} (formula N^N={N**N}, match={functional_count==N**N})")
    print(f"  rigid (Aut=1) iso-classes={rigid_classes}, rigid+functional classes={rigid_functional_classes}")
    print(f"  color-refinement equitability failures={equitable_failures} (should be 0)")
    print(f"  Gamma_1 (one-shot) idempotence failures={idempotence_failures} "
          f"(nonzero => Gamma_1 is NOT idempotent, see report)")
    print(f"  Gamma_1-fixed: raw count={fixed_count}, iso-classes={len(fixed_reps)}")
    print(f"  quotient-size histogram (raw relation counts): {dict(quotient_size_hist)}")
    print(f"  Gamma_infty final-size histogram (raw): {dict(gamma_infty_final_size_hist)}")
    print(f"  Gamma_infty steps histogram (raw): {dict(gamma_infty_steps_hist)}")
    print(f"  Gamma_infty idempotence failures={gamma_infty_idempotence_failures} (should be 0)")
    print(f"  Gamma_infty primitively-fixed iso-classes (no collapse at all): "
          f"{gamma_infty_primitively_fixed_classes}")

# ============================================================
# PART C -- stability of Gamma-fixed points under single-edge perturbation (N=4)
# ============================================================
N = 4
n2 = N * N
verts = list(range(N))
perms4 = list(itertools.permutations(verts))
fixed_reps_N4 = results_by_N[4]["fixed_reps_sample"]  # only sample stored above; recompute full list here
full_fixed = []
for v in range(2 ** n2):
    bits = int_to_bits(v, n2)
    classes, quot_bits, k, eq_ok = color_refinement(bits, N)
    if k == N:
        full_fixed.append(bits)
print(f"\n=== Stability test (N=4): {len(full_fixed)} raw fixed relations (all labelings) ===")

# canonicalize the fixed set to get representatives (dedupe by isomorphism)
fixed_canon_seen = {}
for bits in full_fixed:
    canon, aut = canonical_form(bits, N, perms4)
    if canon not in fixed_canon_seen:
        fixed_canon_seen[canon] = bits

stability_records = []
for canon, bits in fixed_canon_seen.items():
    n_stable_flips = 0
    n_flips = n2
    flip_outcomes = []
    for pos in range(n2):
        pbits = list(bits)
        pbits[pos] = 1 - pbits[pos]
        pbits = tuple(pbits)
        _, _, k2, _ = color_refinement(pbits, N)
        stayed_fixed = (k2 == N)
        if stayed_fixed:
            n_stable_flips += 1
        flip_outcomes.append(k2)
    stability_records.append({
        "canon_int": canon,
        "n_edge_flips_tested": n_flips,
        "n_flips_remaining_fixed": n_stable_flips,
        "fraction_stable_under_1_flip": n_stable_flips / n_flips,
        "min_quotient_size_after_any_1_flip": min(flip_outcomes),
    })

avg_stability = sum(r["fraction_stable_under_1_flip"] for r in stability_records) / len(stability_records)
print(f"  distinct (iso-class) fixed points tested for stability: {len(stability_records)}")
print(f"  average fraction of 1-edge-flip perturbations that remain Gamma-fixed: {avg_stability:.4f}")
n_fully_unstable = sum(1 for r in stability_records if r["n_flips_remaining_fixed"] == 0)
n_fully_stable = sum(1 for r in stability_records if r["n_flips_remaining_fixed"] == r["n_edge_flips_tested"])
print(f"  fixed points where EVERY single-edge flip destabilizes: {n_fully_unstable}")
print(f"  fixed points where NO single-edge flip destabilizes (locally maximally stable): {n_fully_stable}")

# ============================================================
# SAVE
# ============================================================
with open(f"{OUT}/seed_delta_endaut.json", "w") as f:
    json.dump(delta_results, f, indent=2)

with open(f"{OUT}/seed_relation_iso.json", "w") as f:
    json.dump(results_by_N, f, indent=2)

with open(f"{OUT}/seed_stability_raw.json", "w") as f:
    json.dump({
        "N": N,
        "n_isomorphism_class_fixed_points": len(stability_records),
        "average_fraction_stable_under_1_flip": avg_stability,
        "n_fully_unstable_fixed_points": n_fully_unstable,
        "n_fully_stable_fixed_points": n_fully_stable,
        "records": stability_records,
    }, f, indent=2)

print("\nSaved: seed_delta_endaut.json, seed_relation_iso.json, seed_stability_raw.json")

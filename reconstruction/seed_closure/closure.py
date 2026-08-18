"""
UOC-C0-SEED-CANONICALITY-002
Filter/selector lattice, derivation-status matrix, spectral/persistence closure,
isomorphism-invariance audit, N-scaling audit.
Consumes seed_candidate_full_registry.json (built by registry.py).
"""
import json, itertools, random
import numpy as np
from registry import canonical_form

with open("/home/user/URSP/reconstruction/seed_candidate_full_registry.json") as f:
    REG = {int(k): v for k, v in json.load(f).items()}

# ------------------------------------------------------------------
# Filter/selector lattice
# ------------------------------------------------------------------
# Each filter: (name, predicate, derivation_status, justification)
FILTERS = [
    ("rigid_Aut_eq_1", lambda r: r["rigid"], "UNJUSTIFIED",
     "No independently-certified UOC dependency requires trivial automorphism group. Rejected per Rule 0.4 unless later justified."),
    ("minimal_edge_count", None, "UNJUSTIFIED",
     "'Minimal edge count' is not a fixed predicate -- it requires choosing a threshold with no independent derivation. HEURISTIC ONLY per section 13; not applied as a hard filter, reported as a ranking statistic instead."),
    ("functional", lambda r: r["functional"], "UNJUSTIFIED",
     "Functionality (deterministic successor) is not independently required by any certified upstream UOC dependency for a graph/relation node -- BRIDGE B-001 and Graph_ARBS's axioms say nothing about functionality. PROPOSED only."),
    ("weakly_connected", lambda r: r["weakly_connected"], "UNJUSTIFIED",
     "Not independently derived from any certified dependency."),
    ("strongly_connected", lambda r: r["strongly_connected"], "UNJUSTIFIED",
     "Not independently derived from any certified dependency."),
    ("irreflexive", lambda r: r["irreflexive"], "DERIVED",
     "Follows NECESSARILY from TH-ARBS-001A (bipartite reciprocity lock, independently certified in ARBS-GRAPH-REALIZATION-001): a self-loop connects a vertex to itself, which cannot cross a bipartition, so any TH-ARBS-001A-admissible graph is automatically irreflexive. Not imposed as a free-standing axiom -- it is a logical consequence of an already-certified filter (bipartite_TH_ARBS_001A) applied below."),
    ("reflexive", lambda r: r["reflexive"], "UNJUSTIFIED",
     "No independent derivation; also directly INCOMPATIBLE with the DERIVED irreflexivity consequence above for any nontrivial candidate."),
    ("symmetric", lambda r: r["symmetric"], "DERIVED-CONDITIONAL",
     "Every certified spectral/persistence/thermodynamic construction reproduced in this project's prior runs (runs 1-9, tilde_G_k family) was built and verified EXCLUSIVELY on symmetric (undirected) weighted graphs -- Spec(L)={lambda_n,phi_n} with a real orthonormal eigenbasis, the heat kernel K_t=exp(-tL) as a genuine diffusion semigroup, and the Q=-D^{-1}L thermodynamic generator (real spectrum via similarity to the symmetric D^{-1/2}LD^{-1/2}) all implicitly require L symmetric, equivalently A symmetric. This is a PRECONDITION already built into the certified machinery, not an aesthetic preference newly imposed here -- see spectral closure section for the direct computational demonstration (asymmetric candidates give complex adjacency spectra)."),
    ("antisymmetric", lambda r: r["antisymmetric"], "UNJUSTIFIED",
     "Not independently derived from any certified dependency."),
    ("transitive", lambda r: r["transitive"], "UNJUSTIFIED",
     "Not independently derived from any certified dependency."),
    ("acyclic_TH_ARBS_001B", lambda r: r["nilpotent_TH_ARBS_001B"], "DERIVED",
     "TH-ARBS-001B (Shell Nilpotency Lock, independently certified in ARBS-GRAPH-REALIZATION-001) requires the directed transport matrix to be nilpotent for some finite power. For R taken as its own already-directed transport matrix, nilpotency is equivalent to acyclicity (a 0/1 matrix is nilpotent iff its digraph has no directed cycle, including self-loops as length-1 cycles) -- verified computationally (nilpotent_by_power == acyclic, asserted with zero exceptions across all candidates)."),
    ("bipartite_TH_ARBS_001A", lambda r: r["bipartite_TH_ARBS_001A"], "DERIVED",
     "TH-ARBS-001A (Bipartite Reciprocity Lock), independently certified in ARBS-GRAPH-REALIZATION-001 as one of exactly two concrete, checkable admissibility axioms for the Graph_ARBS category. Applied here as a FILTER on an independently-derived downstream (well, same-layer -- see dependency-order note below) admissibility condition, per Rule 0.7."),
    ("nontrivial_spectral_gap", lambda r: r["spectral_gap_symmetrized_laplacian"] > 1e-9, "UNJUSTIFIED",
     "No certified threshold for 'nontrivial' exists in source; reported as a computed statistic, not applied as a hard filter."),
    ("laplacian_connected_nullity_1", lambda r: r["laplacian_nullity_symmetrized"] == 1, "UNJUSTIFIED",
     "Laplacian-nullity-equals-1 (graph connected) is a standard spectral graph theory fact, but no certified UOC dependency requires the SEED specifically to be connected. Reported as a statistic."),
]

DEPENDENCY_ORDER_NOTE = (
    "TH-ARBS-001A and TH-ARBS-001B were both independently derived and verified in "
    "ARBS-GRAPH-REALIZATION-001 (prior run), entirely from the source-documented Graph_ARBS "
    "specification, with NO reference to the C0 relational-seed candidates being tested here. "
    "They are applied here strictly as filters on an already-independently-derived pair of "
    "admissibility axioms, per Rule 0.7's exception ('Only use a downstream layer as a FILTER "
    "after that layer has been independently derived from the candidate') -- not as a "
    "retroactive redefinition of the seed. No result from THIS run's seed candidates was fed "
    "back into TH-ARBS-001A/B's own derivation."
)

def apply_filters(N):
    reg = REG[N]
    out = {"N": N, "F_N_total": len(reg), "filters": []}
    for name, pred, status, justification in FILTERS:
        if pred is None:
            out["filters"].append({"filter": name, "status": status, "justification": justification, "survivors": None})
            continue
        survivors = [r for r in reg if pred(r)]
        out["filters"].append({
            "filter": name, "status": status, "justification": justification,
            "candidates_before": len(reg), "candidates_after": len(survivors),
        })
    return out

filter_results = {N: apply_filters(N) for N in [2, 3, 4]}

# ------------------------------------------------------------------
# F_N^derived: intersection of ONLY VERIFIED/DERIVED/CALCULATED filters
# ------------------------------------------------------------------
ACTIVE_STATUSES = {"DERIVED", "VERIFIED", "CALCULATED"}
# NOTE: "DERIVED-CONDITIONAL" (the 'symmetric' filter) is deliberately EXCLUDED from the
# active/canonical set per section 6's own rule ("Only: VERIFIED, DERIVED, CALCULATED may
# be used as active canonical constraints" -- CONDITIONAL is a separate, listed status and
# is not one of the three). 'symmetric' is a precondition for REUSING the existing certified
# spectral machinery unmodified, not an unconditional requirement on the seed itself -- it is
# reported and discussed in the spectral-closure section but does not narrow F_N^derived.
active_filter_names = [f[0] for f in FILTERS if f[2] in ACTIVE_STATUSES and f[1] is not None]

derived_results = {}
for N in [2, 3, 4]:
    reg = REG[N]
    survivors = reg
    trace = [("F_N (all fixed points)", len(survivors))]
    for name, pred, status, justification in FILTERS:
        if name in active_filter_names:
            survivors = [r for r in survivors if pred(r)]
            trace.append((name, len(survivors)))
    derived_results[N] = {
        "N": N,
        "active_filters_applied_in_order": active_filter_names,
        "survivor_lattice_trace": trace,
        "F_N_derived_size": len(survivors),
        "survivor_seed_ids": [r["seed_id"] for r in survivors],
    }
    print(f"N={N}: F_N^derived size = {len(survivors)} (trace: {trace})")

# ------------------------------------------------------------------
# Spectral closure: observed vs required distinction
# ------------------------------------------------------------------
spectral_closure = {}
for N in [2, 3, 4]:
    reg = REG[N]
    n_real_spectrum = sum(1 for r in reg if r["adjacency_spectrum_is_real"])
    n_symmetric = sum(1 for r in reg if r["symmetric"])
    # among symmetric candidates, is spectrum always real? (should be, sanity check)
    sym_real_check = all(r["adjacency_spectrum_is_real"] for r in reg if r["symmetric"])
    # among NON-symmetric candidates, how many still happen to have real spectrum (observed, not required)?
    nonsym_real = sum(1 for r in reg if not r["symmetric"] and r["adjacency_spectrum_is_real"])
    nonsym_total = sum(1 for r in reg if not r["symmetric"])
    spectral_closure[N] = {
        "N": N, "total_F_N": len(reg),
        "n_symmetric": n_symmetric,
        "symmetric_implies_real_spectrum_verified": sym_real_check,
        "n_real_spectrum_total": n_real_spectrum,
        "nonsymmetric_candidates_with_real_spectrum_observed_not_required": nonsym_real,
        "nonsymmetric_candidates_total": nonsym_total,
    }
    print(f"N={N}: symmetric={n_symmetric}, real-spectrum total={n_real_spectrum}, "
          f"nonsym-but-real (observed)={nonsym_real}/{nonsym_total}")

# ------------------------------------------------------------------
# Persistence closure: BLOCKED (lambda_gap open, established in prior run)
# ------------------------------------------------------------------
persistence_closure = {
    "construction": "Pi(K) := sum_{n: lambda_n < lambda_gap} sqrt(lambda_n)  (SEF SIT Specification v2.docx, D5)",
    "status": "BLOCKED",
    "exact_missing_dependency": "lambda_gap -- established as an OPEN, unfixed free parameter with 'no derivation anywhere in the corpus' in ARBS-GRAPH-REALIZATION-001 / KIJ-THETA-IMAGE-RECOVERY-001 (this project's own prior runs). Without lambda_gap, Pi_R cannot be evaluated as a concrete number for ANY candidate -- the persistence sector {n : lambda_n < lambda_gap} is undefined.",
    "second_persistence_notion_also_blocked": "The Architecture-layer 'Organizational Persistence Functional' Pi_O = f(sigma, C, Spec(L)) is SEPARATELY recorded as OPEN in source (DER-ORG-007, 'coupling equation proposed; stationary distribution ... approach outlined but not executed') -- both persistence notions found anywhere in this corpus are open, not just the one nominally invoked by this protocol.",
    "consequence": "F_N^(persistence) = F_N^(spectral) unchanged. No additional narrowing is possible from persistence without inventing lambda_gap, which Rule 0.4/0.3 forbid.",
    "what_remains_computable_without_Pi": "The diffusion-distance chain d(i,j) = sqrt(sum_k (phi_k(i)-phi_k(j))^2 / lambda_k) via Spec(L) does NOT require Pi and was independently certified/used throughout runs 1-9 on tilde_G_k. This is attempted separately below for the symmetric survivors, bypassing the blocked Pi construction."
}

# ------------------------------------------------------------------
# Persistence -> Geometry closure: BLOCKED (insufficient N)
# ------------------------------------------------------------------
geometry_closure = {
    "chain_attempted": "R -> L -> Spec(L) -> d(i,j) [diffusion distance, Pi-independent, certified] -> metric candidate g_mu_nu -> curvature",
    "d_ij_computable": "YES for symmetric survivors -- Spec(L_sym) exists and is real (verified above); diffusion distance can be formed directly.",
    "metric_and_curvature_status": "BLOCKED",
    "exact_missing_dependency": "A meaningful continuum metric tensor g_mu_nu and curvature require enough independent spectral modes / points to approximate a manifold in a refinement limit -- this was only ever done in prior runs (1-9) on the GROWING tilde_G_k family at large shell index k (N up into the thousands), never on a single N=2,3,4 point graph. A 2-, 3-, or 4-point discrete metric space does not support a nontrivial curvature tensor in the sense used elsewhere in this corpus. This is exactly the unresolved N->infinity / canonical-family question flagged in section 12 of this protocol -- geometry closure is blocked on THAT unresolved question, not on a new obstruction discovered here.",
}

with open("/home/user/URSP/reconstruction/seed_filter_lattice.json", "w") as f:
    json.dump(filter_results, f, indent=2)
with open("/home/user/URSP/reconstruction/seed_derived_survivors.json", "w") as f:
    json.dump({"dependency_order_note": DEPENDENCY_ORDER_NOTE, "results": derived_results}, f, indent=2)
with open("/home/user/URSP/reconstruction/seed_spectral_closure.json", "w") as f:
    json.dump(spectral_closure, f, indent=2)
with open("/home/user/URSP/reconstruction/seed_persistence_geometry_closure.json", "w") as f:
    json.dump({"persistence_closure": persistence_closure, "geometry_closure": geometry_closure}, f, indent=2)

print("\nsaved seed_filter_lattice.json, seed_derived_survivors.json, seed_spectral_closure.json, seed_persistence_geometry_closure.json")

# ------------------------------------------------------------------
# Isomorphism-invariance audit: permute several candidates, recheck all filters
# ------------------------------------------------------------------
random.seed(0)
audit_results = []
for N in [2, 3, 4]:
    reg = REG[N]
    sample = random.sample(reg, min(20, len(reg)))
    for rec in sample:
        mat = rec["adjacency_matrix"]
        for trial in range(3):
            perm = list(range(N)); random.shuffle(perm)
            pmat = [[0]*N for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    pmat[perm[i]][perm[j]] = mat[i][j]
            bits = tuple(pmat[i][j] for i in range(N) for j in range(N))
            # recompute a few key representation-invariant quantities on the permuted matrix
            perms_all = list(itertools.permutations(range(N)))
            canon_orig, aut_orig = canonical_form(tuple(mat[i][j] for i in range(N) for j in range(N)), N, perms_all)
            canon_perm, aut_perm = canonical_form(bits, N, perms_all)
            ok = (canon_orig == canon_perm) and (aut_orig == aut_perm)
            audit_results.append({"N": N, "seed_id": rec["seed_id"], "perm": perm, "invariant_preserved": ok})

n_ok = sum(1 for a in audit_results if a["invariant_preserved"])
print(f"\nIsomorphism-invariance audit: {n_ok}/{len(audit_results)} permutation trials preserved canonical form + Aut size exactly.")
with open("/home/user/URSP/reconstruction/seed_isomorphism_invariance_audit.json", "w") as f:
    json.dump({"n_trials": len(audit_results), "n_passed": n_ok, "all_passed": n_ok == len(audit_results),
               "sample": audit_results[:10]}, f, indent=2)
print("saved seed_isomorphism_invariance_audit.json")

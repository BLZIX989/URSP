"""
Full sweep of the non-abelian commutant bridge (compiler/ncg_nonabelian_bridge.py)
over every seed in F_N^derived_v2, N=2,3,4,5, plus the negative controls
from OPEN-024B Section 14.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from compiler import kernel, ncg_bridge, enumerate_admissible_seeds
from compiler import ncg_nonabelian_bridge as nab
from run_bridge import get_n5_candidates

rng_global = np.random.default_rng(20260818)


def analyze_seed_full(mat, N, same_sign=True):
    p1 = ncg_bridge.build_phase1(mat, N)
    D_F = p1["D_F"]
    basis, block_dims, groups, eigvecs = nab.commutant_basis(D_F)
    nonabelian = nab.is_nonabelian(basis)
    max_irrep = nab.max_irrep_dimension(block_dims)

    p2 = ncg_bridge.build_phase2(p1, same_sign)
    J0 = p2["J0"]
    D_F_full = p2["D_F_full"]

    # generic complex test elements (linear combinations), not just elementary basis ops
    def random_combo():
        coeffs = rng_global.normal(size=len(basis)) + 1j * rng_global.normal(size=len(basis))
        return sum(c * b for c, b in zip(coeffs, basis))
    test_elems = basis + [random_combo() for _ in range(3)]

    oz_ok, oz_r = nab.test_order_zero_full_commutant(test_elems, J0, N)
    fo_ok, fo_r = nab.test_first_order_full_commutant(test_elems, D_F_full, J0, N)

    return {
        "block_dims": block_dims, "dim_A_seed": len(basis),
        "nonabelian": nonabelian, "max_irrep_dim": int(max_irrep),
        "order_zero_holds": oz_ok, "first_order_holds": fo_ok,
    }


def get_seeds(N):
    if N <= 4:
        return [s.adjacency_matrix for s in enumerate_admissible_seeds(N)]
    return get_n5_candidates()


all_results = {}
for N in [2, 3, 4, 5]:
    print(f"=== N={N} ===")
    mats = get_seeds(N)
    n_nonabelian = 0
    n_oz_pass_given_nonabelian = 0
    n_fo_pass_given_nonabelian = 0
    n_both_pass_given_nonabelian = 0
    n_oz_pass_given_abelian = 0
    n_fo_pass_given_abelian = 0
    max_irrep_hist = {}
    for mat in mats:
        r = analyze_seed_full(mat, N)
        max_irrep_hist[r["max_irrep_dim"]] = max_irrep_hist.get(r["max_irrep_dim"], 0) + 1
        if r["nonabelian"]:
            n_nonabelian += 1
            if r["order_zero_holds"]:
                n_oz_pass_given_nonabelian += 1
            if r["first_order_holds"]:
                n_fo_pass_given_nonabelian += 1
            if r["order_zero_holds"] and r["first_order_holds"]:
                n_both_pass_given_nonabelian += 1
        else:
            if r["order_zero_holds"]:
                n_oz_pass_given_abelian += 1
            if r["first_order_holds"]:
                n_fo_pass_given_abelian += 1
    result = {
        "N": N, "n_seeds": len(mats),
        "n_nonabelian_Comm_DF": n_nonabelian,
        "max_irrep_dim_histogram": max_irrep_hist,
        "given_nonabelian__order_zero_pass": n_oz_pass_given_nonabelian,
        "given_nonabelian__first_order_pass": n_fo_pass_given_nonabelian,
        "given_nonabelian__BOTH_pass": n_both_pass_given_nonabelian,
        "given_abelian__order_zero_pass": n_oz_pass_given_abelian,
        "given_abelian__first_order_pass": n_fo_pass_given_abelian,
    }
    all_results[N] = result
    print(json.dumps(result, indent=2))

# ------------------------------------------------------------------
# Controls (Section 14)
# ------------------------------------------------------------------
print("\n=== CONTROLS ===")
controls = {}

# Control A: remove seed relation (D_F=0)
N = 4
D_F_zero = np.zeros((N, N))
basis0, bd0, g0, ev0 = nab.commutant_basis(D_F_zero)
controls["A_remove_relation_DF_zero"] = {
    "nonabelian": nab.is_nonabelian(basis0), "block_dims": bd0,
    "note": "D_F=0 has one degenerate eigenspace of full dimension N -> Comm(D_F)=M_N(C), MAXIMALLY non-abelian but physically vacuous (D_F=0 means no seed relation at all)."
}

# Control E: maximal abelian algebra (already tested in ncg_bridge.py / ncg_asymmetric_bridge.py)
controls["E_maximal_abelian_reference"] = {"note": "See ncg_first_order_proofs.json: order-zero always passes, first-order always fails, for the maximal abelian algebra."}

# Control B/C/D: randomized variants -- test whether repeated D_F eigenvalues (hence non-abelian
# Comm(D_F)) still occur under randomization, to see whether it's the SPECIFIC seed topology or
# just "some sparse 0/1 matrix" that produces degeneracy.
def random_bipartite_mat(N, n_edges, rng):
    mat = [[0]*N for _ in range(N)]
    color = {i: i % 2 for i in range(N)}  # arbitrary fixed balanced-ish coloring for the control
    slots = [(i,j) for i in range(N) for j in range(N) if color[i]!=color[j]]
    rng.shuffle(slots)
    for (i,j) in slots[:n_edges]:
        mat[i][j] = 1
    return mat

rng = np.random.default_rng(123)
n_trials = 50
n_degenerate = 0
for _ in range(n_trials):
    mat = random_bipartite_mat(4, 3, rng)
    p1 = ncg_bridge.build_phase1(mat, 4)
    eigs = np.round(np.linalg.eigvalsh(p1["D_F"]), 6)
    uniq, counts = np.unique(eigs, return_counts=True)
    if counts.max() >= 2:
        n_degenerate += 1
controls["B_randomized_bipartite_same_N_and_edge_count"] = {
    "n_trials": n_trials, "n_degenerate_eigenvalue_found": n_degenerate,
    "note": "Tests whether eigenvalue degeneracy (hence non-abelian Comm(D_F)) is specific to F_N^derived_v2's Gamma-fixed, rigid seeds, or a generic feature of sparse bipartite 0/1 matrices at this size."
}

with open("/home/user/URSP/reconstruction/uoc_nonabelian_bridge_results.json", "w") as f:
    json.dump({"main_sweep": all_results, "controls": controls}, f, indent=2)
print("\nsaved uoc_nonabelian_bridge_results.json")
print(json.dumps(controls, indent=2))

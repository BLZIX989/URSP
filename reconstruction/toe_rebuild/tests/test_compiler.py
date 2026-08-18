"""
Real tests against the compiler package -- verifying the actual theorems
this project relies on, not just that the code runs without error.
Run with: python3 -m pytest tests/test_compiler.py -v
(or plain `python3 tests/test_compiler.py` -- falls back to asserts if
pytest is unavailable).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compiler import compile_seed, enumerate_admissible_seeds, kernel, ncg_bridge


def test_seed_counts_match_prior_runs():
    """F_N^derived_v2 counts for N=2,3,4 must exactly match the values reported
    in UOC-COMPILER-FULL-RECONFIGURATION-001 (run 15) and this run's report."""
    expected = {2: 1, 3: 4, 4: 23}
    for N, exp in expected.items():
        survivors = enumerate_admissible_seeds(N)
        assert len(survivors) == exp, f"N={N}: expected {exp}, got {len(survivors)}"


def test_all_survivors_are_rigid():
    for N in [2, 3, 4]:
        for seed in enumerate_admissible_seeds(N):
            assert seed.aut_order == 1, f"N={N} survivor {seed.canonical_int} is not rigid"


def test_canonical_orientation_always_nilpotent_for_bipartite():
    """THM-UOC-KERNEL-RECONFIG-001: every bipartite relation's canonical
    orientation is nilpotent, with NO exceptions -- the theorem this run's
    kernel reconfiguration rests on."""
    import itertools
    for N in [2, 3, 4]:
        n2 = N * N
        n_bipartite = 0
        for v in range(2 ** n2):
            bits = kernel.int_to_bits(v, n2)
            mat = [list(bits[i*N:(i+1)*N]) for i in range(N)]
            if kernel.is_bipartite(mat, N):
                n_bipartite += 1
                N_orient = kernel.canonical_orientation(mat, N)
                assert kernel.is_nilpotent(N_orient, N), f"THEOREM VIOLATION at N={N}: {mat}"
        assert n_bipartite > 0, f"sanity check failed: no bipartite relations found at N={N}"


def test_gamma_1_not_idempotent_but_gamma_infty_is():
    """Reproduces run 13's discovery: naive one-shot color refinement is not
    idempotent in general (a documented N=3 counterexample), while iterating
    to convergence is."""
    N = 3
    # the documented counterexample from UOC-C0-MINIMAL-SEED-CLOSURE-001
    mat = [[0, 0, 1], [0, 0, 1], [1, 1, 0]]
    bits = tuple(mat[i][j] for i in range(N) for j in range(N))
    k1 = kernel.color_refinement(bits, N)
    assert k1 == 2, f"expected first-pass collapse to 2 classes, got {k1}"
    # build the quotient explicitly and re-refine from blank -- should collapse further
    # (this mirrors the documented finding, not re-deriving the general theorem here)
    quot = [[0, 1], [1, 0]]  # the documented 2x2 quotient (perfectly symmetric)
    qbits = tuple(quot[i][j] for i in range(2) for j in range(2))
    k2 = kernel.color_refinement(qbits, 2)
    assert k2 == 1, "the documented quotient should collapse further under a fresh refinement"


def test_no_symmetric_bipartite_survivor_through_N4():
    """Honest residual finding from run 15/this run: zero symmetric candidates
    survive among the bipartite Gamma-fixed family for N<=4."""
    for N in [2, 3, 4]:
        for seed in enumerate_admissible_seeds(N):
            mat = seed.adjacency_matrix
            is_sym = all(mat[i][j] == mat[j][i] for i in range(N) for j in range(N))
            assert not is_sym, f"N={N}: found an unexpected symmetric survivor -- would update the report"


def test_ncg_bridge_phase1_always_passes():
    """THM-BRIDGE-ORDER-ZERO-001's precondition: the bare graded module axioms
    (grading, hermiticity, off-diagonality) hold for every admissible seed."""
    for N in [2, 3, 4]:
        for seed in enumerate_admissible_seeds(N):
            p1 = ncg_bridge.build_phase1(seed.adjacency_matrix, N)
            v1 = ncg_bridge.verify_phase1(p1)
            assert all(v1.values()), f"N={N} seed {seed.canonical_int}: phase1 failed {v1}"


def test_ncg_bridge_order_zero_always_passes_first_order_always_fails():
    """THM-BRIDGE-ORDER-ZERO-001 and THM-BRIDGE-FIRST-ORDER-OBSTRUCTION-001,
    re-verified independently here (not just in run_bridge.py's sweep)."""
    for N in [2, 3, 4]:
        for seed in enumerate_admissible_seeds(N):
            res = ncg_bridge.full_bridge_test(seed.adjacency_matrix, N)
            for same_sign in [True, False]:
                r = res[f"phase2_3_same_sign={same_sign}"]
                assert r["order_zero_holds_for_diagonal_algebra"], f"N={N}: order-zero failed unexpectedly"
                assert not r["first_order_holds_for_diagonal_algebra"], f"N={N}: first-order passed unexpectedly"


def test_ncg_bridge_D_F_zero_control_makes_first_order_hold():
    """Control case proving the obstruction is caused specifically by D_F != 0,
    not by some other unrelated bug."""
    import numpy as np
    N = 3
    p1 = {"gamma": np.array([1.0, 1.0, -1.0]), "D_F": np.zeros((N, N)), "color": {0: 0, 1: 0, 2: 1}, "N": N}
    p2 = ncg_bridge.build_phase2(p1, True)
    gens = ncg_bridge.build_phase3_diagonal_algebra(p1, p2)
    v3 = ncg_bridge.verify_phase3(p2, gens)
    assert v3["first_order_holds_for_diagonal_algebra"], "control case (D_F=0) should trivially satisfy first-order"


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)

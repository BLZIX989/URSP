"""
OPEN-024B: asymmetric-representation extension of ncg_bridge.py.

SEMANTIC-FUNCTOR-BRIDGE-001 proved that representing the algebra
IDENTICALLY on both P/A copies (pi_R = pi_L) forces first-order to
require D_F=0 -- a universal, structural obstruction, not a per-seed
accident. This module tests the predefined, declared-in-advance search
space of GENUINELY asymmetric pi_R candidates (Section 6 of OPEN-024B),
distinguishing SEED-DERIVED candidates (built from R's own structure)
from GENERIC candidates (representation-theoretic operations that don't
reference R at all), exactly as OPEN-024B Section 6 requires.

No Standard-Model content (hypercharges, generations, dim=32, gauge
groups) enters anywhere. The test algebra is the same generic maximal
abelian algebra as the previous run, now evaluated on GENERIC COMPLEX
diagonal elements (not only the real 0/1 one-hot basis) so that
"complex conjugate" is a genuinely distinct candidate from "identity"
(on purely real generators the two would coincide trivially).
"""
import numpy as np
from . import kernel, ncg_bridge


def build_asym_phase2(p1, same_sign_extension):
    """Same J_F/gamma_F/D_F doubling as ncg_bridge.build_phase2 -- reused
    verbatim, not redefined, since Phase 1/2's structural axioms (grading,
    Hermiticity, KO-class) were already proven general theorems and are
    unaffected by the choice of representation pi_R tested in Phase 3."""
    return ncg_bridge.build_phase2(p1, same_sign_extension)


# ------------------------------------------------------------------
# Predefined representation search space (declared BEFORE any testing,
# per OPEN-024B Section 6/13 -- no candidate added post hoc).
# ------------------------------------------------------------------
REPRESENTATION_CANDIDATES = [
    "identity",              # GENERIC -- the previous run's (failing) choice, kept as control
    "conjugate",              # GENERIC -- pi_R(a) = conj(pi_L(a)); the standard NCG antiparticle convention
    "orientation_reversed",   # SEED-DERIVED -- built from N_orient(R)^T instead of N_orient(R)
    "random_diagonal_perm",   # GENERIC, NEGATIVE CONTROL -- deterministic pseudorandom relabeling, seed-independent
]


def make_generators(N, n_test=6, rng=None):
    """Generic complex diagonal test elements of the maximal abelian algebra
    (not merely the real 0/1 one-hot basis) -- needed so 'conjugate' is
    distinguishable from 'identity'. Deterministic seed for reproducibility."""
    if rng is None:
        rng = np.random.default_rng(20260818)
    gens = []
    # one-hot real generators (basis, always included)
    for i in range(N):
        d = np.zeros(N, dtype=complex)
        d[i] = 1.0
        gens.append(d)
    # generic complex phase generators (to make conjugation nontrivial)
    for _ in range(n_test):
        phases = np.exp(1j * rng.uniform(0, 2 * np.pi, size=N))
        gens.append(phases)
    return gens


def pi_R_for_candidate(candidate, pi_L_diag, N, mat, rng=None):
    """pi_L_diag: length-N complex vector (the diagonal entries of pi_L(a))."""
    if candidate == "identity":
        return pi_L_diag.copy()
    if candidate == "conjugate":
        return np.conj(pi_L_diag)
    if candidate == "orientation_reversed":
        # SEED-DERIVED: relabel vertices by the seed's own reverse-orientation
        # induced permutation. For a bipartite graph with color classes X0,X1,
        # the reversed canonical orientation (N_orient(R)^T instead of N_orient(R))
        # doesn't itself define a vertex permutation -- so the seed-derived
        # asymmetry tested here is the color-swap involution when |X0|=|X1|
        # (the only seed-intrinsic involution available when Aut(R)=1, which
        # is always the case for F_N^derived_v2), applied to pi_L's DIAGONAL
        # (a relabeling of which entry sits where), and otherwise (unequal
        # class sizes) falls back to the identity candidate with a flag.
        color = kernel.bipartition(mat, N)
        X0 = [i for i in range(N) if color.get(i, 0) == 0]
        X1 = [i for i in range(N) if color.get(i, 0) == 1]
        if len(X0) != len(X1):
            return None  # not defined for this seed -- recorded, not silently substituted
        perm = {}
        for a, b in zip(sorted(X0), sorted(X1)):
            perm[a] = b
            perm[b] = a
        out = np.zeros(N, dtype=complex)
        for i in range(N):
            out[perm[i]] = pi_L_diag[i]
        return out
    if candidate == "random_diagonal_perm":
        if rng is None:
            rng = np.random.default_rng(999)
        perm = rng.permutation(N)
        return pi_L_diag[perm]
    raise ValueError(candidate)


def J_conjugate_op(J0, op):
    return J0 @ op @ np.linalg.inv(J0)


def test_candidate(mat, N, candidate, same_sign):
    p1 = ncg_bridge.build_phase1(mat, N)
    p2 = build_asym_phase2(p1, same_sign)
    J0, D_F_full = p2["J0"], p2["D_F_full"]
    gens = make_generators(N)
    rng = np.random.default_rng(42)

    order_zero_ok = True
    first_order_ok = True
    undefined = False
    for a_diag in gens:
        # Build full block-diagonal pi(a) = diag(pi_L(a), pi_R(a))
        pi_R_a = pi_R_for_candidate(candidate, a_diag, N, mat, rng)
        if pi_R_a is None:
            undefined = True
            break
        pi_a_full = np.diag(np.concatenate([a_diag, pi_R_a]))
        for b_diag in gens:
            pi_R_b = pi_R_for_candidate(candidate, b_diag, N, mat, rng)
            pi_b_full = np.diag(np.concatenate([b_diag, pi_R_b]))
            Jb = J_conjugate_op(J0, pi_b_full)
            oz = pi_a_full @ Jb - Jb @ pi_a_full
            if not np.allclose(oz, 0, atol=1e-8):
                order_zero_ok = False
            comm_Da = D_F_full @ pi_a_full - pi_a_full @ D_F_full
            fo = comm_Da @ Jb - Jb @ comm_Da
            if not np.allclose(fo, 0, atol=1e-8):
                first_order_ok = False
    if undefined:
        return {"status": "UNDEFINED_FOR_THIS_SEED"}
    return {
        "status": "TESTED",
        "order_zero_holds": order_zero_ok,
        "first_order_holds": first_order_ok,
    }


def full_asymmetric_sweep(mat, N):
    results = {}
    for candidate in REPRESENTATION_CANDIDATES:
        for same_sign in [True, False]:
            key = f"{candidate}__same_sign={same_sign}"
            results[key] = test_candidate(mat, N, candidate, same_sign)
    return results

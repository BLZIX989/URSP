"""
Semantic functor bridge: Track A (finite relational seed R, bipartite,
Gamma-fixed) -> Track B (finite noncommutative-geometry spectral triple
(A_F, H_F, D_F, J_F, gamma_F)).

Every axiom tested here is taken VERBATIM from the NCG workbook's own
formal definitions (source/UOC_NCG_First_Principles_Unified_ToE_Rebuild_
v2.25_KO0_Explicit_First_Order_Closure.xlsx, sheets 152-157), not
reinvented. No Standard-Model-specific representation content (quark/
lepton labels, hypercharges, 3 generations, dim=32) is assumed anywhere
in this construction -- only generic, non-target-conditioned candidate
algebras are tested, per the project's target-independence mandate.

Construction (Phase 1-3, see the accompanying closure report for the
full reasoning):

Phase 1 (graded module, no real structure):
    H_F^bare = C^N            (N = |X|, the seed's own vertex count)
    gamma_F  = +1 on color class 0, -1 on color class 1 (the seed's own
               TH-ARBS-001A bipartition -- already established, not new)
    D_F      = off-diagonal block built from N_orient(R) (the seed's own
               already-derived canonical transport orientation, run 15)
    Tests: gamma_F^2=1, {D_F,gamma_F}=0, D_F=D_F^dagger (DF-001/002,
    GR-001/003 in the source workbook -- there marked "DERIVED
    STRUCTURE", i.e. expected to hold by construction; verified here
    programmatically for every seed, not assumed).

Phase 2 (real structure via the standard particle+antiparticle doubling):
    H_F = H_F^bare (+) H_F^bare  (dimension 2N)
    J_F[v,w] = [conj(w), conj(v)]   (source sheet 171_V2_CALC_018_RIGHT_REP_J
               -- this is the STANDARD, always-available way to add a real
               structure to a triple that doesn't already have one, not
               invented for this bridge)
    gamma_F, D_F extended to the doubled space by the two natural
    conventions (same-sign and opposite-sign across the two copies);
    both are tested against the source's own KO-dimension sign table
    (152_V2_CALC_017_KO_DIM) to see which (if any) KO class is realized.

Phase 3 (order-zero / first-order, generic non-SM algebra):
    A_F candidate = the maximal abelian (diagonal) algebra C^N, acting
    identically on both P/A copies -- the SAME kind of minimal/generic
    candidate the source workbook itself uses for its own closed "2-point
    test model" (OZ-003, FO-002), not a Standard-Model-specific choice.
    Tests order-zero [pi(a), J pi(b) J^-1] = 0 and first-order
    [[D_F,pi(a)], J pi(b) J^-1] = 0 for all pairs of basis generators.
"""
import numpy as np
from . import kernel


def build_phase1(mat, N):
    """Bare graded module + Dirac operator from a bipartite seed R."""
    color = kernel.bipartition(mat, N)
    gamma = np.array([1.0 if color.get(i, 0) == 0 else -1.0 for i in range(N)])
    N_orient = np.array(kernel.canonical_orientation(mat, N), dtype=float)
    # D_F must be Hermitian and off-diagonal w.r.t. gamma: symmetrize the
    # directed canonical orientation into a genuine Hermitian block.
    D_F = N_orient + N_orient.T
    return {"gamma": gamma, "D_F": D_F, "color": color, "N": N}


def verify_phase1(p1):
    N = p1["N"]
    gamma, D_F = p1["gamma"], p1["D_F"]
    checks = {}
    checks["gamma_squared_is_identity"] = np.allclose(gamma ** 2, np.ones(N))
    anticomm = np.diag(gamma) @ D_F + D_F @ np.diag(gamma)
    checks["D_F_anticommutes_with_gamma"] = np.allclose(anticomm, 0)
    checks["D_F_is_hermitian"] = np.allclose(D_F, D_F.T)
    checks["D_F_is_offdiagonal_in_grading_basis"] = bool(
        np.allclose(D_F[np.ix_([i for i in range(N) if gamma[i] > 0],
                                [i for i in range(N) if gamma[i] > 0])], 0)
        and np.allclose(D_F[np.ix_([i for i in range(N) if gamma[i] < 0],
                                    [i for i in range(N) if gamma[i] < 0])], 0)
    )
    return checks


# KO-dimension sign table, taken verbatim from source sheet 152_V2_CALC_017_KO_DIM
KO_TABLE = [
    (0, 1, 1, 1), (2, -1, 1, -1), (4, -1, 1, 1), (6, 1, 1, -1),
    (8, 1, -1, 1), (10, -1, -1, -1), (12, -1, -1, 1), (14, 1, -1, -1),
]


def build_phase2(p1, same_sign_extension):
    """Double to (H_F^bare (+) H_F^bare) with the standard swap+conjugate J_F."""
    N = p1["N"]
    gamma, D_F = p1["gamma"], p1["D_F"]
    if same_sign_extension:
        gamma_full = np.concatenate([gamma, gamma])
    else:
        gamma_full = np.concatenate([gamma, -gamma])
    D_F_full = np.block([[D_F, np.zeros((N, N))], [np.zeros((N, N)), D_F]])
    # J_F: antilinear swap-and-conjugate. Represented as (linear part J0, conj flag).
    J0 = np.block([[np.zeros((N, N)), np.eye(N)], [np.eye(N), np.zeros((N, N))]])
    return {"gamma_full": gamma_full, "D_F_full": D_F_full, "J0": J0, "N": N}


def apply_J(J0, v):
    """J_F(v) = J0 @ conj(v) -- antilinear."""
    return J0 @ np.conj(v)


def verify_phase2(p2):
    N2 = 2 * p2["N"]
    J0 = p2["J0"]
    gamma_full, D_F_full = p2["gamma_full"], p2["D_F_full"]
    # J_F^2 acting on an arbitrary vector: J(J(v)) = J0 @ conj(J0 @ conj(v)) = J0 @ conj(J0) @ v
    J_squared_matrix = J0 @ np.conj(J0)
    eps = None
    if np.allclose(J_squared_matrix, np.eye(N2)):
        eps = 1
    elif np.allclose(J_squared_matrix, -np.eye(N2)):
        eps = -1
    # J D J^-1 relation: J(D(J(v))) should equal eps' * D(v) for all v (antilinear composition)
    # J(D(w)) = J0 @ conj(D_F_full @ w) = J0 @ conj(D_F_full) @ conj(w) [D_F_full real => conj(D)=D]
    JD = J0 @ D_F_full  # since D_F_full is real, conj(D_F_full)=D_F_full
    DJ_conjpart = D_F_full @ J0  # for comparison after accounting for antilinearity consistently
    # Because D_F_full is real and J0 is real, J_F D_F J_F^{-1} (as an antilinear conjugation of a
    # real operator) reduces, on this real representation, to checking J0 D_F_full == D_F_full J0
    # up to a sign eps'.
    eps_prime = None
    if np.allclose(J0 @ D_F_full, D_F_full @ J0):
        eps_prime = 1
    elif np.allclose(J0 @ D_F_full, -(D_F_full @ J0)):
        eps_prime = -1
    eps_dprime = None
    Gamma_full = np.diag(gamma_full)
    if np.allclose(J0 @ Gamma_full, Gamma_full @ J0):
        eps_dprime = 1
    elif np.allclose(J0 @ Gamma_full, -(Gamma_full @ J0)):
        eps_dprime = -1
    matched_KO = [ko for ko, e, ep, edp in KO_TABLE if e == eps and ep == eps_prime and edp == eps_dprime]
    return {
        "J_squared_sign_eps": eps, "JD_sign_eps_prime": eps_prime, "Jgamma_sign_eps_dprime": eps_dprime,
        "matched_KO_dimensions_mod_8": matched_KO,
    }


def build_phase3_diagonal_algebra(p1, p2):
    """Generic (non-SM) maximal abelian algebra: independent phase per vertex,
    represented identically on both P/A copies."""
    N = p1["N"]
    generators = []  # one generator per vertex: diag with a single nonzero entry
    for i in range(N):
        d = np.zeros(N)
        d[i] = 1.0
        pi_a = np.diag(np.concatenate([d, d]))  # acts identically on both copies
        generators.append(pi_a)
    return generators


def verify_phase3(p2, generators):
    N2 = 2 * p2["N"]
    J0, D_F_full = p2["J0"], p2["D_F_full"]

    def J_conjugate(op):
        # J pi(b) J^{-1} acting on a real representation with antilinear J = J0 . conj:
        # for a REAL matrix op (our generators are real & diagonal), J op J^{-1} = J0 @ op @ J0^{-1}
        # (conjugation of a real matrix is itself; J0 is a real involutive permutation here).
        return J0 @ op @ np.linalg.inv(J0)

    order_zero_ok = True
    first_order_ok = True
    for a in generators:
        Ja = J_conjugate(a)
        for b in generators:
            Jb = J_conjugate(b)
            oz = a @ Jb - Jb @ a
            if not np.allclose(oz, 0, atol=1e-9):
                order_zero_ok = False
            comm_Da = D_F_full @ a - a @ D_F_full
            fo = comm_Da @ Jb - Jb @ comm_Da
            if not np.allclose(fo, 0, atol=1e-9):
                first_order_ok = False
    return {"order_zero_holds_for_diagonal_algebra": order_zero_ok,
            "first_order_holds_for_diagonal_algebra": first_order_ok}


def full_bridge_test(mat, N):
    p1 = build_phase1(mat, N)
    v1 = verify_phase1(p1)
    results = {"phase1": v1}
    for same_sign in [True, False]:
        p2 = build_phase2(p1, same_sign)
        v2 = verify_phase2(p2)
        gens = build_phase3_diagonal_algebra(p1, p2)
        v3 = verify_phase3(p2, gens)
        results[f"phase2_3_same_sign={same_sign}"] = {**v2, **v3}
    return results

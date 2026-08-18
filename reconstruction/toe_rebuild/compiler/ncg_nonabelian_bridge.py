"""
OPEN-024B (non-abelian): A_seed := Comm(D_F), the commutant of the
seed's own (already-derived) finite Dirac operator.

Motivation (Section 4B, "commutant / double-commutant"): since D_F is
Hermitian (proven, run 17/18), it is unitarily diagonalizable with an
orthogonal eigenspace decomposition H_F^bare = (+)_lambda E_lambda.
Its commutant is EXACTLY (+)_lambda End(E_lambda) -- external standard
linear algebra (the centralizer of a normal matrix is the direct sum
of full endomorphism algebras of its eigenspaces), applied to a
seed-derived operator, not assumed or imported. This is the smallest
non-arbitrary "maximal" candidate available from the seed's own
Hermitian structure: no free parameter, no target algebra chosen in
advance, and it is non-abelian exactly when D_F has a repeated
eigenvalue -- a directly checkable seed property, not a matter of
selection.

Elements of Comm(D_F) commute with D_F by DEFINITION, so
[D_F, pi(a)] = 0 identically for the "identical copy" representation
-- meaning first-order is expected to hold automatically for this
algebra where it failed for the maximal abelian algebra. Order-zero is
NOT automatic and is tested honestly, not assumed.
"""
import numpy as np
from . import kernel, ncg_bridge


def eigenspace_decomposition(D_F, tol=1e-6):
    """Returns (eigenvalues, eigenvectors, groups) where groups is a list
    of index-lists, one per distinct eigenvalue (multiplicity >= 1)."""
    eigvals, eigvecs = np.linalg.eigh(D_F)  # ascending, orthonormal columns
    groups = []
    used = [False] * len(eigvals)
    for i in range(len(eigvals)):
        if used[i]:
            continue
        grp = [i]
        used[i] = True
        for j in range(i + 1, len(eigvals)):
            if not used[j] and abs(eigvals[j] - eigvals[i]) < tol:
                grp.append(j)
                used[j] = True
        groups.append(grp)
    return eigvals, eigvecs, groups


def commutant_basis(D_F, tol=1e-6):
    """Basis of Comm(D_F) = (+)_lambda End(E_lambda), expressed in the
    ORIGINAL (seed) basis, not the eigenbasis -- so it can act directly
    on H_F alongside D_F, gamma_F, N_orient etc."""
    N = D_F.shape[0]
    eigvals, eigvecs, groups = eigenspace_decomposition(D_F, tol)
    basis = []
    block_dims = [len(g) for g in groups]
    for grp in groups:
        m = len(grp)
        V = eigvecs[:, grp]  # N x m, orthonormal columns spanning E_lambda
        for p in range(m):
            for q in range(m):
                E_pq_eigbasis = np.zeros((m, m), dtype=complex)
                E_pq_eigbasis[p, q] = 1.0
                op = V @ E_pq_eigbasis @ V.conj().T  # N x N, in original basis
                basis.append(op)
    return basis, block_dims, groups, eigvecs


def is_nonabelian(basis, tol=1e-8):
    for a in basis:
        for b in basis:
            if not np.allclose(a @ b - b @ a, 0, atol=tol):
                return True
    return False


def max_irrep_dimension(block_dims):
    return max(block_dims) if block_dims else 1


def test_order_zero_full_commutant(basis, J0, N, tol=1e-8):
    """Order-zero for pi(a)=diag(a,a) (identical copies), a ranging over
    the FULL commutant basis, tested pairwise against J-conjugates."""
    ok = True
    worst = 0.0
    for a in basis:
        pi_a = np.block([[a, np.zeros((N, N))], [np.zeros((N, N)), a]])
        for b in basis:
            pi_b = np.block([[b, np.zeros((N, N))], [np.zeros((N, N)), b]])
            Jb = J0 @ pi_b @ np.linalg.inv(J0)
            comm = pi_a @ Jb - Jb @ pi_a
            resid = np.max(np.abs(comm))
            worst = max(worst, resid)
            if resid > tol:
                ok = False
    return ok, worst


def test_first_order_full_commutant(basis, D_F_full, J0, N, tol=1e-8):
    ok = True
    worst = 0.0
    for a in basis:
        pi_a = np.block([[a, np.zeros((N, N))], [np.zeros((N, N)), a]])
        comm_Da = D_F_full @ pi_a - pi_a @ D_F_full
        for b in basis:
            pi_b = np.block([[b, np.zeros((N, N))], [np.zeros((N, N)), b]])
            Jb = J0 @ pi_b @ np.linalg.inv(J0)
            fo = comm_Da @ Jb - Jb @ comm_Da
            resid = np.max(np.abs(fo))
            worst = max(worst, resid)
            if resid > tol:
                ok = False
    return ok, worst


def real_subalgebra_basis(basis, tol=1e-8):
    """The natural restriction to test if the full commutant fails
    order-zero: the REAL subalgebra {a in Comm(D_F) : conj(a) = a} --
    canonical (not arbitrary), since order-zero's failure mode is
    exactly a not commuting with conj(b); restricting to real elements
    makes conj(b)=b, so order-zero reduces to the algebra being abelian
    on its real part. Constructed by symmetrizing the given basis, then
    reduced to a linearly independent spanning set via QR."""
    candidates = []
    for op in basis:
        sym = (op + op.conj()) / 2.0
        if np.max(np.abs(sym)) > 1e-10:
            candidates.append(sym)
    if not candidates:
        return []
    flat = np.array([op.flatten() for op in candidates]).T  # (N*N) x n_candidates
    q, r = np.linalg.qr(flat)
    rank = int(np.sum(np.abs(np.diag(r)) > tol))
    # greedily pick independent columns among candidates
    independent = []
    accum = None
    for op in candidates:
        v = op.flatten().reshape(-1, 1)
        test = v if accum is None else np.hstack([accum, v])
        if np.linalg.matrix_rank(test, tol=tol) > (0 if accum is None else np.linalg.matrix_rank(accum, tol=tol)):
            independent.append(op)
            accum = test
        if len(independent) >= rank:
            break
    return independent


def analyze_seed(mat, N, same_sign=True):
    p1 = ncg_bridge.build_phase1(mat, N)
    D_F = p1["D_F"]
    basis, block_dims, groups, eigvecs = commutant_basis(D_F)
    nonabelian = is_nonabelian(basis)
    max_irrep = max_irrep_dimension(block_dims)

    p2 = ncg_bridge.build_phase2(p1, same_sign)
    J0 = p2["J0"]
    D_F_full = p2["D_F_full"]

    oz_ok, oz_resid = test_order_zero_full_commutant(basis, J0, N)
    fo_ok, fo_resid = test_first_order_full_commutant(basis, D_F_full, J0, N)

    return {
        "N": N, "block_dims": block_dims, "dim_A_seed": len(basis),
        "nonabelian": nonabelian, "max_irrep_dim": max_irrep,
        "order_zero_holds": oz_ok, "order_zero_worst_residual": float(oz_resid),
        "first_order_holds": fo_ok, "first_order_worst_residual": float(fo_resid),
    }

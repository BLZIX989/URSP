"""
C-004D: independent verification of the thermodynamic generator reconciliation.

Computes, for G0-G4, and verifies numerically:
    L = D - A                          (certified spectral Laplacian)
    Q  = -D^{-1} L                     (candidate CTRW forward generator)
    Q* = Q^T = -L D^{-1}               (its adjoint; claimed = ScrL*_therm)
    L_norm = D^{-1/2} L D^{-1/2}       (symmetric normalized Laplacian)
    P_uniform = (1/N) * 1
    P_degree  = d / (2|E|)

Verified identities:
    L 1 = 0                              -> -L has uniform stationary state
    Q* d = 0                             -> Q* has degree-weighted stationary state
    L_norm = D^{1/2} (-Q) D^{-1/2}        -> similarity, so Spec(-Q) = Spec(L_norm)
    Spec(L) != Spec(L_norm) for irregular graphs (numerically)

No checkpoint value, no 32, no downstream target enters this file.
"""
import numpy as np
import json
from build_arbs import analyze

results = {}

for n in range(5):
    key = f"G{n}"
    r = analyze(n)
    A, L, N = r["A"], r["L"], r["N"]
    d = A.sum(axis=1)
    D = np.diag(d)
    E = r["E"]

    regular = bool(np.allclose(d, d[0]))
    unique_degrees, counts = np.unique(d.astype(int), return_counts=True)

    Dinv = np.diag(1.0 / d)
    Dinv_sqrt = np.diag(1.0 / np.sqrt(d))
    Dsqrt = np.diag(np.sqrt(d))

    Q = -Dinv @ L                     # -D^{-1}L
    Qstar = Q.T                       # = -L D^{-1}
    Qstar_direct = -L @ Dinv
    assert np.allclose(Qstar, Qstar_direct, atol=1e-10)

    L_norm = Dinv_sqrt @ L @ Dinv_sqrt

    P_uniform = np.ones(N) / N
    P_degree = d / (2 * E)

    # verify L @ 1 = 0
    L_ones_norm = float(np.linalg.norm(L @ np.ones(N)))
    # verify Q* @ d = 0  (equivalently Q* @ P_degree = 0)
    Qstar_d_norm = float(np.linalg.norm(Qstar @ d))
    Qstar_Pdeg_norm = float(np.linalg.norm(Qstar @ P_degree))
    # verify -L @ P_uniform = 0
    negL_Puniform_norm = float(np.linalg.norm(-L @ P_uniform))

    # similarity check: L_norm ?= Dsqrt @ (-Q) @ Dinv_sqrt
    candidate_similarity = Dsqrt @ (-Q) @ Dinv_sqrt
    similarity_holds = bool(np.allclose(L_norm, candidate_similarity, atol=1e-8))

    # direct matrix-equality tests (Frobenius norm), not just eigenvalues
    frob_Ltherm_plus_L = float(np.linalg.norm(Q - (-L), ord="fro"))          # ||Q - (-L)||_F
    frob_Qstar_plus_L = float(np.linalg.norm(Qstar - (-L), ord="fro"))

    # spectra
    eig_L = np.sort(np.linalg.eigvalsh(L))
    eig_Lnorm = np.sort(np.linalg.eigvalsh(L_norm))
    eig_negQ = np.sort(np.real(np.linalg.eigvals(-Q)))  # -Q is similar to symmetric L_norm -> real eigenvalues expected

    eig_negQ_matches_Lnorm = bool(np.allclose(eig_negQ, eig_Lnorm, atol=1e-6))

    lam1_L = float(eig_L[eig_L > 1e-8][0])
    lam1_Lnorm = float(eig_Lnorm[eig_Lnorm > 1e-8][0])
    lammax_L = float(eig_L.max())
    lammax_Lnorm = float(eig_Lnorm.max())

    l1_l2_dist_uniform_degree = float(np.linalg.norm(P_uniform - P_degree, ord=1))
    l2_dist_uniform_degree = float(np.linalg.norm(P_uniform - P_degree, ord=2))

    results[key] = {
        "N": N, "E": E,
        "regular": regular,
        "unique_degrees": unique_degrees.tolist(),
        "degree_multiplicities": counts.tolist(),
        "L_ones_norm_(should_be_0)": L_ones_norm,
        "Qstar_times_d_norm_(should_be_0)": Qstar_d_norm,
        "Qstar_times_Pdegree_norm_(should_be_0)": Qstar_Pdeg_norm,
        "negL_times_Puniform_norm_(should_be_0)": negL_Puniform_norm,
        "similarity_L_norm_eq_Dsqrt_negQ_Dinvsqrt": similarity_holds,
        "frobenius_||Q-(-L)||_F": frob_Ltherm_plus_L,
        "frobenius_||Qstar-(-L)||_F": frob_Qstar_plus_L,
        "L_therm_equals_negL_(Frobenius<1e-8)": frob_Ltherm_plus_L < 1e-8,
        "Qstar_equals_negL_(Frobenius<1e-8)": frob_Qstar_plus_L < 1e-8,
        "eig_negQ_matches_eig_Lnorm": eig_negQ_matches_Lnorm,
        "lambda1_L": lam1_L,
        "lambda1_Lnorm": lam1_Lnorm,
        "lambda1_ratio_L_over_Lnorm": lam1_L / lam1_Lnorm,
        "lambdamax_L": lammax_L,
        "lambdamax_Lnorm": lammax_Lnorm,
        "spec_L_equals_spec_Lnorm": bool(np.allclose(eig_L, eig_Lnorm, atol=1e-6)),
        "P_uniform_minus_Pdegree_L1": l1_l2_dist_uniform_degree,
        "P_uniform_minus_Pdegree_L2": l2_dist_uniform_degree,
        "P_uniform_equals_Pdegree": bool(np.allclose(P_uniform, P_degree, atol=1e-10)),
    }

    # save matrices
    for name, M in [("L", L), ("D", D), ("Lnorm", L_norm), ("Q_Ltherm", Q), ("Qstar_LthermStar", Qstar)]:
        np.save(f"/home/user/URSP/reconstruction/generator/{key}_{name}.npy", M)
    np.save(f"/home/user/URSP/reconstruction/generator/{key}_P_uniform.npy", P_uniform)
    np.save(f"/home/user/URSP/reconstruction/generator/{key}_P_degree.npy", P_degree)
    np.savetxt(f"/home/user/URSP/reconstruction/generator/{key}_eig_L.csv", eig_L, delimiter=",")
    np.savetxt(f"/home/user/URSP/reconstruction/generator/{key}_eig_Lnorm.csv", eig_Lnorm, delimiter=",")

    print(f"--- {key} --- N={N} E={E} regular={regular} degrees={unique_degrees.tolist()}")
    for k2, v2 in results[key].items():
        if k2 not in ("unique_degrees", "degree_multiplicities"):
            print(f"    {k2}: {v2}")

with open("/home/user/URSP/reconstruction/c004d_generator_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved c004d_generator_results.json")

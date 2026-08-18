"""
Full downstream re-execution now that complete ARBS spectra exist (produced by
build_arbs.py). Recomputes t_H, lambda_c, delta_spec, N_H(G_k) independently
from the complete spectra (not from the v1.0 checkpoint scalars), and compares
against those checkpoints. Also evaluates rank(P_boundary) for G3's isolated
gap and the OPEN-020E.2 Pi_0 status given the source definitions recovered
from the corpus search (delta_spec = lambda_1(L); sigma = entropy production,
dynamically defined via H-theorem, not reduced to a static per-graph scalar
anywhere in the source material).
"""
import numpy as np
import json
from build_arbs import analyze

CHECKPOINT_TH = {
    "G0": 0.173286795140, "G1": 0.137578446530, "G2": 0.079911417241,
    "G3": 0.043225367441, "G4": 0.022564403969,
}
CHECKPOINT_LC = {
    "G0": 5.770780163555398, "G1": 7.268580400651221, "G2": 12.513856399069492,
    "G3": 23.134563317823480, "G4": 44.317589836356648,
}


def p_A(t, lam_nonzero):
    return float(np.mean(np.exp(-2.0 * t * lam_nonzero)))


def solve_tH(lam_nonzero, lo=1e-6, hi=100.0, tol=1e-15, maxit=200):
    # p_A is strictly decreasing in t from ~1 to 0
    flo = p_A(lo, lam_nonzero) - 0.5
    fhi = p_A(hi, lam_nonzero) - 0.5
    assert flo > 0 and fhi < 0, (flo, fhi)
    for _ in range(maxit):
        mid = 0.5 * (lo + hi)
        fmid = p_A(mid, lam_nonzero) - 0.5
        if abs(fmid) < tol:
            return mid
        if fmid > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


results = {}
for n in range(5):
    key = f"G{n}"
    r = analyze(n)
    lam = r["laplacian_eigs_ascending"]
    lam_nonzero = lam[lam > 1e-8]

    tH_calc = solve_tH(lam_nonzero)
    lc_calc = 1.0 / tH_calc
    delta_spec_calc = float(lam_nonzero[0])  # lambda_1(L), first nonzero eigenvalue

    N_H = int(np.sum(lam >= lc_calc - 1e-9))  # rank(P_H) = # eigenvalues >= lambda_c
    lam_max = float(lam.max())

    results[key] = {
        "N": r["N"], "E": r["E"],
        "t_H_calculated": tH_calc,
        "t_H_checkpoint": CHECKPOINT_TH[key],
        "t_H_abs_diff": abs(tH_calc - CHECKPOINT_TH[key]),
        "lambda_c_calculated": lc_calc,
        "lambda_c_checkpoint": CHECKPOINT_LC[key],
        "lambda_c_abs_diff": abs(lc_calc - CHECKPOINT_LC[key]),
        "delta_spec_lambda1": delta_spec_calc,
        "lambda_max": lam_max,
        "N_H_rank_P_H": N_H,
        "num_nonzero_laplacian_eigs": int(len(lam_nonzero)),
        "kernel_dim": r["kernel_dim"],
    }
    print(f"{key}: N={r['N']} E={r['E']}  t_H_calc={tH_calc:.12f} (checkpoint {CHECKPOINT_TH[key]:.12f}, "
          f"diff={abs(tH_calc-CHECKPOINT_TH[key]):.3e})  "
          f"lambda_c_calc={lc_calc:.12f} (checkpoint {CHECKPOINT_LC[key]:.12f})  "
          f"delta_spec={delta_spec_calc:.6f}  lambda_max={lam_max:.6f}  N_H={N_H}")

# G3 boundary rank tests -- use the NONZERO Laplacian spectrum, index-matched
# to the nonzero Dirac singular values (lambda_j = sigma_j^2, j=1..r), exactly
# as the checkpoint sheet's sigma16/sigma17 -> lambda16/lambda17 relation uses.
g3 = analyze(3)
lam3_full = g3["laplacian_eigs_ascending"]
lam3 = lam3_full[lam3_full > 1e-8]
lam16, lam17 = lam3[15], lam3[16]
rank_P_boundary_laplacian = int(np.sum((lam3 >= lam16) & (lam3 < lam17)))

pos3 = g3["dirac_positive_ascending"]
sigma16, sigma17 = pos3[15], pos3[16]
# rank of projector onto Dirac eigenvalues with |eigenvalue| <= sigma16 (nonzero pairs only)
rank_dirac_32 = int(np.sum(pos3 <= sigma16 + 1e-9)) * 2

boundary_report = {
    "G3_lambda16": float(lam16), "G3_lambda17": float(lam17),
    "rank_P_boundary_1_[lambda16,lambda17)_on_Laplacian": rank_P_boundary_laplacian,
    "G3_sigma16": float(sigma16), "G3_sigma17": float(sigma17),
    "rank_of_first_16_nonzero_Dirac_pairs_(+-sigma_1..sigma_16)": rank_dirac_32,
    "interpretation": ("The Laplacian-side boundary interval [lambda16,lambda17) contains exactly "
                        "1 eigenvalue by construction of a half-open interval between two adjacent "
                        "sorted eigenvalues. The '32-state' language corresponds instead to the "
                        "projector onto the first 16 nonzero +-sigma Dirac pairs (32 states total), "
                        "which is well-defined and isolated because sigma_16 < sigma_17 with a "
                        "nonzero gap -- but WHY index 16 specifically is the physically selected cutoff "
                        "is a separate, still-unresolved question (no target-independent selector in "
                        "the source material picks out k=16)."),
}
print("\nG3 boundary report:", json.dumps(boundary_report, indent=2))

out = {"per_shell": results, "G3_boundary": boundary_report}
with open("/home/user/URSP/reconstruction/full_analysis_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nSaved full_analysis_results.json")

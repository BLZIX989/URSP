"""
C-004H: ARBS continuum compatibility recovery. Tests the CERTIFIED
diffusion-distance / effective-resistance metric (DER-GEO-005, ENG-011,
cross-referenced dozens of times across the corpus as 'Spec(L) -> diffusion
distance -> metric') against the source's Diameter Stability and Induced
Metric Invariance conditions -- as an alternative to the (assumed, not
source-labeled-canonical) unit-edge hop metric tested in C-004G, which
failed both.
"""
import numpy as np
import json
from arbs_light import analyze_light

N_SHELLS = 9  # G0..G8


def diffusion_matrix(L):
    evals, evecs = np.linalg.eigh(L)
    nz = evals > 1e-8
    lam = evals[nz]
    phi = evecs[:, nz]
    scaled = phi / np.sqrt(lam)
    sq = np.sum(scaled ** 2, axis=1)
    Gm = scaled @ scaled.T
    D2 = np.maximum(sq[:, None] + sq[None, :] - 2 * Gm, 0)
    return np.sqrt(D2), lam


def resistance_matrix(L):
    Lp = np.linalg.pinv(L)
    d = np.diag(Lp)
    R = np.maximum(d[:, None] + d[None, :] - 2 * Lp, 0)
    return R


shells = {n: analyze_light(n) for n in range(N_SHELLS)}

# ---- diameter trend, diffusion metric ----
diam_results = {}
for n, r in shells.items():
    D, lam = diffusion_matrix(r["L"])
    R = resistance_matrix(r["L"])
    diam_results[f"G{n}"] = {
        "N": r["N"],
        "diffusion_diam": float(D.max()),
        "resistance_diam": float(R.max()),
        "sqrt_resistance_diam": float(np.sqrt(R.max())),
        "identity_check_max|d^2-Reff|": float(np.max(np.abs(D ** 2 - R))),
        "mean_pairwise_diffusion_dist": float(D[np.triu_indices(r["N"], 1)].mean()),
        "lambda_1": float(lam[0]),
    }

print("=== Diameter trend (diffusion / resistance metric) ===")
for k, v in diam_results.items():
    print(f"{k}: N={v['N']} diffusion_diam={v['diffusion_diam']:.10f} "
          f"identity_residual={v['identity_check_max|d^2-Reff|']:.2e}")

# ---- induced metric invariance under inclusion rho_k ----
invariance_results = {}
prev = None
for n in range(N_SHELLS - 1):
    rk, rk1 = shells[n], shells[n + 1]
    Dk, _ = diffusion_matrix(rk["L"])
    Dk1, _ = diffusion_matrix(rk1["L"])
    Nk = rk["N"]
    sub = Dk1[:Nk, :Nk]
    diff = np.abs(sub - Dk)
    m = float(diff.max())
    ratio = (prev / m) if (prev is not None and m > 0) else None
    invariance_results[f"G{n}_to_G{n+1}"] = {
        "max_|d_{k+1}(vi,vj)-d_k(vi,vj)|_over_old_pairs": m,
        "mean_violation": float(diff.mean()),
        "ratio_prev_over_curr": ratio,
    }
    prev = m

print("\n=== Induced metric invariance violation trend ===")
for k, v in invariance_results.items():
    print(f"{k}: max_violation={v['max_|d_{k+1}(vi,vj)-d_k(vi,vj)|_over_old_pairs']:.8f} "
          f"ratio={v['ratio_prev_over_curr']}")

with open("/home/user/URSP/reconstruction/c004h_diameter.json", "w") as f:
    json.dump(diam_results, f, indent=2)
with open("/home/user/URSP/reconstruction/c004h_metric_invariance.json", "w") as f:
    json.dump(invariance_results, f, indent=2)

print("\nSaved c004h_diameter.json, c004h_metric_invariance.json")

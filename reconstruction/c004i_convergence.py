"""
C-004I: exhaustive metric-measure convergence test for ARBS under the
source-certified diffusion-distance / effective-resistance metric.
Produces all required registries/CSVs.
"""
import numpy as np
import ot
import json
import csv
from arbs_light import analyze_light

N_SHELLS = 11  # G0..G10


def diffusion_matrix(L):
    evals, evecs = np.linalg.eigh(L)
    nz = evals > 1e-8
    lam = evals[nz]
    phi = evecs[:, nz]
    scaled = phi / np.sqrt(lam)
    sq = np.sum(scaled ** 2, axis=1)
    Gm = scaled @ scaled.T
    D2 = np.maximum(sq[:, None] + sq[None, :] - 2 * Gm, 0)
    return np.sqrt(D2), lam, phi


def resistance_matrix(L):
    Lp = np.linalg.pinv(L)
    d = np.diag(Lp)
    return np.maximum(d[:, None] + d[None, :] - 2 * Lp, 0)


shells = {n: analyze_light(n) for n in range(N_SHELLS)}

# ---- C-004I.1: analytic identity check d^2 = R_eff ----
identity_check = {}
for n in range(9):
    r = shells[n]
    D, lam, phi = diffusion_matrix(r["L"])
    R = resistance_matrix(r["L"])
    identity_check[f"G{n}"] = float(np.max(np.abs(D ** 2 - R)))

# ---- C-004I.2: vertex-class (equitable partition) symmetry check ----
class_symmetry = {}
for n in range(6):
    r = shells[n]
    D, _, _ = diffusion_matrix(r["L"])
    classes = []
    for k, (Loff, Lsz, Roff, Rsz) in enumerate(r["shells"]):
        classes.append(list(range(Loff, Loff + Lsz)))
        classes.append(list(range(Roff, Roff + Rsz)))
    maxstd = 0.0
    for ia in classes:
        for ib in classes:
            sub = D[np.ix_(ia, ib)]
            if ia is ib or ia == ib:
                if len(ia) > 1:
                    vals = sub[~np.eye(len(ia), dtype=bool)]
                    maxstd = max(maxstd, float(vals.std()))
            else:
                maxstd = max(maxstd, float(sub.std()))
    class_symmetry[f"G{n}"] = maxstd

# ---- C-004I.3/4: diameter + metric invariance (epsilon_k), diffusion metric ----
diam_data = {}
for n in range(N_SHELLS):
    r = shells[n]
    D, lam, _ = diffusion_matrix(r["L"])
    diam_data[f"G{n}"] = {"N": r["N"], "diam": float(D.max()), "lambda1": float(lam[0])}

eps_abs = {}
eps_sq = {}
for n in range(N_SHELLS - 1):
    rk, rk1 = shells[n], shells[n + 1]
    Dk, _, _ = diffusion_matrix(rk["L"])
    Dk1, _, _ = diffusion_matrix(rk1["L"])
    Nk = rk["N"]
    sub = Dk1[:Nk, :Nk]
    diff = np.abs(sub - Dk)
    diffsq = np.abs(sub ** 2 - Dk ** 2)
    eps_abs[f"G{n}_to_G{n+1}"] = float(diff.max())
    eps_sq[f"G{n}_to_G{n+1}"] = float(diffsq.max())

eps_vals = list(eps_abs.values())
eps_ratios = [eps_vals[i] / eps_vals[i + 1] for i in range(len(eps_vals) - 1) if eps_vals[i + 1] > 0]

# ---- C-004I.5: measure defect, TV/L1/L2 (metric-independent, carried structure, recomputed) ----
measure_defect = {}
for n in range(N_SHELLS - 1):
    rk, rk1 = shells[n], shells[n + 1]
    Nk, Nk1 = rk["N"], rk1["N"]
    Ek, Ek1 = rk["E"], rk1["E"]
    pik = rk["d"] / (2 * Ek)
    pik1 = rk1["d"] / (2 * Ek1)
    push = np.zeros(Nk1)
    push[:Nk] = pik
    diff = push - pik1
    tv = 0.5 * float(np.sum(np.abs(diff)))
    l1 = float(np.linalg.norm(diff, ord=1))
    l2 = float(np.linalg.norm(diff, ord=2))
    measure_defect[f"G{n}_to_G{n+1}"] = {"TV": tv, "L1": l1, "L2": l2}

# ---- C-004I.7: Wasserstein-1 convergence under diffusion ground metric ----
wasserstein = {}
for n in range(N_SHELLS - 1):
    rk, rk1 = shells[n], shells[n + 1]
    Nk, Nk1 = rk["N"], rk1["N"]
    Ek, Ek1 = rk["E"], rk1["E"]
    pik = rk["d"] / (2 * Ek)
    pik1 = rk1["d"] / (2 * Ek1)
    push = np.zeros(Nk1)
    push[:Nk] = pik
    Dk1, _, _ = diffusion_matrix(rk1["L"])
    W1 = float(ot.emd2(push, pik1, Dk1))
    wasserstein[f"G{n}_to_G{n+1}"] = W1

w_vals = list(wasserstein.values())
w_ratios = [w_vals[i] / w_vals[i + 1] for i in range(len(w_vals) - 1)]

print("=== Identity check d^2=R_eff ===", identity_check)
print("=== Class symmetry (should be ~0) ===", class_symmetry)
print("=== eps_abs ratios ===", eps_ratios)
print("=== Wasserstein values ===", w_vals)
print("=== Wasserstein ratios ===", w_ratios)

registry = {
    "identity_check_d2_eq_Reff": identity_check,
    "vertex_class_symmetry_max_std": class_symmetry,
    "diameter_diffusion_metric": diam_data,
    "epsilon_abs_metric_invariance_violation": eps_abs,
    "epsilon_abs_ratios": eps_ratios,
    "epsilon_sq_metric_invariance_violation": eps_sq,
    "measure_defect_TV_L1_L2": measure_defect,
    "wasserstein1_diffusion_ground_metric": wasserstein,
    "wasserstein1_ratios": w_ratios,
}
with open("/home/user/URSP/reconstruction/C004I_convergence_registry.json", "w") as f:
    json.dump(registry, f, indent=2)

# CSVs
with open("/home/user/URSP/reconstruction/C004I_diameter.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["shell", "N", "diffusion_diameter", "lambda1"])
    for k, v in diam_data.items():
        w.writerow([k, v["N"], v["diam"], v["lambda1"]])

with open("/home/user/URSP/reconstruction/C004I_measure_defects.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["transition", "TV", "L1", "L2", "Wasserstein1_diffusion"])
    for k in measure_defect:
        w.writerow([k, measure_defect[k]["TV"], measure_defect[k]["L1"], measure_defect[k]["L2"], wasserstein[k]])

print("\nSaved C004I_convergence_registry.json, C004I_diameter.csv, C004I_measure_defects.csv")

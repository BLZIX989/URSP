"""
C-004C, Section 17 demonstration: even if we resolve the generator ambiguity by
using the SAME certified combinatorial Laplacian L=D-A that the rest of ARBS
already uses (GEO-003/DER-SPC-004: K_t=exp(-tL)), with its actual stationary
distribution (uniform -- the true fixed point of exp(-tL) for a connected
graph, NOT the degree distribution BRIDGE B-006 states; see the generator-
mismatch note in the closure report), entropy production sigma(t) still
depends materially on the free choice of initial distribution P(0) and
evaluation time t. This is a concrete, numerical demonstration that
argmax_k Pi_0(G_k) is NOT parameter-independent -- it is not an attempt to
define a canonical sigma_k, and no choice made here is treated as canonical.
"""
import numpy as np
import json
from build_arbs import analyze

CHECKPOINT_LC = {
    "G0": 5.770780163555398, "G1": 7.268580400651221, "G2": 12.513856399069492,
    "G3": 23.134563317823480, "G4": 44.317589836356648,
}


def kl_to_uniform(P, N):
    P = np.clip(P, 1e-300, None)
    return float(np.sum(P * np.log(P * N)))


def sigma_at(t, P0, evals, evecs, N, h=1e-6):
    def F(tt):
        coeffs = evecs.T @ P0
        Pt = evecs @ (np.exp(-tt * evals) * coeffs)
        Pt = np.maximum(Pt, 0.0)
        s = Pt.sum()
        if s <= 0:
            return np.nan
        Pt = Pt / s
        return kl_to_uniform(Pt, N)
    return -(F(t + h) - F(t - h)) / (2 * h)


results = {}
demo_times = [0.05, 0.2, 0.6]

for n in range(5):
    key = f"G{n}"
    r = analyze(n)
    L = r["L"]
    N = r["N"]
    evals, evecs = np.linalg.eigh(L)
    delta_spec = float(np.sort(evals[evals > 1e-8])[0])
    lam_c = CHECKPOINT_LC[key]

    node_choices = {"first_node_(shell0_L)": 0, "last_node_(topshell_R)": N - 1}
    shell_results = {}
    for node_name, node_idx in node_choices.items():
        P0 = np.zeros(N)
        P0[node_idx] = 1.0
        for t in demo_times:
            sigma = sigma_at(t, P0, evals, evecs, N)
            if sigma is not None and sigma > 1e-12:
                pi0 = (delta_spec - lam_c) / sigma
            else:
                pi0 = None
            shell_results[f"{node_name}_t={t}"] = {
                "sigma": None if sigma is None else float(sigma),
                "Pi0": pi0,
            }
    results[key] = {"delta_spec": delta_spec, "lambda_c": lam_c, "samples": shell_results}

# For each (node_choice, t) combination used consistently across shells, compute argmax_k Pi0
combo_argmax = {}
for node_name in ["first_node_(shell0_L)", "last_node_(topshell_R)"]:
    for t in demo_times:
        combo = f"{node_name}_t={t}"
        vals = {}
        for k, v in results.items():
            entry = v["samples"].get(combo)
            if entry and entry["Pi0"] is not None:
                vals[k] = entry["Pi0"]
        if vals:
            # argmax = least negative (closest to zero) Pi0
            best = max(vals, key=vals.get)
            combo_argmax[combo] = {"argmax_shell": best, "values": vals}

print(json.dumps(combo_argmax, indent=2))

out = {"per_shell_samples": results, "combo_argmax": combo_argmax}
with open("/home/user/URSP/reconstruction/sigma_nonidentifiability_demo.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nSaved sigma_nonidentifiability_demo.json")

argmaxes = set(v["argmax_shell"] for v in combo_argmax.values())
print("\nDistinct argmax shells across the 6 sampled (P(0), t) combinations:", argmaxes)

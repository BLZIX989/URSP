"""
Section 13: does the free-energy functional F[P||P_ss] yield sigma=-dF/dt>=0
DIRECTLY from the recovered generator Q*=-LD^{-1}, without choosing P(0) or t?

Standard argument (Markov-chain Lyapunov theory), instantiated with the
concretely-derived, concretely-verified (C-004F.2/3) reversible generator:

  dF/dt = sum_i (Q*P)_i (log(P_i/pi_i)+1)
        = sum_i (Q*P)_i log(P_i/pi_i)          [conservation: sum_i(Q*P)_i=0 kills the "+1" term]

Expand (Q*P)_i = sum_j Q_ji P_j (since Q*=Q^T). Using detailed balance pi_i Q_ij = pi_j Q_ji:

  dF/dt = sum_{i,j} Q_ji P_j log(P_i/pi_i)

Symmetrizing over the pair (i,j) using detailed balance (standard master-equation
manipulation) gives the pairwise-flux form

  dF/dt = -(1/2) sum_{i,j} pi_i Q_ij [P_j/pi_j - P_i/pi_i] [log(P_j/pi_j) - log(P_i/pi_i)]

each term of which is <=0 because (a-b)(log a - log b) >= 0 for a,b>0. Hence dF/dt<=0,
with equality iff P=P_ss. This is exactly BRIDGE B-006's own claimed proof method
("the log-sum inequality"), now instantiated on the concrete, fully-derived Q*
rather than asserted abstractly. It requires ONLY detailed balance + conservation
(both proven in C-004F.2/3) -- NOT a choice of P(0) or evaluation time.

This script performs a numerical sanity check of the inequality along several
ARBITRARY sample trajectories (never treated as canonical) to confirm the
algebra above is not silently wrong.
"""
import numpy as np
import json
from arbs_light import analyze_light


def kl(P, pi):
    P = np.clip(P, 1e-300, None)
    return float(np.sum(P * np.log(P / pi)))


results = {}
rng = np.random.default_rng(1)
for n in range(5):
    r = analyze_light(n)
    A, D, L, d, N, E = r["A"], r["D"], r["L"], r["d"], r["N"], r["E"]
    pi = d / (2 * E)
    Dinv = np.diag(1.0 / d)
    Q = -Dinv @ L
    Qstar = Q.T

    evals, evecs = np.linalg.eig(Qstar)
    # sanity checks per sample trajectory
    checks = []
    for trial in range(4):
        P0 = rng.dirichlet(np.ones(N))
        for t in [0.05, 0.3, 1.0]:
            # P(t) = exp(t Qstar) P0, via series (Qstar not symmetric in general basis but fine for small N)
            Msum = np.eye(N)
            term = np.eye(N)
            for k in range(1, 40):
                term = term @ (t * Qstar) / k
                Msum = Msum + term
            Pt = Msum @ P0
            Pt = np.clip(Pt, 0, None)
            Pt = Pt / Pt.sum()
            F_t = kl(Pt, pi)
            # small forward step to estimate derivative sign
            dt = 1e-5
            Msum2 = np.eye(N)
            term2 = np.eye(N)
            for k in range(1, 40):
                term2 = term2 @ ((t + dt) * Qstar) / k
                Msum2 = Msum2 + term2
            Pt2 = Msum2 @ P0
            Pt2 = np.clip(Pt2, 0, None)
            Pt2 = Pt2 / Pt2.sum()
            F_t2 = kl(Pt2, pi)
            dFdt_numeric = (F_t2 - F_t) / dt
            checks.append({"t": t, "F(t)": F_t, "dF/dt_numeric": dFdt_numeric, "sigma=-dF/dt": -dFdt_numeric,
                            "sigma>=0": bool(-dFdt_numeric >= -1e-6)})

    results[f"G{n}"] = {"sample_checks": checks,
                         "all_sigma_nonneg": bool(all(c["sigma>=0"] for c in checks))}

with open("/home/user/URSP/reconstruction/c004f_entropy_consequence.json", "w") as f:
    json.dump(results, f, indent=2)

for k, v in results.items():
    print(k, "all sigma>=0 across 12 sampled (P0,t):", v["all_sigma_nonneg"])

"""
C-004F: degree-weighted thermodynamic continuum recovery.
Executes steps C-004F.1 through C-004F.7 (measure/generator/Dirichlet-form/
refinement/pushforward) for shells G0..G9, extending beyond G0-G4 for trend
analysis per Section 17 (explicitly NOT claimed as proof of k->infinity
convergence from finite data).
"""
import numpy as np
import json
from arbs_light import analyze_light

N_SHELLS = 10  # G0..G9

shells_data = {n: analyze_light(n) for n in range(N_SHELLS)}

# ---------------------------------------------------------------------
# C-004F.1 -- Degree measure recovery
# ---------------------------------------------------------------------
degree_measure_results = {}
for n, r in shells_data.items():
    d = r["d"]
    N = r["N"]
    E = r["E"]
    pi = d / (2 * E)
    u = np.ones(N) / N
    entropy = float(-np.sum(pi * np.log(pi)))
    degree_measure_results[f"G{n}"] = {
        "N": N, "E": E,
        "pi_min": float(pi.min()), "pi_max": float(pi.max()),
        "pi_sum": float(pi.sum()),
        "entropy_H(pi)": entropy,
        "entropy_H(uniform)": float(np.log(N)),
        "||pi-u||_1": float(np.linalg.norm(pi - u, ord=1)),
        "||pi-u||_2": float(np.linalg.norm(pi - u, ord=2)),
    }

# ---------------------------------------------------------------------
# C-004F.2 / .3 -- weighted Hilbert space + generator recovery
# ---------------------------------------------------------------------
generator_results = {}
for n, r in shells_data.items():
    A, D, L, d, N, E = r["A"], r["D"], r["L"], r["d"], r["N"], r["E"]
    pi = d / (2 * E)
    Dinv = np.diag(1.0 / d)

    # positivity/nondegeneracy of the weighted inner product
    weighted_ip_positive = bool(np.all(pi > 0))

    Q = -Dinv @ L
    Qstar = Q.T

    Qstar_d_norm = float(np.linalg.norm(Qstar @ d))
    Qstar_pi_norm = float(np.linalg.norm(Qstar @ pi))

    # detailed balance: pi_i Q_ij = pi_j Q_ji  <=>  diag(pi) Q symmetric
    piQ = np.diag(pi) @ Q
    detailed_balance_residual = float(np.linalg.norm(piQ - piQ.T, ord="fro"))

    # conservation: 1^T Qstar = 0  (sum_i (Qstar P)_i = 0 for any P)
    ones = np.ones(N)
    conservation_residual = float(np.linalg.norm(ones @ Qstar))

    # stochastic semigroup check at a few t values
    stoch_checks = {}
    for t in [0.01, 0.1, 1.0]:
        Tt = __import__("scipy.linalg", fromlist=["expm"]).expm(t * Q) if False else None
    # avoid scipy dependency: use eigen-decomposition-free series via numpy matrix_power fallback
    from numpy.linalg import matrix_power

    def expm_series(M, t, terms=40):
        Msum = np.eye(M.shape[0])
        term = np.eye(M.shape[0])
        for k in range(1, terms):
            term = term @ (t * M) / k
            Msum = Msum + term
        return Msum

    for t in [0.05, 0.2, 1.0]:
        Tt = expm_series(Q, t)
        row_sums = Tt.sum(axis=1)
        nonneg = bool(np.all(Tt > -1e-6))
        row_stochastic = bool(np.allclose(row_sums, 1.0, atol=1e-4))
        stoch_checks[f"t={t}"] = {"row_stochastic": row_stochastic, "nonneg_entries": nonneg,
                                   "max_row_sum_dev": float(np.max(np.abs(row_sums - 1.0)))}

    generator_results[f"G{n}"] = {
        "weighted_inner_product_positive_definite": weighted_ip_positive,
        "Qstar_d_norm_(should_be_0)": Qstar_d_norm,
        "Qstar_pi_norm_(should_be_0)": Qstar_pi_norm,
        "detailed_balance_residual_(should_be_0)": detailed_balance_residual,
        "conservation_residual_1T_Qstar_(should_be_0)": conservation_residual,
        "T(t)_stochastic_checks": stoch_checks,
        "convention": "Q_ij = A_ij/d_i for i!=j, Q_ii=-1 (row generator, row-stochastic exp(tQ)); Q*=Q^T acts on column probability vectors dP/dt=Q*P",
    }

print("=== C-004F.1/2/3 done ===")

# ---------------------------------------------------------------------
# C-004F.4 -- Dirichlet form recovery
# ---------------------------------------------------------------------
dirichlet_results = {}
for n, r in shells_data.items():
    A, D, L, d, N, E = r["A"], r["D"], r["L"], r["d"], r["N"], r["E"]
    pi = d / (2 * E)
    Dinv = np.diag(1.0 / d)
    Q = -Dinv @ L

    def E_form(f, g, A_, E_):
        # E(f,g) = 1/(4E) sum_ij A_ij (f_i-f_j)(g_i-g_j) = (1/(2E)) f^T L g  [derived]
        diff_f = f[:, None] - f[None, :]
        diff_g = g[:, None] - g[None, :]
        return float(np.sum(A_ * diff_f * diff_g) / (4 * E_))

    def inner_mu(f, g, pi_):
        return float(np.sum(f * g * pi_))

    # verify E_k(f,g) = <f,-Qg>_mu for several random test functions
    rng = np.random.default_rng(0)
    residuals = []
    for _ in range(5):
        f = rng.normal(size=N)
        g = rng.normal(size=N)
        lhs = E_form(f, g, A, E)
        rhs = inner_mu(f, -(Q @ g), pi)
        residuals.append(abs(lhs - rhs))
    max_residual = float(max(residuals))

    # E_k(f,f) for standard basis functions (first few)
    basis_vals = [E_form((np.eye(N)[i]), (np.eye(N)[i]), A, E) for i in range(min(N, 5))]

    # kernel of E_k: E(f,f)=0 iff f constant (since = (1/2E) f^T L f, and L psd with ker=span{1})
    const_val = E_form(np.ones(N), np.ones(N), A, E)

    dirichlet_results[f"G{n}"] = {
        "formula": "E_k(f,g) = (1/(4E)) sum_ij A_ij (f_i-f_j)(g_i-g_j) = (1/(2E)) f^T L g",
        "verified_equals_<f,-Qg>_mu_max_residual": max_residual,
        "E_k(e_i,e_i)_first5": basis_vals,
        "E_k(const,const)_(should_be_0)": const_val,
        "ker(E_k)_is_span{1}": "PROVEN: E_k(f,f)=(1/2E) f^T L f >= 0 (L psd); =0 iff Lf=0 iff f constant (G connected)",
    }

print("=== C-004F.4 done ===")

# ---------------------------------------------------------------------
# C-004F.5 -- ARBS refinement map recovery (combinatorial)
# ---------------------------------------------------------------------
refinement_results = {}
for n in range(N_SHELLS - 1):
    r_k = shells_data[n]
    r_k1 = shells_data[n + 1]
    Nk, Nk1 = r_k["N"], r_k1["N"]
    dk = r_k["d"]
    dk1 = r_k1["d"]
    # G_k's vertex set is literally the first Nk vertices of G_{k+1} (inclusion, by construction order)
    inclusion_holds = bool(np.array_equal(r_k["A"], r_k1["A"][:Nk, :Nk]))
    # which vertices' degrees change: R_{k} block (the last shell's R partition in G_k)
    L_off, L_sz, R_off, R_sz = r_k["shells"][n]
    degree_changed = ~np.isclose(dk1[:Nk], dk)
    num_degree_changed = int(degree_changed.sum())
    changed_are_exactly_Rk = bool(np.array_equal(np.where(degree_changed)[0], np.arange(R_off, R_off + R_sz)))
    degree_increase_amount = dk1[R_off:R_off + R_sz] - dk[R_off:R_off + R_sz]

    refinement_results[f"G{n}_to_G{n+1}"] = {
        "inclusion_holds_(G_k_is_induced_subgraph_of_G_k+1)": inclusion_holds,
        "num_vertices_with_changed_degree": num_degree_changed,
        "changed_vertices_are_exactly_R_k": changed_are_exactly_Rk,
        "R_k_degree_increase_(all_equal_2^(n+1)?)": {
            "expected_increase": 2 ** (n + 1),
            "actual_increase_min": float(degree_increase_amount.min()) if len(degree_increase_amount) else None,
            "actual_increase_max": float(degree_increase_amount.max()) if len(degree_increase_amount) else None,
            "uniform": bool(np.allclose(degree_increase_amount, degree_increase_amount[0])) if len(degree_increase_amount) else None,
        },
        "map_type": "INCLUSION/EMBEDDING (G_k is an induced subgraph of G_k+1; ALL of G_k's vertices, edges, "
                     "shells, and partitions are preserved verbatim; only R_k vertices gain new edges to L_k+1)",
        "metric_rescaling_status": "NOT SOURCE-SUPPORTED -- no explicit contraction constant, edge-length law, "
                                    "or embedding-radius rescaling is given anywhere in the corpus for the specific "
                                    "K_{2^k,2^k}/R_{k-1}xL_k construction (only an abstract 'global isotropic "
                                    "contraction constant alpha, 0<alpha<1' is asserted for the GENERIC refinement "
                                    "functor R in the whitepaper's Section 2.1, with no formula tying it to ARBS's "
                                    "actual edge/shell rule).",
    }

print("=== C-004F.5 done ===")

# ---------------------------------------------------------------------
# C-004F.6 -- measure pushforward
# ---------------------------------------------------------------------
pushforward_results = {}
for n in range(N_SHELLS - 1):
    r_k = shells_data[n]
    r_k1 = shells_data[n + 1]
    Nk, Nk1 = r_k["N"], r_k1["N"]
    Ek, Ek1 = r_k["E"], r_k1["E"]
    dk = r_k["d"]
    dk1 = r_k1["d"]
    pi_k = dk / (2 * Ek)
    pi_k1 = dk1 / (2 * Ek1)

    # pushforward of pi_k under inclusion: same mass on old vertices, zero on new ones
    pushforward = np.zeros(Nk1)
    pushforward[:Nk] = pi_k

    diff = pushforward - pi_k1
    tv = 0.5 * float(np.sum(np.abs(diff)))
    l1 = float(np.linalg.norm(diff, ord=1))
    l2 = float(np.linalg.norm(diff, ord=2))
    mass_on_new_vertices = float(pi_k1[Nk:].sum())  # fraction of pi_{k+1}'s mass on genuinely new vertices

    pushforward_results[f"G{n}_to_G{n+1}"] = {
        "total_variation_distance": tv,
        "L1_distance": l1,
        "L2_distance": l2,
        "mass_fraction_pi_{k+1}_on_new_vertices": mass_on_new_vertices,
        "pushforward_equals_pi_{k+1}_exactly": bool(np.allclose(pushforward, pi_k1, atol=1e-12)),
    }

print("=== C-004F.6 done ===")

with open("/home/user/URSP/reconstruction/c004f_degree_measure.json", "w") as f:
    json.dump(degree_measure_results, f, indent=2)
with open("/home/user/URSP/reconstruction/c004f_generator.json", "w") as f:
    json.dump(generator_results, f, indent=2)
with open("/home/user/URSP/reconstruction/c004f_dirichlet.json", "w") as f:
    json.dump(dirichlet_results, f, indent=2)
with open("/home/user/URSP/reconstruction/c004f_refinement.json", "w") as f:
    json.dump(refinement_results, f, indent=2)
with open("/home/user/URSP/reconstruction/c004f_pushforward.json", "w") as f:
    json.dump(pushforward_results, f, indent=2)

print("\nAll C-004F.1-6 JSON artifacts saved.")

# quick trend print for pushforward
print("\nTrend: mass fraction on new vertices, TV distance, by shell transition")
for k, v in pushforward_results.items():
    print(f"  {k}: mass_frac_new={v['mass_fraction_pi_{k+1}_on_new_vertices']:.4f}  TV={v['total_variation_distance']:.4f}")

"""
ARBS-CONSTRUCTION-001: implementation of the bipartite shell graph construction
exactly as specified in this task's Sections 1-13:

    S_k = L_k sqcup R_k,  |L_k|=|R_k|=2^k
    G[S_k] = K_{2^k,2^k}                (intra-shell complete bipartite)
    E(S_{k-1},S_k) = R_{k-1} x L_k       (inter-shell complete bipartite)
    G_n = union_{k=0}^n S_k

Node ordering: shells k=0..n in order; within each shell, L_k block then R_k
block; within each block, increasing local index. This ordering is used
consistently for A, D, L, and B (incidence) below.

No reference to 32, sigma16, sigma17, or any other downstream checkpoint
appears in the construction code below (Sections 1-4). Checkpoint values are
only used afterward, in the comparison step, to test the reconstructed
spectrum -- never to build the graph.
"""
import numpy as np
import json


def build_shell_graph(n):
    """Build G_n. Returns dict with node ordering info, A, N, E, edge list."""
    shells = []          # shells[k] = (L_offset, L_size, R_offset, R_size)
    offset = 0
    for k in range(n + 1):
        size = 2 ** k
        L_offset = offset
        offset += size
        R_offset = offset
        offset += size
        shells.append((L_offset, size, R_offset, size))
    N = offset

    edges = set()

    # intra-shell: K_{2^k,2^k}
    for k in range(n + 1):
        L_off, L_sz, R_off, R_sz = shells[k]
        for i in range(L_sz):
            u = L_off + i
            for j in range(R_sz):
                v = R_off + j
                edges.add((u, v) if u < v else (v, u))

    # inter-shell: R_{k-1} x L_k
    for k in range(1, n + 1):
        _, _, Rprev_off, Rprev_sz = shells[k - 1]
        Lk_off, Lk_sz, _, _ = shells[k]
        for i in range(Rprev_sz):
            u = Rprev_off + i
            for j in range(Lk_sz):
                v = Lk_off + j
                edges.add((u, v) if u < v else (v, u))

    edges = sorted(edges)
    E = len(edges)

    A = np.zeros((N, N), dtype=np.float64)
    for (u, v) in edges:
        A[u, v] = 1.0
        A[v, u] = 1.0

    return {
        "n": n, "N": N, "E": E, "shells": shells, "edges": edges, "A": A,
    }


def incidence_matrix(N, edges):
    """Oriented incidence matrix B (N x E): lower index -> higher index."""
    E = len(edges)
    B = np.zeros((N, E), dtype=np.float64)
    for e, (u, v) in enumerate(edges):
        B[u, e] = 1.0
        B[v, e] = -1.0
    return B


def analyze(n):
    g = build_shell_graph(n)
    A, N, E, edges = g["A"], g["N"], g["E"], g["edges"]

    # expected counts (Section 5/6 closed forms, verified independently)
    N_expected = 2 * (2 ** (n + 1) - 1)
    E_intra_expected = sum(4 ** k for k in range(n + 1))
    E_inter_expected = sum(2 ** (2 * k - 1) for k in range(1, n + 1))
    E_expected = E_intra_expected + E_inter_expected

    checks = {}
    checks["N_matches_expected"] = (N == N_expected)
    checks["E_matches_expected"] = (E == E_expected)

    D = np.diag(A.sum(axis=1))
    checks["A_symmetric"] = bool(np.allclose(A, A.T))
    checks["no_self_loops"] = bool(np.all(np.diag(A) == 0))
    checks["D_symmetric"] = bool(np.allclose(D, D.T))
    checks["degrees_nonneg"] = bool(np.all(np.diag(D) >= 0))
    checks["sum_degrees_eq_2E"] = bool(np.isclose(np.trace(D), 2 * E))

    L = D - A
    checks["L_symmetric"] = bool(np.allclose(L, L.T))
    checks["L_row_sums_zero"] = bool(np.allclose(L.sum(axis=1), 0, atol=1e-8))

    # bipartite check on the GLOBAL partition L=union L_k, R=union R_k
    global_L = set()
    global_R = set()
    for (L_off, L_sz, R_off, R_sz) in g["shells"]:
        global_L.update(range(L_off, L_off + L_sz))
        global_R.update(range(R_off, R_off + R_sz))
    bipartite_ok = all(
        (u in global_L and v in global_R) or (u in global_R and v in global_L)
        for (u, v) in edges
    )
    checks["G_bipartite_global_LR"] = bool(bipartite_ok)

    B = incidence_matrix(N, edges)
    checks["B_shape_ok"] = (B.shape == (N, E))
    L_from_B = B @ B.T
    checks["L_eq_BBt"] = bool(np.allclose(L, L_from_B, atol=1e-8))

    eigvals_L = np.linalg.eigvalsh(L)
    eigvals_L_sorted = np.sort(eigvals_L)
    checks["L_eigs_nonneg"] = bool(np.all(eigvals_L_sorted > -1e-8))
    kernel_dim = int(np.sum(eigvals_L_sorted < 1e-8))
    checks["kernel_dim_is_1"] = (kernel_dim == 1)

    # connectivity via kernel dimension (number of connected components)
    connected = (kernel_dim == 1)
    checks["G_connected"] = bool(connected)

    # Dirac operator D_G = [[0,B],[B^T,0]]
    top = np.hstack([np.zeros((N, N)), B])
    bot = np.hstack([B.T, np.zeros((E, E))])
    D_G = np.vstack([top, bot])
    checks["D_G_symmetric"] = bool(np.allclose(D_G, D_G.T))

    D_G2 = D_G @ D_G
    block_expected = np.zeros((N + E, N + E))
    block_expected[:N, :N] = B @ B.T
    block_expected[N:, N:] = B.T @ B
    checks["D_G_squared_block_identity"] = bool(np.allclose(D_G2, block_expected, atol=1e-6))
    checks["upper_left_block_eq_L"] = bool(np.allclose((D_G2)[:N, :N], L, atol=1e-6))

    # singular values of B = |Dirac eigenvalues| restricted to N-block sector
    singvals_B = np.linalg.svd(B, compute_uv=False)
    singvals_B_sorted = np.sort(singvals_B)[::-1]  # descending like sigma_1 >= sigma_2 ...

    # sigma_j^2 should equal nonzero eigenvalues of L (ascending order convention
    # used in the checkpoint sheet: sigma_16, sigma_17 are the 16th/17th SMALLEST
    # nonzero singular values in ascending order -- test both orderings explicitly)
    lam_nonzero_ascending = eigvals_L_sorted[eigvals_L_sorted > 1e-8]
    sigma_from_L_ascending = np.sqrt(np.maximum(lam_nonzero_ascending, 0))

    # full Dirac spectrum via eigvalsh (should be +-sigma_j and zeros)
    eigvals_DG = np.linalg.eigvalsh(D_G)
    pos = np.sort(eigvals_DG[eigvals_DG > 1e-8])
    neg = np.sort(eigvals_DG[eigvals_DG < -1e-8])
    checks["dirac_pm_sigma_pairing"] = bool(
        len(pos) == len(neg) and np.allclose(pos, -neg[::-1], atol=1e-6)
    )
    checks["sigma_from_L_matches_dirac_positive"] = bool(
        np.allclose(np.sort(sigma_from_L_ascending), pos, atol=1e-6)
    )

    return {
        "n": n, "N": N, "E": E, "N_expected": N_expected, "E_expected": E_expected,
        "checks": checks,
        "A": A, "L": L, "B": B, "D_G": D_G,
        "laplacian_eigs_ascending": eigvals_L_sorted,
        "dirac_positive_ascending": pos,
        "kernel_dim": kernel_dim,
    }


if __name__ == "__main__":
    import os
    os.makedirs("/home/user/URSP/reconstruction/arrays", exist_ok=True)
    results = {}
    for n in range(5):
        r = analyze(n)
        results[f"G{n}"] = r
        print(f"--- G{n} ---")
        print("N:", r["N"], "expected", r["N_expected"], "match:", r["N"] == r["N_expected"])
        print("E:", r["E"], "expected", r["E_expected"], "match:", r["E"] == r["E_expected"])
        for k, v in r["checks"].items():
            print(f"  {k}: {'PASS' if v else 'FAIL'}")
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_A.npy", r["A"])
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_L.npy", r["L"])
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_B.npy", r["B"])
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_DG.npy", r["D_G"])
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_laplacian_spectrum.npy", r["laplacian_eigs_ascending"])
        np.save(f"/home/user/URSP/reconstruction/arrays/G{n}_dirac_positive_spectrum.npy", r["dirac_positive_ascending"])

    # ---- checkpoint comparison (NOT used to build the graph; used only here) ----
    print("\n=== CHECKPOINT COMPARISON ===")
    checkpoint_report = {}

    g3 = results["G3"]
    pos_g3 = g3["dirac_positive_ascending"]
    print("G3 positive Dirac spectrum count:", len(pos_g3))
    if len(pos_g3) >= 17:
        sigma16_calc = pos_g3[15]  # 0-indexed 16th smallest
        sigma17_calc = pos_g3[16]
        print(f"  sigma16 (calculated, ascending #16) = {sigma16_calc!r}")
        print(f"  sigma17 (calculated, ascending #17) = {sigma17_calc!r}")
        print(f"  checkpoint sigma16 = 2.828427124746192")
        print(f"  checkpoint sigma17 = 2.849152618684595")
        checkpoint_report["G3_sigma16_calculated"] = float(sigma16_calc)
        checkpoint_report["G3_sigma17_calculated"] = float(sigma17_calc)
        checkpoint_report["G3_sigma16_checkpoint"] = 2.828427124746192
        checkpoint_report["G3_sigma17_checkpoint"] = 2.849152618684595
        checkpoint_report["G3_sigma16_match"] = bool(np.isclose(sigma16_calc, 2.828427124746192, atol=1e-6))
        checkpoint_report["G3_sigma17_match"] = bool(np.isclose(sigma17_calc, 2.849152618684595, atol=1e-6))
    else:
        print("  Fewer than 17 positive singular values in G3 -- cannot compare sigma16/sigma17")
        checkpoint_report["G3_error"] = f"only {len(pos_g3)} positive singular values"

    g4 = results["G4"]
    pos_g4 = g4["dirac_positive_ascending"]
    print("G4 positive Dirac spectrum count:", len(pos_g4))
    if len(pos_g4) >= 17:
        sigma16_g4 = pos_g4[15]
        sigma17_g4 = pos_g4[16]
        print(f"  sigma16 (calculated) = {sigma16_g4!r}")
        print(f"  sigma17 (calculated) = {sigma17_g4!r}")
        print(f"  checkpoint sigma16=sigma17 = 3.464101615137755")
        checkpoint_report["G4_sigma16_calculated"] = float(sigma16_g4)
        checkpoint_report["G4_sigma17_calculated"] = float(sigma17_g4)
        checkpoint_report["G4_checkpoint"] = 3.464101615137755
        checkpoint_report["G4_degenerate_match"] = bool(np.isclose(sigma16_g4, sigma17_g4, atol=1e-6))
        checkpoint_report["G4_value_match"] = bool(np.isclose(sigma16_g4, 3.464101615137755, atol=1e-6))
    else:
        checkpoint_report["G4_error"] = f"only {len(pos_g4)} positive singular values"

    with open("/home/user/URSP/reconstruction/checkpoint_comparison.json", "w") as f:
        json.dump(checkpoint_report, f, indent=2)

    # full audit dump (checks only, matrices go to .npy)
    audit = {}
    for gname, r in results.items():
        audit[gname] = {
            "N": r["N"], "N_expected": r["N_expected"],
            "E": r["E"], "E_expected": r["E_expected"],
            "kernel_dim": r["kernel_dim"],
            "checks": r["checks"],
            "laplacian_eigs_first20": [float(x) for x in r["laplacian_eigs_ascending"][:20]],
            "dirac_positive_first20": [float(x) for x in r["dirac_positive_ascending"][:20]],
        }
    with open("/home/user/URSP/reconstruction/reconstruction_audit.json", "w") as f:
        json.dump(audit, f, indent=2)

    print("\nSaved arrays/, checkpoint_comparison.json, reconstruction_audit.json")

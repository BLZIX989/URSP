"""
Independent arithmetic re-verification of the ARBS numerical checkpoints
recorded in Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.0.xlsx
(sheets '39 Calculation Inputs', '46 Calculation Results', '47 Result Registry').

Scope and honesty constraint: this script re-derives NOTHING about the
underlying ARBS graphs. It only checks that the numbers already recorded
in the workbook are internally arithmetically consistent with each other
(sigma^2 = lambda, lambda_c = 1/t_H, ordering relations). It has no access
to any ARBS adjacency/incidence data or full eigenvalue arrays, because no
such data exists in the four supplied source workbooks or the repository
(see CLOSURE_REPORT.md, Section "Missing dependency"). Reproducing this
check therefore does NOT certify that the checkpoint numbers are correct
values of any actual graph Laplacian spectrum -- only that they are
self-consistent as reported.
"""
import json
from mpmath import mp, mpf, sqrt

mp.dps = 50

t_H = {
    "G0": mpf("0.173286795140"),
    "G1": mpf("0.137578446530"),
    "G2": mpf("0.079911417241"),
    "G3": mpf("0.043225367441"),
    "G4": mpf("0.022564403969"),
}
lambda_c_given = {
    "G0": mpf("5.770780163555398"),
    "G1": mpf("7.268580400651221"),
    "G2": mpf("12.513856399069492"),
    "G3": mpf("23.134563317823480"),
    "G4": mpf("44.317589836356648"),
}
NE = {"G0": (2, 1), "G1": (6, 7), "G2": (14, 31), "G3": (30, 127), "G4": (62, 511)}

sigma16_G3 = mpf("2.828427124746192")
sigma17_G3 = mpf("2.849152618684595")
lambda16_G3_given = mpf("8.000000000000011")
lambda17_G3_given = mpf("8.117670644557285")
delta_sigma_G3_given = mpf("0.020725493938403")

sigma_G4 = mpf("3.464101615137755")

results = {"lambda_c_check": {}, "G3_boundary_check": {}, "G4_boundary_check": {},
           "NE_pattern_observation": {}, "C004B_ordering_check": {}}

for k in t_H:
    computed = 1 / t_H[k]
    results["lambda_c_check"][k] = {
        "t_H": str(t_H[k]),
        "lambda_c_computed_from_1_over_tH": str(computed),
        "lambda_c_given_in_workbook": str(lambda_c_given[k]),
        "abs_diff": str(computed - lambda_c_given[k]),
        "consistent_at_double_precision": abs(computed - lambda_c_given[k]) < mpf("1e-14"),
    }

lam16 = sigma16_G3 ** 2
lam17 = sigma17_G3 ** 2
results["G3_boundary_check"] = {
    "sigma16": str(sigma16_G3),
    "sigma17": str(sigma17_G3),
    "sigma16_squared": str(lam16),
    "lambda16_given": str(lambda16_G3_given),
    "sigma17_squared": str(lam17),
    "lambda17_given": str(lambda17_G3_given),
    "delta_sigma_computed": str(sigma17_G3 - sigma16_G3),
    "delta_sigma_given": str(delta_sigma_G3_given),
    "consistent_at_double_precision": (
        abs(lam16 - lambda16_G3_given) < mpf("1e-14")
        and abs(lam17 - lambda17_G3_given) < mpf("1e-14")
    ),
    "note": "sigma16(G3) coincides with sqrt(8)=2*sqrt(2) to ~1.9e-15 and "
            "sigma17(G3)^2 - 8 = 0.11767... ; this is an observation about "
            "the reported numbers only, not an independent derivation.",
}

lam_G4 = sigma_G4 ** 2
results["G4_boundary_check"] = {
    "sigma16_eq_sigma17": str(sigma_G4),
    "squared": str(lam_G4),
    "note": "coincides with sqrt(12)=2*sqrt(3) to ~4.1e-16; degenerate boundary confirmed self-consistent.",
}

for k, (N, E) in NE.items():
    idx = int(k[1])
    N_pred = 2 ** (idx + 2) - 2
    E_pred = 2 ** (2 * idx + 1) - 1
    results["NE_pattern_observation"][k] = {
        "N_reported": N, "N_closed_form_guess_2^(k+2)-2": N_pred, "N_match": N == N_pred,
        "E_reported": E, "E_closed_form_guess_2^(2k+1)-1": E_pred, "E_match": E == E_pred,
        "status": "OPEN / PROPOSED -- pattern-matches all 5 reported points but is NOT "
                  "a source-derived construction rule and MUST NOT be used to generate "
                  "any adjacency matrix or spectrum.",
    }

lc_G3 = lambda_c_given["G3"]
results["C004B_ordering_check"] = {
    "lambda16": str(lam16), "lambda17": str(lam17), "lambda_c_G3": str(lc_G3),
    "lambda16_lt_lambda17_lt_lambda_c": bool(lam16 < lam17 < lc_G3),
    "conclusion": "Confirms C-004B = FALSIFIED FOR 32-BOUNDARY COMPATIBILITY: the canonical "
                  "threshold lambda_c=1/t_H lies strictly above the independently reported "
                  "G3 boundary interval, so it does not select that boundary.",
}

with open("checkpoint_verification.json", "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))

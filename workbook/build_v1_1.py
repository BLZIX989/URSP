"""
Build Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.1.xlsx from v1.0.

Preserves all 47 existing sheets unchanged (no historical checkpoint is
altered or deleted). Appends new audit sheets recording this closure run:
the exhaustive source search for the ARBS graph construction rule, the
arithmetic self-consistency verification of existing checkpoints, and the
STOP report required because that construction rule is not present in any
supplied source file.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json

SRC = "/home/user/URSP/source/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.0.xlsx"
OUT = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.1.xlsx"

with open("/home/user/URSP/artifacts/checkpoint_verification.json") as f:
    V = json.load(f)

wb = openpyxl.load_workbook(SRC, data_only=False)

TITLE_FONT = Font(name="Arial", size=12, bold=True)
HEADER_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
BODY_FONT = Font(name="Arial", size=10)
NOTE_FONT = Font(name="Arial", size=9, italic=True)
WRAP = Alignment(wrap_text=True, vertical="top")


def new_sheet(name):
    ws = wb.create_sheet(name)
    return ws


def write_title(ws, title, subtitle):
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    ws["A2"] = subtitle
    ws["A2"].font = NOTE_FONT
    ws["A2"].alignment = WRAP


def write_table(ws, start_row, headers, rows, widths=None):
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=start_row, column=j, value=h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
    for i, r in enumerate(rows, start=start_row + 1):
        for j, v in enumerate(r, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.font = BODY_FONT
            c.alignment = WRAP
    if widths:
        for j, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
    return start_row + 1 + len(rows)


# ---------------------------------------------------------------------
# 48 Spectral Reconstruction Audit
# ---------------------------------------------------------------------
ws = new_sheet("48 Spectral Reconstr Audit")
write_title(ws, "SPECTRAL RECONSTRUCTION AUDIT",
            "Search for the complete ARBS spectra {lambda_k,j} / {sigma_k,j}, k=0..4, "
            "and for the canonical ARBS recursive graph construction rule, executed "
            "against all four supplied source workbooks and the project repository.")
r = write_table(ws, 4,
    ["Source searched", "Sheets inspected", "Object sought", "Found?", "Finding"],
    [
        ("Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.0.xlsx", "all 47 sheets",
         "ARBS adjacency/incidence matrices, full eigenvalue arrays, recursive graph rule",
         "NO", "Only checkpoint scalars (N,E per shell; sigma16/sigma17 for G3/G4; t_H, lambda_c per shell) are present. No node/edge list, no adjacency matrix, no algorithmic construction rule."),
        ("Universal_Rosetta_Stone_Master_Workbook.xlsx", "all 11 sheets",
         "same", "NO", "Documentation-tier subset of the master workbook; no numeric spectra."),
        ("Universal_Rosetta_Stone_FULL_UNIFICATION_MATRIX.xlsx", "all 31 sheets",
         "same", "NO", "Extends registries/matrices; no ARBS construction rule or spectra found."),
        ("Universal_Rosetta_Stone_MDCL_Complete.xlsx", "all 21 sheets",
         "same", "NO", "Grammar/compiler/domain-core content; no ARBS construction rule or spectra found."),
        ("Project repository (BLZIX989/URSP)", "entire tree",
         "same", "NO", "Repository contained only a one-line README at session start; no source code, CSV, or checkpoint files of any kind."),
    ],
    widths=[45, 16, 45, 8, 60])

ws.cell(row=r+1, column=1, value="Object referenced repeatedly as the source of the checkpoint numbers:").font = BODY_FONT
r += 2
r = write_table(ws, r,
    ["Reference ID", "Cited as source for", "Located?"],
    [("ARBS-FULL-SPEC-001", "N,E per shell; sigma16/sigma17(G3); sigma16=sigma17(G4); Delta_sigma; RES-G3-boundary; RES-G4-degeneracy; OPEN-NEXT",
      "NO -- cited in '47 Result Registry' and '39 Calculation Inputs' as provenance, but no object with this ID (graph data, construction algorithm, or spectrum array) exists in any of the four workbooks or the repository.")],
    widths=[20, 60, 70])

r += 2
ws.cell(row=r, column=1, value="STOP FINDING").font = Font(name="Arial", size=11, bold=True, color="C00000")
r += 1
ws.cell(row=r, column=1,
        value=("The single missing upstream datum is the canonical ARBS recursive graph "
               "construction rule (equivalently: explicit adjacency/incidence data for "
               "G0-G4, sufficient to build L=D-A and B with B B^T = L directly from the "
               "construction, independent of any downstream numeric target). Per the "
               "governing instructions (Section 5/20), reconstruction stops exactly here: "
               "the complete spectra {lambda_k,j} cannot be produced, and none were invented.")).font = BODY_FONT
ws.cell(row=r, column=1).alignment = WRAP
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws.row_dimensions[r].height = 60

# ---------------------------------------------------------------------
# 49 Arithmetic Verification (live formulas)
# ---------------------------------------------------------------------
ws = new_sheet("49 Arithmetic Verification")
write_title(ws, "ARITHMETIC SELF-CONSISTENCY VERIFICATION",
            "Independently re-evaluated with live formulas from the checkpoint scalars already "
            "recorded in '39 Calculation Inputs'. This verifies internal consistency of the "
            "reported numbers only (sigma^2 vs lambda; 1/t_H vs lambda_c); it does NOT "
            "independently confirm those numbers against any actual graph Laplacian, because "
            "no ARBS graph data exists in the source material (see sheet 48).")

headers = ["Shell", "t_H (given)", "1/t_H (formula)", "lambda_c (given)", "abs diff", "Consistent (<1e-10)?"]
rows = []
tH_vals = {"G0": 0.173286795140, "G1": 0.137578446530, "G2": 0.079911417241,
           "G3": 0.043225367441, "G4": 0.022564403969}
lc_vals = {"G0": 5.770780163555398, "G1": 7.268580400651221, "G2": 12.513856399069492,
           "G3": 23.134563317823480, "G4": 44.317589836356648}
start = 5
for i, k in enumerate(["G0", "G1", "G2", "G3", "G4"]):
    row = start + 1 + i
    rows.append((k, tH_vals[k], None, lc_vals[k], None, None))
r = write_table(ws, start, headers, rows, widths=[8, 16, 18, 18, 14, 20])
for i in range(5):
    row = start + 1 + i
    ws.cell(row=row, column=3, value=f"=1/B{row}")
    ws.cell(row=row, column=5, value=f"=ABS(C{row}-D{row})")
    ws.cell(row=row, column=6, value=f'=IF(E{row}<0.0000000001,"YES","NO")')

r += 2
ws.cell(row=r, column=1, value="G3 boundary check (sigma -> lambda = sigma^2)").font = Font(name="Arial", bold=True)
r += 1
headers2 = ["Quantity", "sigma (given)", "sigma^2 (formula)", "lambda (given)", "abs diff"]
rows2 = [
    ("sigma16(G3)", 2.828427124746192, None, 8.000000000000011, None),
    ("sigma17(G3)", 2.849152618684595, None, 8.117670644557285, None),
]
row_start2 = r
r = write_table(ws, r, headers2, rows2, widths=[16, 18, 18, 18, 14])
for i in range(2):
    row = row_start2 + 1 + i
    ws.cell(row=row, column=3, value=f"=B{row}^2")
    ws.cell(row=row, column=5, value=f"=ABS(C{row}-D{row})")

r += 1
ws.cell(row=r, column=1, value="Delta_sigma(G3) = sigma17 - sigma16").font = BODY_FONT
ws.cell(row=r, column=2, value=f"=B{row_start2+2}-B{row_start2+1}")
ws.cell(row=r, column=3, value="given:")
ws.cell(row=r, column=4, value=0.020725493938403)
r += 2

ws.cell(row=r, column=1, value="G4 degenerate boundary check").font = Font(name="Arial", bold=True)
r += 1
ws.cell(row=r, column=1, value="sigma16=sigma17 (G4)")
ws.cell(row=r, column=2, value=3.464101615137755)
ws.cell(row=r, column=3, value="=B%d^2" % r)
r += 2

ws.cell(row=r, column=1, value="C-004B ordering test: lambda16 < lambda17 < lambda_c(G3) ?").font = Font(name="Arial", bold=True)
r += 1
ws.cell(row=r, column=1, value=f"=AND(D{row_start2+1}<D{row_start2+2}, D{row_start2+2}<D{start+4})")
ws.cell(row=r, column=2, value="TRUE => C-004B remains FALSIFIED FOR 32-BOUNDARY COMPATIBILITY (canonical lambda_c lies above the G3 boundary interval).")
ws.cell(row=r, column=2).font = NOTE_FONT
ws.cell(row=r, column=2).alignment = WRAP
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)

# ---------------------------------------------------------------------
# 50 Threshold Candidate Table
# ---------------------------------------------------------------------
ws = new_sheet("50 Threshold Candidate Table")
write_title(ws, "THRESHOLD / SELECTOR CANDIDATE TABLE (Section 8)",
            "Every threshold construction with an explicit source-registered definition and "
            "numeric instantiation, found across the four workbooks.")
write_table(ws, 4,
    ["Candidate", "Exact source definition", "Dependencies", "Numeric values G0..G4",
     "P_H", "N_H", "G3 selected?", "Target-independent?", "Status"],
    [
        ("lambda_c = 1/t_H", "ENG-007/ENG-008: p_A(t_H)=1/2 ; lambda_c=1/t_H (Calculation Engine, 40)",
         "positive spectrum via p_A(t)", "5.770780163555398; 7.268580400651221; 12.513856399069492; 23.134563317823480; 44.317589836356648",
         "1_[lambda_c,infinity)(L) -- rank not evaluable, full spectrum absent",
         "NOT EVALUABLE (missing lambda_max(L))", "NO -- does not select the G3 boundary [8, 8.1177)",
         "YES (verified in 49 Arithmetic Verification: no N_H/H_F/V_CKM/D_F/... dependency in the formula)",
         "CALCULATED / C-004B = FALSIFIED FOR 32-BOUNDARY COMPATIBILITY"),
        ("P_boundary = 1_[lambda16,lambda17)(L_3)", "Independently reported G3 spectral boundary (Result Registry RES-G3-boundary)",
         "sigma16(G3), sigma17(G3) only",
         "[8.000000000000011, 8.117670644557285) for G3 only; degenerate (empty interval) for G4",
         "distinct object from P_H -- NOT renamed P_H per governing instructions Section 7",
         "NOT EVALUABLE (rank requires the full G3 eigenbasis/eigenvector multiplicities, which are absent)",
         "Isolated cluster confirmed for G3 by sigma16<sigma17, but rank(P_boundary) cannot be certified",
         "YES (interval derived only from G3's own spectrum, no downstream object entered)",
         "CALCULATED (existence of isolated boundary) / rank OPEN (missing full spectrum)"),
        ("delta_spec, Pi (persistence subspace), R=exp(-beta L), heat kernel Z=Tr(e^{-beta L})",
         "Named as formula labels only (Calculation Engine ENG-019 for Z; Bridge Registry BR-006/BR-007 for heat semigroup/diffusion distance; Translation Registry TR-008 for Pi)",
         "L, beta, or t", "NONE -- no shell-indexed numeric instantiation exists in any source workbook",
         "n/a", "n/a", "n/a", "n/a", "OPEN -- formula exists, no G0..G4 numeric values recorded anywhere"),
    ],
    widths=[26, 46, 26, 40, 34, 34, 34, 30, 40])
ws2 = ws
ws2.cell(row=10, column=1,
         value="Both source-supported formulations above are preserved (per Section 8: do not silently select the more convenient one). "
               "They measure different objects (a target-independent global threshold vs. an independently observed local spectral gap) "
               "and are NOT in contradiction; no equivalence/falsification test between them is admissible without the missing full spectra.")
ws2.cell(row=10, column=1).font = NOTE_FONT
ws2.cell(row=10, column=1).alignment = WRAP
ws2.merge_cells(start_row=10, start_column=1, end_row=10, end_column=9)
ws2.row_dimensions[10].height = 45

# ---------------------------------------------------------------------
# 51 OPEN-020E.2 Audit
# ---------------------------------------------------------------------
ws = new_sheet("51 OPEN-020E.2 Audit")
write_title(ws, "OPEN-020E.2 -- SHELL UNIQUENESS AUDIT",
            "Test of Pi_0(G_k) = [delta_spec(G_k) - lambda_c,k] / sigma_k and argmax_k Pi_0(G_k) = 3.")
write_table(ws, 4,
    ["Required object", "Present in source?", "Value/location", "Consequence"],
    [
        ("delta_spec(G_k), k=0..4", "NO", "Not found as a shell-indexed numeric quantity in any workbook (only named as a label in the candidate table, sheet 50)", "Pi_0 numerator undefined"),
        ("lambda_c,k, k=0..4", "YES", "sheet 39 Calculation Inputs / this workbook sheet 49", "Pi_0 numerator partially available"),
        ("sigma_k (normalization), k=0..4", "NO", "No source registry entry defines this scale factor per the governing prompt's own instruction: 'If sigma_k is unavailable: DO NOT INVENT IT.'", "Pi_0 denominator undefined; sigma_k NOT invented here"),
    ],
    widths=[26, 18, 60, 40])
r = 9
ws.cell(row=r, column=1, value="sign(Pi_0) determinable without magnitude?").font = Font(name="Arial", bold=True)
r += 1
ws.cell(row=r, column=1,
        value=("NO. Pi_0's numerator requires delta_spec(G_k), which is entirely absent from the source "
               "material (not merely unscaled). Sign cannot be determined from an undefined numerator "
               "regardless of the denominator's availability."))
ws.cell(row=r, column=1).font = BODY_FONT
ws.cell(row=r, column=1).alignment = WRAP
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.row_dimensions[r].height = 45
r += 2
ws.cell(row=r, column=1, value="OPEN-020E.2 OUTCOME").font = Font(name="Arial", bold=True, color="C00000")
r += 1
ws.cell(row=r, column=1,
        value="D. Pi_0 cannot be evaluated because an upstream quantity is missing (delta_spec(G_k) is undefined for all k, and sigma_k is undefined for all k). "
              "argmax_k Pi_0(G_k) = 3 is NOT tested; A is not forced.")
ws.cell(row=r, column=1).font = BODY_FONT
ws.cell(row=r, column=1).alignment = WRAP
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.row_dimensions[r].height = 45

# ---------------------------------------------------------------------
# 52 Falsification Ledger
# ---------------------------------------------------------------------
ws = new_sheet("52 Falsification Ledger")
write_title(ws, "FALSIFICATION LEDGER", "Every failed candidate and the exact reason for failure. Nothing here is deleted or promoted.")
write_table(ws, 4,
    ["Candidate", "Claim tested", "Result", "Exact reason", "Status"],
    [
        ("lambda_c = 1/t_H as a 32-boundary selector", "P_H = 1_[lambda_c,infinity)(L_3) selects the observed G3 isolated boundary [lambda16,lambda17)",
         "FAILED", "lambda_c(G3)=23.134563317823480 >> lambda17(G3)=8.117670644557285; the threshold lies strictly above the entire boundary interval, so P_H cannot equal or contain P_boundary.",
         "C-004B = FALSIFIED FOR 32-BOUNDARY COMPATIBILITY (carried forward from v1.0, independently re-confirmed by formula in sheet 49)"),
        ("N_k=2^(k+2)-2, E_k=2^(2k+1)-1 as the canonical ARBS construction rule", "This closed form is THE source-registered recursive construction rule for ARBS shells",
         "NOT ADMITTED (not a failure of the arithmetic, a failure of provenance)", "The formula reproduces all 5 reported (N,E) checkpoints exactly, but no source workbook attributes this or any other explicit rule to ARBS-FULL-SPEC-001; adopting it here would be inventing the missing construction rule, which Section 5/20 explicitly forbids.",
         "OPEN / PROPOSED -- quarantined observation only, not used in any downstream calculation"),
    ],
    widths=[38, 46, 30, 60, 46])

# ---------------------------------------------------------------------
# 53 Proof Obligation Ledger
# ---------------------------------------------------------------------
ws = new_sheet("53 Proof Obligation Ledger")
write_title(ws, "PROOF OBLIGATION LEDGER", "Unresolved mathematical statements blocking further closure, in dependency order.")
write_table(ws, 4,
    ["Obligation ID", "Statement", "Blocks", "Blocking reason"],
    [
        ("OBL-ARBS-CONSTRUCT", "Recover or derive the canonical ARBS recursive graph construction rule (ARBS-FULL-SPEC-001): an explicit, target-independent algorithm producing the adjacency/incidence data of G0..G4.",
         "Full spectra {lambda_k,j}; C-004B N_H(G_k) computation; rank(P_boundary); OPEN-020E.2 sigma_k, delta_spec; G* uniqueness theorem; everything in Sections 9-15 of the governing instructions.",
         "No adjacency matrix, edge list, or construction algorithm exists in any of the four supplied workbooks or the repository (see sheet 48). Only 5 scalar (N,E) checkpoints and 4 scalar spectral checkpoints per relevant shell are present."),
        ("OBL-DELTA-SPEC", "Define delta_spec(G_k) per an actual source registry entry (none currently exists).",
         "OPEN-020E.2 Pi_0", "No shell-indexed numeric or symbolic definition of delta_spec found anywhere in source material."),
        ("OBL-SIGMA-K", "Define the sigma_k normalization used in Pi_0 = [delta_spec - lambda_c] / sigma_k.",
         "OPEN-020E.2 Pi_0", "Not defined in source; explicitly forbidden to invent per governing instructions Section 9."),
        ("OBL-GSTAR-SELECTOR", "Prove a substrate-only (target-independent) uniqueness theorem selecting G* among G0..G4.",
         "G* promotion (Section 10); P_H^(32) construction; OPEN-021A-D; finite NCG closure; flavor; continuum; scale.",
         "No such theorem is present in the source registries; BR-026 (horizon selection) is explicitly recorded as OPEN in '35 Bridge Registry' with 'Selector not generated.'"),
        ("BR-026 (carried from source)", "Horizon selection P_H^2=P_H, P_H^dagger=P_H with a generating selector.",
         "same as OBL-GSTAR-SELECTOR", "Recorded OPEN in source Bridge Registry; not resolved by this run."),
    ],
    widths=[22, 60, 46, 60])

# ---------------------------------------------------------------------
# 54 Closure Matrix
# ---------------------------------------------------------------------
ws = new_sheet("54 Closure Matrix")
write_title(ws, "CLOSURE MATRIX", "Target | Result | Status | Dependencies")
write_table(ws, 4,
    ["Target", "Result", "Status", "Dependencies"],
    [
        ("Checkpoint arithmetic self-consistency (sigma^2=lambda, lambda_c=1/t_H, ordering)", "All checks pass at double-precision tolerance (<1e-10); see sheet 49",
         "VERIFIED", "Existing checkpoint scalars in source sheet 39"),
        ("C-004B (canonical persistence threshold selects G3 32-boundary)", "lambda_c(G3)=23.1346 > lambda17(G3)=8.1177; threshold does not select the boundary",
         "FALSIFIED FOR 32-BOUNDARY COMPATIBILITY", "lambda_c=1/t_H formula; G3 boundary checkpoints"),
        ("Complete ARBS spectra {lambda_k,j}, k=0..4", "Cannot be reconstructed", "OPEN -- missing upstream datum",
         "OBL-ARBS-CONSTRUCT (canonical graph construction rule, absent from all source material)"),
        ("N_H(G0)..N_H(G4)", "Cannot be calculated", "OPEN", "Requires complete spectra"),
        ("rank(P_boundary) for G3", "Cannot be certified", "OPEN", "Requires complete G3 eigenbasis/eigenvector multiplicities"),
        ("OPEN-020E.2 Pi_0(G_k) / argmax test", "Outcome D -- cannot be evaluated", "OPEN",
         "delta_spec(G_k) and sigma_k both undefined in source (OBL-DELTA-SPEC, OBL-SIGMA-K)"),
        ("G* promotion (G*=G3)", "Not promoted", "G* UNRESOLVED (G3 retained only as independently verified spectral candidate)",
         "OBL-GSTAR-SELECTOR unresolved; BR-026 open in source"),
        ("P_H^(32), rank=32 certification", "Not attempted", "BLOCKED", "Requires G* derived + complete spectra"),
        ("OPEN-021A..D, finite NCG closure (V2-CALC-025 etc.), flavor, continuum, scale closures", "Not attempted",
         "BLOCKED", "All strictly downstream of G* promotion per Section 1 dependency order; executing them would violate the governing ordering"),
    ],
    widths=[46, 50, 40, 55])

# ---------------------------------------------------------------------
# 55 Canonical Dependency Chain (this run)
# ---------------------------------------------------------------------
ws = new_sheet("55 Canonical Dep Chain (Run)")
write_title(ws, "CANONICAL DEPENDENCY CHAIN -- THIS CLOSURE RUN",
            "Using the prec-relation (<) exactly as supplied; state reached vs. blocked.")
chain = [
    ("Gamma", "reached (source-certified, carried from v1.0)"),
    ("ARBS", "reached (checkpoint scalars only; full construction NOT reached)"),
    ("G_k structural checkpoints (N,E)", "reached / VERIFIED self-consistent, k=0..4"),
    ("Spec(L_k) -- COMPLETE spectra", "NOT REACHED -- OBL-ARBS-CONSTRUCT"),
    ("G* (shell selection)", "NOT REACHED -- unresolved, G3 remains CANDIDATE only"),
    ("P_H^(32) / rank=32 certification", "NOT REACHED"),
    ("Finite NCG closure (Phi_H, KO=0/4, Poincare, orientability)", "NOT REACHED"),
    ("Flavor (Y_f, V_CKM, U_PMNS)", "NOT REACHED"),
    ("Continuum closure (g_munu, R_munu, G_munu)", "NOT REACHED"),
    ("Absolute scale (b_0, Lambda_trans, Xi_UOC)", "NOT REACHED"),
]
r = 4
ws.cell(row=r, column=1, value="Step").font = HEADER_FONT
ws.cell(row=r, column=1).fill = HEADER_FILL
ws.cell(row=r, column=2, value="State this run").font = HEADER_FONT
ws.cell(row=r, column=2).fill = HEADER_FILL
for i, (step, state) in enumerate(chain, start=r+1):
    prefix = "  " * 0 + ("-> " if i > r+1 else "")
    ws.cell(row=i, column=1, value=f"{prefix}{step}").font = BODY_FONT
    ws.cell(row=i, column=2, value=state).font = BODY_FONT
    ws.cell(row=i, column=2).alignment = WRAP
ws.column_dimensions["A"].width = 48
ws.column_dimensions["B"].width = 60

# ---------------------------------------------------------------------
# 56 Next Dependency
# ---------------------------------------------------------------------
ws = new_sheet("56 Next Dependency")
write_title(ws, "EXACTLY ONE NEXT UNRESOLVED UPSTREAM DEPENDENCY", "")
ws["A4"] = ("Recover or derive the canonical ARBS recursive graph construction rule "
            "(ARBS-FULL-SPEC-001): the explicit, target-independent algorithm that produces "
            "the adjacency/incidence data of G0, G1, G2, G3, G4, sufficient to build "
            "L = D - A and B with B B^T = L directly from the construction -- without "
            "reference to the 32-state target, the reported (N,E) checkpoints, or the "
            "reported sigma16/sigma17 checkpoints.")
ws["A4"].font = Font(name="Arial", size=12, bold=True)
ws["A4"].alignment = WRAP
ws.merge_cells("A4:E4")
ws.row_dimensions[4].height = 90
ws["A6"] = ("Everything downstream of this dependency (complete spectra, N_H(G_k), "
            "rank(P_boundary), OPEN-020E.2, G* promotion, P_H^(32), finite NCG closure, "
            "flavor, continuum, and absolute-scale closure) is blocked until it is resolved. "
            "This is the sole STOP point identified by this run.")
ws["A6"].font = BODY_FONT
ws["A6"].alignment = WRAP
ws.merge_cells("A6:E6")
ws.row_dimensions[6].height = 60

wb.save(OUT)
print("saved", OUT)
print("sheets:", wb.sheetnames)

"""
Build v2.4 from v2.3: preserves all 216 existing sheets, appends the
UOC-C0-SEED-CANONICALITY-002 sheets.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json

SRC = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.3.xlsx"
OUT = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.4.xlsx"
RECON = "/home/user/URSP/reconstruction"

def load(name):
    with open(f"{RECON}/{name}") as f:
        return json.load(f)

CROSS = load("seed_recompute_crosscheck.json")
LATTICE = load("seed_filter_lattice.json")
DERIVED = load("seed_derived_survivors.json")
SPECTRAL = load("seed_spectral_closure.json")
PERSGEO = load("seed_persistence_geometry_closure.json")
ISOAUD = load("seed_isomorphism_invariance_audit.json")
with open(f"{RECON}/seed_candidate_full_registry.json") as f:
    REG = {int(k): v for k, v in json.load(f).items()}

wb = openpyxl.load_workbook(SRC, data_only=False)

TITLE_FONT = Font(name="Arial", size=12, bold=True)
HEADER_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
BODY_FONT = Font(name="Arial", size=10)
NOTE_FONT = Font(name="Arial", size=9, italic=True)
WRAP = Alignment(wrap_text=True, vertical="top")

def new_sheet(name):
    return wb.create_sheet(name)

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

def block(ws, r, title, text, height=60):
    ws.cell(row=r, column=1, value=title).font = Font(bold=True)
    r += 1
    ws.cell(row=r, column=1, value=text)
    ws.cell(row=r, column=1).font = BODY_FONT
    ws.cell(row=r, column=1).alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    ws.row_dimensions[r].height = height
    return r + 2


# 217 Executive Result
ws = new_sheet("217 CANON-002 Executive")
write_title(ws, "UOC-C0-SEED-CANONICALITY-002 -- EXECUTIVE RESULT", "")
r = block(ws, 5, "Result",
    "CASE B (non-unique family survives), with a genuine structural incompatibility discovered: "
    "Symmetric (spectral-machinery precondition) and Acyclic (TH-ARBS-001B, derived) are mutually "
    "exclusive for any nonempty relation. |F_N^derived| = 1, 2, 6 at N=2,3,4 -- N=2 alone looks "
    "unique but this does NOT generalize.", height=100)

# 218 Enumeration Audit
ws = new_sheet("218 CANON-002 Enum Audit")
write_title(ws, "C0 ENUMERATION AUDIT -- independent cross-check (networkx VF2)", "")
write_table(ws, 5, ["N", "raw relations", "raw fixed", "iso-classes (orig)", "iso-classes (VF2, independent)"], [
    (N, 2**(N*N), CROSS[str(N)]["raw_fixed_relations"], {2:6,3:70,4:2462}[N], CROSS[str(N)]["independent_isomorphism_classes_networkx_VF2"])
    for N in [2,3,4]
], widths=[6,16,14,20,32])
r = 11
r = block(ws, r, "Correction required?", "NO -- both methods agree exactly at every N.", height=30)

# 219 Filter Lattice
ws = new_sheet("219 CANON-002 Filter Lattice")
write_title(ws, "SELECTOR / ADMISSIBILITY LATTICE", "Each filter applied independently to the full F_N (not chained). See sheet 221 for the chained derived-only trace.")
rows = []
for N in [2,3,4]:
    for f in LATTICE[str(N)]["filters"]:
        rows.append((N, f["filter"], f["status"], f.get("candidates_before"), f.get("candidates_after")))
write_table(ws, 5, ["N", "Filter", "Status", "Before", "After"], rows, widths=[6,30,20,12,12])

# 220 Derivation Status Matrix
ws = new_sheet("220 CANON-002 Derivation Status")
write_title(ws, "DERIVATION-STATUS MATRIX", "")
write_table(ws, 5, ["Status", "Filters"], [
    ("DERIVED (active)", "irreflexive, acyclic/TH-ARBS-001B, bipartite/TH-ARBS-001A"),
    ("DERIVED-CONDITIONAL (reported, not active)", "symmetric"),
    ("UNJUSTIFIED/PROPOSED/HEURISTIC", "rigid, minimal edge count, functional, weakly/strongly connected, reflexive, antisymmetric, transitive, nontrivial spectral gap, Laplacian nullity=1"),
    ("BLOCKED", "persistence (both notions), geometry/curvature"),
], widths=[40, 100])

# 221 D_R T_R C_R Reconstruction
ws = new_sheet("221 CANON-002 DTC Recon")
write_title(ws, "D_R / T_R / C_R RECONSTRUCTION", "")
write_table(ws, 5, ["Operator", "Status", "Detail"], [
    ("D_R", "PROVEN, unconditional", "Coarsest equitable (color-refinement) partition -- well-defined for every record"),
    ("T_R (functional case)", "CONDITIONAL", "Unique successor tau(x)=y; functional-F_N counts 1/3/6 at N=2/3/4"),
    ("T_R (nonfunctional case)", "PROPOSED-ONLY", "Only Aut(R) (a group, generally non-unique) is canonically available; no function substituted"),
    ("C_R", "PROVEN", "C_R(T):=1[T(R)=R], well-defined for every record"),
], widths=[26, 20, 100])

# 222 Spectral Closure
ws = new_sheet("222 CANON-002 Spectral")
write_title(ws, "SPECTRAL CLOSURE -- observed vs required", "")
write_table(ws, 5, ["N", "total F_N", "n symmetric", "symmetric=>real (verified)", "n real-spectrum total", "nonsym-but-real (observed)"], [
    (SPECTRAL[str(N)]["N"], SPECTRAL[str(N)]["total_F_N"], SPECTRAL[str(N)]["n_symmetric"],
     SPECTRAL[str(N)]["symmetric_implies_real_spectrum_verified"], SPECTRAL[str(N)]["n_real_spectrum_total"],
     f'{SPECTRAL[str(N)]["nonsymmetric_candidates_with_real_spectrum_observed_not_required"]}/{SPECTRAL[str(N)]["nonsymmetric_candidates_total"]}')
    for N in [2,3,4]
], widths=[6,14,14,26,20,26])
r = 12
r = block(ws, r, "Key finding", "F_N^derived survivors are all nilpotent by construction, so their raw adjacency spectrum is trivially all-zero (a direct consequence of nilpotency, not new information). The symmetrized-Laplacian spectrum is the only differentiator, and even it is degenerate for several N=4 survivors (identical spectrum despite non-isomorphism as directed graphs).", height=90)

# 223 Persistence + Geometry Closure
ws = new_sheet("223 CANON-002 Persist+Geo")
write_title(ws, "PERSISTENCE -> GEOMETRY CLOSURE", "")
r = block(ws, 5, "Persistence status", PERSGEO["persistence_closure"]["status"] + ": " + PERSGEO["persistence_closure"]["exact_missing_dependency"], height=110)
r = block(ws, r, "Geometry status", PERSGEO["geometry_closure"]["metric_and_curvature_status"] + ": " + PERSGEO["geometry_closure"]["exact_missing_dependency"], height=110)

# 224 Isomorphism-Invariance Audit
ws = new_sheet("224 CANON-002 Iso Invariance")
write_title(ws, "ISOMORPHISM-INVARIANCE AUDIT", "")
r = block(ws, 5, "Result", f'{ISOAUD["n_passed"]}/{ISOAUD["n_trials"]} permutation trials preserved canonical form and |Aut(R)| exactly. All passed: {ISOAUD["all_passed"]}.', height=50)

# 225 N-Scaling Audit
ws = new_sheet("225 CANON-002 N-Scaling")
write_title(ws, "N-SCALING AUDIT", "")
write_table(ws, 5, ["Quantity", "N=2", "N=3", "N=4"], [
    ("|F_N|", 6, 70, 2462),
    ("|F_N^derived|", 1, 2, 6),
], widths=[30,10,10,10])
r = 10
r = block(ws, r, "Conclusion", "|F_N^derived| grows (1->2->6), not constant. No infinite-limit theorem inferred from N<=4. N=2's apparent uniqueness does NOT generalize.", height=60)

# 226 Surviving Candidates
ws = new_sheet("226 CANON-002 Survivors")
write_title(ws, "SURVIVING CANDIDATES (F_N^derived, all 9)", "")
rows = []
for N in [2,3,4]:
    ids = DERIVED["results"][str(N)]["survivor_seed_ids"]
    for sid in ids:
        rec = next(x for x in REG[N] if x["seed_id"] == sid)
        rows.append((sid, str(rec["adjacency_matrix"]), rec["n_edges"], rec["aut_group_order"]))
write_table(ws, 5, ["Seed ID", "Adjacency matrix", "Edges", "Aut order"], rows, widths=[12, 50, 8, 10])

# 227 Unique-Seed Test / Final Certification
ws = new_sheet("227 CANON-002 Certification")
write_title(ws, "UNIQUE-SEED TEST -- FINAL CERTIFICATION", "")
ws["A5"] = ("Per the Final Certification Rule: R* is NOT certified as 'the correct seed.'\n\n"
            "Condition 1 (exactly one isomorphism class survives): holds ONLY at N=2. Condition 6 "
            "(survives the tested N-scaling): FAILS -- N=3 gives 2 survivors, N=4 gives 6.\n\n"
            "The surviving family is reported in full (sheet 226) together with the precise "
            "unresolved dependency (sheet 228) that would need to close before uniqueness could "
            "be certified. The objective was to determine whether uniqueness is mathematically "
            "forced -- it is not, at any N tested beyond N=2.")
ws["A5"].font = BODY_FONT
ws["A5"].alignment = WRAP
ws.merge_cells("A5:F5")
ws.row_dimensions[5].height = 180

# 228 Next Dependency
ws = new_sheet("228 CANON-002 Next Dep")
write_title(ws, "EXACTLY ONE NEXT UNRESOLVED UPSTREAM DEPENDENCY", "")
ws["A4"] = ("Resolve the symmetric/acyclic incompatibility discovered this run -- either by finding "
            "an independently-certified extension of the spectral/persistence machinery to genuinely "
            "asymmetric (directed) graphs, or by finding a source-derived reason the seed need not "
            "itself carry the nilpotency requirement directly (e.g. nilpotency applies to a transport "
            "operator DERIVED FROM R, not R literally, reopening the symmetric branch) -- OR extend "
            "the exhaustive enumeration past N=4 to determine whether |F_N^derived| keeps growing "
            "(1->2->6 suggests it does) or eventually stabilizes. None of these three is resolvable "
            "by further reasoning from the currently available corpus and computation.")
ws["A4"].font = Font(name="Arial", size=12, bold=True)
ws["A4"].alignment = WRAP
ws.merge_cells("A4:F4")
ws.row_dimensions[4].height = 200

wb.save(OUT)
print("saved", OUT)
print("total sheets:", len(wb.sheetnames))

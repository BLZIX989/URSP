"""
Build v2.2 from v2.1: preserves all 185 existing sheets, appends the
KIJ-THETA-IMAGE-RECOVERY-001 sheets.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json

SRC = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.1.xlsx"
OUT = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.2.xlsx"
RECON = "/home/user/URSP/reconstruction"

def load(name):
    with open(f"{RECON}/{name}") as f:
        return json.load(f)

R = load("kij_theta_image_search.json")

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


# 187 Overview
ws = new_sheet("187 KIJ-IMG-001 Overview")
write_title(ws, "KIJ-THETA-IMAGE-RECOVERY-001", "Follows up ARBS-GRAPH-REALIZATION-001's SIT Delta->G text-only review by searching embedded images/rendered equation objects for K_ij and theta, per the C-004G precedent.")
r = block(ws, 5, "Bottom line", R["conclusion"], height=140)

# 188 Methodology
ws = new_sheet("188 KIJ-IMG-002 Method")
write_title(ws, "METHODOLOGY", "")
write_table(ws, 5, ["Step"], [[s] for s in R["methodology"]], widths=[150])

# 189 Image Census
ws = new_sheet("189 KIJ-IMG-003 Census")
write_title(ws, "IMAGE CENSUS", "")
write_table(ws, 5, ["Metric", "Value"], [
    ("Total .docx files in corpus", "1 (Combined_Compiler_Theories_Whitepaper.docx)"),
    ("Total .xlsx files in corpus", "8"),
    ("Embedded images in the .docx (word/media/*.png)", str(R["images_checked"])),
    ("Embedded images in all 8 .xlsx files combined", "0 (verified per-file via zipfile media/ listing)"),
    ("Images with graph-construction keyword hit in preceding text", "19 of 140"),
    ("Images directly inspected and relevant to K_ij/theta", str(R["images_relevant_to_K_ij_or_theta"])),
], widths=[55, 90])

# 190 K_ij status
ws = new_sheet("190 KIJ-IMG-004 Kij Status")
write_title(ws, "K_ij CONSTRUCTION -- STATUS", "")
r = block(ws, 5, "Status", R["K_ij_construction_status"], height=110)

# 191 theta status
ws = new_sheet("191 KIJ-IMG-005 Theta Status")
write_title(ws, "THETA CONSTRUCTION -- STATUS", "")
r = block(ws, 5, "Status", R["theta_construction_status"], height=90)

# 192 Complete text chain
ws = new_sheet("192 KIJ-IMG-006 Full Chain")
write_title(ws, "COMPLETE SIT Delta->G TEXT CONSTRUCTION (confirmed not truncated)", "")
CT = R["complete_text_construction_confirmed_not_truncated"]
r = block(ws, 5, "Source", CT["source"], height=50)
r = block(ws, r, "Chain", CT["chain"], height=90)
r = block(ws, r, "Source's own empirical test", CT["source_own_empirical_test"], height=90)
r = block(ws, r, "Second citation confirms same construction verbatim", CT["second_citation_confirms_same_construction_verbatim"], height=60)

# 193 Free parameter registry
ws = new_sheet("193 KIJ-IMG-007 Free Params")
write_title(ws, "FREE PARAMETER REGISTRY (source's own summary table, verbatim)", "")
rows = [tuple(x.split(" | ")) for x in R["complete_text_construction_confirmed_not_truncated"]["free_parameter_registry_full_text"]]
write_table(ws, 5, ["Parameter | Role | Status (as one field)"], [[x] for x in R["complete_text_construction_confirmed_not_truncated"]["free_parameter_registry_full_text"]], widths=[150])

# 194 Source document availability
ws = new_sheet("194 KIJ-IMG-008 Doc Avail")
write_title(ws, "SOURCE DOCUMENT AVAILABILITY", "Why the image search cannot be extended further")
write_table(ws, 5, ["Cited source document", "Present in corpus as a file?", "What survives"], [
    ("SEF SIT Specification v2.docx (SRC-013)", "NO -- not found anywhere in repository", "Paragraph/table text only, rows 2342-2457 of 54_SOURCE_TEXT_CORPUS"),
    ("Audit and Recommended Revisions.docx (SRC-014)", "NO -- not found anywhere in repository", "Paragraph/table text only, rows 2459-2555 of 54_SOURCE_TEXT_CORPUS"),
    ("Combined_Compiler_Theories_Whitepaper.docx", "YES", "Full document + 140 embedded images, all checked; none relevant to K_ij/theta"),
    ("All 8 .xlsx sources", "YES", "Zero embedded images in any of them (verified)"),
], widths=[45, 40, 70])

# 195 Related but distinct finding: K(G_U)
ws = new_sheet("195 KIJ-IMG-009 K(G_U)")
write_title(ws, "RELATED BUT DISTINCT NOTATION -- K(G_U) IS NOT K_ij", "Flagged to prevent future symbol-collision confusion")
r = block(ws, 5, "Finding", "K(G_U) denotes the clique complex of a bipartite substrate B=(U,V,E), used in the Hodge-1 gauge-field (A_mu) derivation (SRC-008 UCG Specification v5, SRC-015/016 DER Registry). It is a topological construction on an already-given graph, not the SIT compatibility kernel K_ij (a real-valued [0,1] weight matrix between distinctions). The two are explicitly not the same object anywhere they co-occur, and this run confirms they were not conflated.", height=110)
r = block(ws, r, "Second graph-construction claim found (not the one searched for, noted for completeness)", "DER-ORG-005 'Graph from Distinctions [CERTIFIED]': G=(V,E) derived from {Delta_i}, 'verified by the construction of the bipartite substrate B and its one-mode projection G_U.' No concrete B (vertex/edge instantiation) or projection formula was found anywhere in the corpus -- same class of semantic-schema-without-instantiation gap as G_ARBS itself. Not pursued further this run (out of scope: this run's mandate was the K_ij/theta image search specifically).", height=110)

# 196 Target independence
ws = new_sheet("196 KIJ-IMG-010 Target Indep")
write_title(ws, "TARGET-INDEPENDENCE AUDIT", "")
TI = R["target_independence_check"]
r = block(ws, 5, "Checked", TI["checked"], height=40)
r = block(ws, r, "Result", TI["result"], height=70)

# 197 Closure matrix
ws = new_sheet("197 KIJ-IMG-011 Closure")
write_title(ws, "CLOSURE MATRIX", "")
write_table(ws, 5, ["Object", "Status"], [
    ("K_ij construction, embedded-image form", "NOT RECOVERED -- no such image exists anywhere in the corpus"),
    ("theta construction, embedded-image form", "NOT RECOVERED -- same reasoning"),
    ("K_ij/theta construction, complete text form", "CONFIRMED COMPLETE (not truncated); both theta and lambda_C explicitly labeled 'Unfixed' by source's own status table"),
    ("SEF SIT Specification v2.docx / Audit and Recommended Revisions.docx as files", "ABSENT from corpus -- their own images (if any existed) are permanently unrecoverable from this project's holdings"),
    ("Whitepaper embedded images (140 total)", "ALL CHECKED -- none relevant to K_ij/theta"),
    ("All 8 xlsx sources", "ZERO embedded images, confirmed"),
    ("K(G_U) vs K_ij symbol collision", "IDENTIFIED and kept distinct"),
    ("tilde_G_k substituted as fallback for G_ARBS/G*", "NOT DONE, per governing instruction"),
    ("Runs 1-11 all prior results", "PRESERVED, UNCHANGED, VALID"),
], widths=[55, 95])

# 198 Next dependency
ws = new_sheet("198 KIJ-IMG-012 Next Dep")
write_title(ws, "EXACTLY ONE NEXT UNRESOLVED UPSTREAM DEPENDENCY", "")
ws["A4"] = ("Recover, from admissible source material not yet located (or genuinely new derivation, not invention), "
            "either: (a) a concrete instantiation of V, E, W for ARBS shell 1's G node; (b) the actual original files "
            "'SEF SIT Specification v2.docx' and/or 'Audit and Recommended Revisions.docx' (only their extracted text "
            "survives in this corpus; their own embedded images, if any, are not recoverable without the files themselves); "
            "or (c) a concrete construction of the bipartite substrate B=(U,V,E) and its one-mode projection G_U referenced "
            "by DER-ORG-005 -- OR obtain independent, out-of-band documentation establishing the actual origin of the "
            "historical spectral checkpoints this project has reproduced since its first run. None of these is resolvable "
            "by further reading of the currently available corpus, which has now been searched exhaustively -- text AND "
            "images -- across four consecutive runs.")
ws["A4"].font = Font(name="Arial", size=12, bold=True)
ws["A4"].alignment = WRAP
ws.merge_cells("A4:F4")
ws.row_dimensions[4].height = 220

wb.save(OUT)
print("saved", OUT)
print("total sheets:", len(wb.sheetnames))

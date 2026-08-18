"""
Build v2.0 from v1.9 (v1.9 already exists, per instruction use v2.0):
preserves all 141 existing sheets, appends the ARBS-ONTOLOGY-RECOVERY-001
sheets.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json

SRC = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.9.xlsx"
OUT = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.0.xlsx"
RECON = "/home/user/URSP/reconstruction"

def load(name):
    with open(f"{RECON}/{name}") as f:
        return json.load(f)

ONTO = load("arbs_ontology_registry.json")
ACR = load("arbs_acronym_registry.json")
TYP = load("arbs_type_registry.json")
DEP = load("arbs_dependency_registry.json")
HYP = load("arbs_hypergraph.json")
PROJ = load("arbs_graph_projection.json")
INV = load("arbs_projection_invariants.json")
SPEC = load("arbs_spectral_inheritance.json")
RECL = load("arbs_prior_result_reclassification.json")
TI = load("arbs_target_independence.json")

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


# 142 Overview
ws = new_sheet("142 ARBS-ONTO-001 Overview")
write_title(ws, "ARBS-ONTOLOGY-RECOVERY-001", "")
r = block(ws, 5, "Central finding", ONTO["central_finding"], height=90)
r = block(ws, r, "Case classification", PROJ["case_classification"]["finding"] + " Status: " + PROJ["case_classification"]["status"], height=100)

# 143 Acronym Recovery
ws = new_sheet("144 ARBS-ONTO-002 Acronym")
write_title(ws, "ACRONYM RECOVERY", "ARBS = " + ACR["full_expansion"])
rows = [(k, v["recovered_meaning"], v["status"]) for k, v in ACR["components"].items()]
write_table(ws, 5, ["Letter/component", "Recovered meaning", "Status"], rows, widths=[16, 90, 40])

# 145 Source Search
ws = new_sheet("145 ARBS-ONTO-003 Source Search")
write_title(ws, "SOURCE SEARCH", "")
d = ONTO["full_source_definition"]
r = block(ws, 5, "Location", d["location"])
r = block(ws, r, "Definition (verbatim)", d["definition"], height=60)
r = block(ws, r, "Node taxonomy (verbatim)", d["node_taxonomy"], height=50)
r = block(ws, r, "Shell taxonomy (verbatim)", d["shell_taxonomy"], height=50)

# 146 Provenance
ws = new_sheet("146 ARBS-ONTO-004 Provenance")
write_title(ws, "PROVENANCE AUDIT", "")
r = block(ws, 5, "Critical observation", d["critical_observation"], height=140)
rows = [(k, v) for k, v in d["shell_registry_table"].items()]
r = write_table(ws, r, ["Shell (k)", "Layer name / primary objects / content"], rows, widths=[10, 130])

# 147 Abelian Structure
ws = new_sheet("147 ARBS-ONTO-005 Abelian")
write_title(ws, "THM-ARBS-ABELIAN-001", "")
a = ONTO["abelian_recovery"]
r = block(ws, 5, "Exact definition", a["exact_definition_recovered"])
r = write_table(ws, r, ["Abelian region examples (source)"], [[x] for x in a["abelian_region_examples_(source-listed)"]], widths=[130])
r += 1
r = write_table(ws, r, ["Non-Abelian region examples (source)"], [[x] for x in a["non_abelian_region_examples_(source-listed)"]], widths=[130])
r += 1
r = block(ws, r, "Proof for the stated operator families", a["proof_for_the_specific_operator_families_listed"], height=70)
r = block(ws, r, "Status", a["status"], height=60)

# 148 Recursive Structure
ws = new_sheet("148 ARBS-ONTO-006 Recursive")
write_title(ws, "THM-ARBS-RECURSION-001", "")
rr = ONTO["recursive_structure_recovery"]
r = block(ws, 5, "Exact mechanism recovered", rr["exact_mechanism_recovered"], height=90)
r = block(ws, r, "Distinction from G_k's construction", rr["distinction_from_G_k's_construction"], height=70)
r = block(ws, r, "Status", rr["status"], height=40)

# 149 Bipartite Structure
ws = new_sheet("149 ARBS-ONTO-007 Bipartite")
write_title(ws, "THM-ARBS-BIPARTITE-001", "")
r = block(ws, 5, "ARBS bipartition", "Object Node vs Operator Node -- a SEMANTIC type bipartition of what mathematical role a node plays (state vs. transformation).", height=40)
r = block(ws, r, "G_k bipartition", "L_j vs R_j -- a purely STRUCTURAL halving of each shell's vertex set, with no semantic role attached to either half.", height=40)
r = block(ws, r, "Conclusion", "These are different bipartitions of different kinds. G_k's L/R split has never been shown, and is not claimed by any source document, to correspond to ARBS's Object/Operator split.", height=50)

# 150 Shell Structure
ws = new_sheet("150 ARBS-ONTO-008 Shell")
write_title(ws, "THM-ARBS-SHELL-001", "")
r = block(ws, 5, "ARBS shell meaning", "8 FIXED organizational/physical-scale layers (k=0 Primitives through k=7 Emergent Structures) -- see full table, sheet 146.", height=40)
r = block(ws, r, "G_k shell meaning", "Combinatorial recursion depth of the bipartite-shell graph construction, UNBOUNDED (k=0,1,2,...,9,10,... as computed throughout this project).", height=40)
r = block(ws, r, "K_{2^k,2^k} canonicality", "NOT source-supported as part of ARBS's own definition -- never mentioned in the ARBS Hyper-Graph Architecture section.", height=40)
r = block(ws, r, "Status", "PROVEN INCOMPATIBLE as literal identification of shell indices; G_k's 'shell' is a naming collision with ARBS's 'shell', not the same object.", height=40)

# 151 Type System
ws = new_sheet("151 ARBS-ONTO-009 Type System")
write_title(ws, "ARBS TYPE SYSTEM", "")
rows = [(e["type"], e["color"], e["direction"], e["meaning"]) for e in TYP["edge_types"]]
r = write_table(ws, 5, ["Edge type", "Color (poster)", "Direction", "Semantic meaning"], rows, widths=[22, 18, 14, 70])
r = block(ws, r, "Node types", TYP["node_types"]["Object Node"] + " | " + TYP["node_types"]["Operator Node"], height=40)
r = block(ws, r, "Comparison to G_k", TYP["comparison_to_G_k"]["conclusion"], height=50)
r = block(ws, r, "Status", TYP["status"], height=40)

# 152 Dependency Relation
ws = new_sheet("152 ARBS-ONTO-010 Dependency")
write_title(ws, "THM-ARBS-DEPENDENCY-001", "")
r = block(ws, 5, "Recovered relation", DEP["recovered_relation"], height=50)
r = write_table(ws, r, ["Axiom", "Status"], [(a, "CERTIFIED") for a in DEP["governing_axioms_(SDR_registry, CERTIFIED elsewhere in corpus)"]], widths=[100, 20])
r = block(ws, r, "Classification", DEP["classification"], height=30)
r = block(ws, r, "Critical distinction from G_k adjacency", DEP["critical_distinction_from_G_k_adjacency"]["finding"] + " " + DEP["critical_distinction_from_G_k_adjacency"]["conclusion"], height=110)
r = block(ws, r, "Status", DEP["status"], height=40)

# 153 Hypergraph Structure
ws = new_sheet("153 ARBS-ONTO-011 Hypergraph")
write_title(ws, "THM-ARBS-HYPERGRAPH-001", "")
r = block(ws, 5, "Recovered definition", HYP["recovered_definition"]["form"] + " General: " + HYP["recovered_definition"]["general_notation"], height=50)
r = block(ws, r, "Certified property", HYP["recovered_definition"]["certified_property"], height=30)
r = block(ws, r, "Reduction to pairwise edges?", HYP["reduction_to_pairwise_edges"]["finding"], height=90)
r = block(ws, r, "G_k hyperedge content", HYP["G_k_hyperedge_content"], height=30)
r = block(ws, r, "Status", HYP["status"], height=60)

# 154 Full ARBS Object
ws = new_sheet("154 ARBS-ONTO-012 Full Object")
write_title(ws, "THE FULL ARBS OBJECT (recovered, not assumed)", "")
ws["A5"] = ("A_k (better: A, since ARBS's shell structure is FIXED, not indexed by an unbounded k) = "
            "(N_obj, N_op, E_typed[9 types], H[hyperedges, arity>=3, Preserves-Measure], "
            "tau: N -> {Object,Operator}, shell: N -> {0,...,7}, feedback: Pi_0 -> G). "
            "This tuple is assembled ENTIRELY from recovered source components (sheets 144-153); "
            "no component was invented or assumed from the acronym alone.")
ws["A5"].font = BODY_FONT
ws["A5"].alignment = WRAP
ws.merge_cells("A5:F5")
ws.row_dimensions[5].height = 90

# 155 Graph Projection
ws = new_sheet("155 ARBS-ONTO-013 Projection")
write_title(ws, "THM-ARBS-REALIZATION-001 -- GRAPH PROJECTION", "")
r = block(ws, 5, "Search result", PROJ["search_result"], height=90)
r = block(ws, r, "What G_k could legitimately be", PROJ["what_G_k_could_legitimately_be"], height=90)
write_table(ws, r, ["Map component", "Status"], list(PROJ["P_k_properties_(since_no_P_k_exists)"].items()), widths=[16, 110])

# 156 Projection Information Loss
ws = new_sheet("156 ARBS-ONTO-014 Info Loss")
write_title(ws, "PROJECTION INFORMATION LOSS", INV["caveat"])
r = write_table(ws, 6, ["Structure that would be lost (IF a projection existed)"], [[x] for x in INV["structure_that_would_be_lost_under_any_forgetful_map_ARBS_to_simple_graph"]], widths=[140])
r = block(ws, r, "Status", INV["status"], height=40)

# 157 Spectral Preservation
ws = new_sheet("157 ARBS-ONTO-015 Spectral")
write_title(ws, "SPECTRAL PRESERVATION", "")
r = block(ws, 5, "Finding", SPEC["finding"], height=130)
r = block(ws, r, "Consequence", SPEC["consequence"], height=90)
r = write_table(ws, r, ["Object", "Status"], list(SPEC["recorded_status"].items()), widths=[40, 90])

# 158 Prior Result Reclassification
ws = new_sheet("158 ARBS-ONTO-016 Reclassify")
write_title(ws, "RECLASSIFICATION OF EVERY PRIOR ARBS-LABELED RESULT", RECL["default_rule"])
rows = [(x["result"], x["original_label"], x["correct_object"], x["new_status"],
         x["depends_on_ARBS_ontology"], x["remains_valid"], x["required_proof"])
        for x in RECL["reclassification_table"]]
write_table(ws, 6, ["Result", "Original label", "Correct object", "New status", "Depends on ARBS ontology?", "Remains valid?", "Required proof"],
            rows, widths=[30, 30, 30, 40, 14, 12, 40])

# 159 Target Independence
ws = new_sheet("159 ARBS-ONTO-017 Target Indep")
write_title(ws, "TARGET-INDEPENDENCE AUDIT", "")
r = block(ws, 5, "Check performed", TI["check"], height=50)
r = block(ws, r, "Result", TI["result"], height=50)
r = block(ws, r, "Construction code check", TI["construction_code_check"], height=30)

# 160 Theorem Registry
ws = new_sheet("160 ARBS-ONTO-018 Theorems")
write_title(ws, "THEOREM REGISTRY", "")
write_table(ws, 5, ["Theorem", "Status"], [
    ("THM-ARBS-ONTOLOGY-001 (ARBS = meta-level derivation-pipeline hypergraph)", "DERIVED / VERIFIED (fully documented in source)"),
    ("THM-ARBS-ABELIAN-001", ONTO["abelian_recovery"]["status"]),
    ("THM-ARBS-RECURSION-001", ONTO["recursive_structure_recovery"]["status"]),
    ("THM-ARBS-BIPARTITE-001", "PROVEN INCOMPATIBLE with G_k's L/R bipartition (different kind of bipartition)"),
    ("THM-ARBS-SHELL-001", "PROVEN INCOMPATIBLE with G_k's shell-index-as-recursion-depth reading"),
    ("THM-ARBS-TYPE-001", TYP["status"]),
    ("THM-ARBS-DEPENDENCY-001", DEP["status"]),
    ("THM-ARBS-HYPERGRAPH-001", HYP["status"]),
    ("THM-ARBS-REALIZATION-001", "PROVEN: no realization map ARBS->G_k currently exists or is source-supported (CASE D)"),
    ("THM-ARBS-SPECTRAL-001", "GRAPH_SPECTRUM_VERIFIED=true; ARBS_SPECTRAL_DERIVATION=OPEN"),
], widths=[50, 90])

# 161 Falsification Ledger
ws = new_sheet("161 ARBS-ONTO-019 Falsification")
write_title(ws, "FALSIFICATION LEDGER", "")
write_table(ws, 5, ["Claim tested", "Result"], [
    ("G_k's L_k/R_k bipartition = ARBS's Object/Operator bipartition", "FALSIFIED -- different bipartition kinds (structural vs. semantic)"),
    ("G_k's shell index k = ARBS's shell index k", "FALSIFIED -- ARBS's k indexes 8 fixed derivation stages; G_k's k is an unbounded combinatorial recursion depth"),
    ("G_k's edges = ARBS's Dependency edges", "FALSIFIED -- symmetric graph adjacency vs. asymmetric strict partial order"),
    ("G_k contains ARBS hyperedges", "FALSIFIED -- G_k has zero arity->=3 relations of any kind"),
    ("K_{2^k,2^k}/R_{k-1}xL_k is documented as ARBS's construction rule", "FALSIFIED (re-confirmed) -- absent from the ARBS Hyper-Graph Architecture section and every other searched location"),
    ("Numeric checkpoint reproduction proves ARBS realization", "REJECTED as a proof method -- explicitly, per this project's own standing principle since run 1"),
], widths=[60, 90])

# 162 MDCL
ws = new_sheet("162 ARBS-ONTO-020 MDCL")
write_title(ws, "CORRECTED CANONICAL DEPENDENCY CHAIN", "")
ws["A5"] = ("Gamma < ARBS [meta-level 8-shell typed dependency hypergraph, feedback-recursive, DOCUMENTED]\n"
            "         < shell-1 Object Node 'G=(V,E,W)' [UNSPECIFIED which G -- no source-supported construction rule]\n"
            "         ??? [NO PROVEN MAP] ???\n"
            "         < G_k [explicit K_{2^k,2^k}/R_{k-1}xL_k bipartite-shell graph -- a self-contained, well-verified "
            "graph family, CASE D: reproduces checkpoints, not proven to realize ARBS]\n"
            "         < B_k < L_k < D_{G_k} < Spec(L_k) < [everything computed in runs 2-9, all VALID as G_k-facts]\n\n"
            "The '???' marks the exact location of the still-open dependency: no source-supported construction "
            "rule or realization map exists to cross from ARBS's shell-1 Object Node to any specific graph.")
ws["A5"].font = BODY_FONT
ws["A5"].alignment = WRAP
ws.merge_cells("A5:F5")
ws.row_dimensions[5].height = 180

# 163 Closure Matrix
ws = new_sheet("163 ARBS-ONTO-021 Closure")
write_title(ws, "CLOSURE MATRIX", "")
write_table(ws, 5, ["Object", "Status"], [
    ("ARBS ontology (name, structure, taxonomy)", "DERIVED / VERIFIED -- fully documented in source"),
    ("ARBS vs G_k relationship", "CASE D -- G_k reproduces checkpoints but is not a proven ARBS realization"),
    ("Abelian property", "DERIVED / VERIFIED for the stated linear-operator-family instances"),
    ("Recursive (feedback) mechanism", "DERIVED / VERIFIED as documented; NOT the mechanism G_k implements"),
    ("Bipartite (Object/Operator) structure", "DERIVED / VERIFIED for ARBS; PROVEN INCOMPATIBLE with G_k's L/R split"),
    ("Shell (8-layer) structure", "DERIVED / VERIFIED for ARBS; PROVEN INCOMPATIBLE with G_k's recursion-depth reading"),
    ("Typed edges/nodes", "DERIVED / VERIFIED for ARBS; FALSIFIED as realized by G_k (zero types present)"),
    ("Dependency relation", "DERIVED / VERIFIED for ARBS; PROVEN NOT realized by G_k's adjacency"),
    ("Hypergraph structure", "DERIVED / VERIFIED for ARBS; PROVEN INCOMPATIBLE with G_k (no hyperedges)"),
    ("Graph realization map ARBS->G_k", "DOES NOT EXIST -- no source support found"),
    ("All runs 1-9 numerical results", "REMAIN VALID as G_k-level facts (see reclassification table, sheet 158)"),
    ("sigma_k, Pi_0, G*, NCG, flavor, scale", "UNTOUCHED, per stop condition"),
    ("PACKET-REFINEMENT-RECOVERY-001", "NOT ACTIVATED -- not required by this run's findings"),
], widths=[46, 100])

# 164 Next Dependency
ws = new_sheet("164 ARBS-ONTO-022 Next Dep")
write_title(ws, "EXACTLY ONE NEXT UNRESOLVED UPSTREAM DEPENDENCY", "")
ws["A4"] = ("Recover or derive, from admissible source material only, a construction rule or realization map "
            "for the SINGLE Object Node 'G=(V,E,W)' that occupies ARBS's shell k=1 -- i.e., determine what "
            "specific graph (if any is ever specified beyond the abstract symbol G) the documented ARBS "
            "architecture actually intends there, OR formally establish, with genuine source support (not "
            "checkpoint reproduction and not directive text asserting recovery), that the K_{2^k,2^k}/"
            "R_{k-1}xL_k construction (G_k) is an admissible or canonical choice for that node. Until this "
            "exists, every downstream numerical result computed throughout this project (runs 1-9, all "
            "preserved and valid) remains correctly interpreted as a G_k-level fact only, not as a "
            "conclusion about the ARBS object documented in source. This is the exact point at which the "
            "entire multi-run derivation chain currently terminates.")
ws["A4"].font = Font(name="Arial", size=12, bold=True)
ws["A4"].alignment = WRAP
ws.merge_cells("A4:F4")
ws.row_dimensions[4].height = 220

wb.save(OUT)
print("saved", OUT)
print("total sheets:", len(wb.sheetnames))

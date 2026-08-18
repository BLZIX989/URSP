"""
Build v2.9 from v2.8: preserves all 280 existing sheets, appends the
OPEN-024B non-abelian bridge's 29 required sheets (OPEN024B-001..029).
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json

SRC = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.8.xlsx"
OUT = "/home/user/URSP/workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.9.xlsx"
RECON = "/home/user/URSP/reconstruction"

def load(name):
    with open(f"{RECON}/{name}") as f:
        return json.load(f)

ALG_REG = load("nonabelian_seed_algebra_registry.json")
REP_REG = load("nonabelian_representation_registry.json")
TRIPLE = load("nonabelian_spectral_triple_registry.json")
THM = load("nonabelian_theorem_registry.json")
CTRL = load("nonabelian_control_results.json")
TI = load("nonabelian_target_independence.json")
BRIDGE = load("nonabelian_bridge_results.json")
PROJ = load("nonabelian_projection_map.json")

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
            c = ws.cell(row=i, column=j, value=str(v) if not isinstance(v, (int, float)) else v)
            c.font = BODY_FONT
            c.alignment = WRAP
    if widths:
        for j, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
    return start_row + 1 + len(rows)

def block(ws, r, title, text, height=60):
    ws.cell(row=r, column=1, value=title).font = Font(bold=True)
    r += 1
    ws.cell(row=r, column=1, value=str(text))
    ws.cell(row=r, column=1).font = BODY_FONT
    ws.cell(row=r, column=1).alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    ws.row_dimensions[r].height = height
    return r + 2


SHEET_PREFIX = 281  # first available sheet number after 280 ASYM-021

# 001 Overview
ws = new_sheet(f"{SHEET_PREFIX} NAB-001 Overview")
write_title(ws, "OPEN-024B (NON-ABELIAN) -- COMMUTANT NCG BRIDGE", "")
r = block(ws, 5, "Objective", "Determine whether a genuinely non-abelian finite algebra can be "
          "canonically derived from the seed's own internal structure and used to close the finite "
          "NCG axiom set, changing exactly one ingredient from the frozen SEMANTIC-FUNCTOR-BRIDGE-001 "
          "/ OPEN-024B (asymmetric) results: the algebra.", height=90)
r = block(ws, r, "Result", "A_seed := Comm(D_F), the commutant of the seed's own Hermitian D_F, is "
          "non-abelian for 56/259 seeds (11/23 at N=4, 45/231 at N=5; 0 at N=2,3). For these seeds, "
          "FIRST-ORDER HOLDS UNIVERSALLY -- the first time in the entire investigation -- but "
          "ORDER-ZERO FAILS UNIVERSALLY, for a proven general reason (THM-NAB-ORDER-ZERO-"
          "OBSTRUCTION-001). Outcome B: canonical algebra, one axiom unresolved.", height=110)
SHEET_PREFIX += 1

# 002 Seed Algebra Candidates
ws = new_sheet(f"{SHEET_PREFIX} NAB-002 Seed Algebra Cand")
write_title(ws, "A_SEED CANDIDATES ACROSS F_N^derived_v2", "A_seed := Comm(D_F)")
hist = {}
for s in ALG_REG["seeds"]:
    key = (s["N"], tuple(sorted(s["block_dims"])))
    hist[key] = hist.get(key, 0) + 1
rows = [(N, str(bd), cnt) for (N, bd), cnt in sorted(hist.items())]
write_table(ws, 5, ["N", "block_dims (sorted)", "count"], rows, widths=[8, 30, 10])
SHEET_PREFIX += 1

# 003 Endomorphism Algebra (4A)
ws = new_sheet(f"{SHEET_PREFIX} NAB-003 Endomorphism Alg")
write_title(ws, "4A: ENDOMORPHISM ALGEBRA -- NOT PURSUED SEPARATELY", "")
r = block(ws, 5, "Note", "End(H_F^bare)=M_N(C), the full endomorphism algebra of the seed's own "
          "N-dimensional carrier space, is trivially non-abelian for N>=2 but contains NO seed "
          "information at all (it doesn't depend on R). Control F (see NAB-023) tests it directly: "
          "both order-zero AND first-order fail for M_N(C) (first-order residual 2.0, vs machine "
          "precision for Comm(D_F)) -- confirming this candidate is a worse, not better, starting "
          "point. Comm(D_F) (4B) was prioritized because it is the smallest non-arbitrary algebra "
          "that both is seed-derived (depends on R via D_F) and automatically satisfies first-order "
          "by construction.", height=160)
SHEET_PREFIX += 1

# 004 Commutant Analysis (4B, primary construction)
ws = new_sheet(f"{SHEET_PREFIX} NAB-004 Commutant Analysis")
write_title(ws, "4B: COMMUTANT ANALYSIS -- A_seed := Comm(D_F)", "primary construction this run")
r = block(ws, 5, "Definition", "D_F Hermitian (proven) => unitarily diagonalizable, H_F^bare = "
          "(+)_lambda E_lambda. Comm(D_F) = (+)_lambda End(E_lambda), a standard external linear-"
          "algebra fact applied to a seed-derived operator.", height=70)
r = block(ws, r, "Non-abelian iff", "D_F has a repeated eigenvalue (checked exactly, tol=1e-6, "
          "eigh on the real-symmetric D_F).", height=50)
witness_rows = [(TRIPLE["witness_seed"]["N"], TRIPLE["witness_seed"]["seed_id"],
                  str(TRIPLE["A_seed"]["block_dims"]), TRIPLE["A_seed"]["dim"],
                  TRIPLE["A_seed"]["max_irrep_dim"])]
write_table(ws, r, ["N", "seed_id", "block_dims", "dim A_seed", "max irrep dim"], witness_rows, widths=[6,10,20,14,16])
SHEET_PREFIX += 1

# 005 Relation Algebra (4C/4D)
ws = new_sheet(f"{SHEET_PREFIX} NAB-005 Relation Algebra")
write_title(ws, "4C/4D: PATH/INCIDENCE AND RELATION-COMPOSITION ALGEBRAS -- DEFERRED", "")
r = block(ws, 5, "Status", "Not computed this run. Comm(D_F) (4B) produced a clean, general, "
          "provable closure/obstruction pair (THM-NAB-005/006/ORDER-ZERO-OBSTRUCTION-001) covering "
          "ANY conjugation-closed seed-derived algebra combined with the standard swap-conjugate "
          "real structure -- since 4C/4D candidates would also be built from R's real adjacency "
          "matrix, they inherit conj(A)=A automatically, so THM-NAB-ORDER-ZERO-OBSTRUCTION-001 "
          "predicts the SAME order-zero obstruction would recur for any non-abelian algebra "
          "produced by these mechanisms too, under this representation/reality convention. Not "
          "independently verified by direct construction this run -- reported honestly as a "
          "predicted-but-untested consequence, not a proven fact for 4C/4D specifically.", height=180)
SHEET_PREFIX += 1

# 006 Bipartite Operator Algebra (4E)
ws = new_sheet(f"{SHEET_PREFIX} NAB-006 Bipartite Operator Alg")
write_title(ws, "4E: BIPARTITE OPERATOR ALGEBRA T:H_R->H_L -- DEFERRED", "")
r = block(ws, 5, "Status", "Not computed this run, for the same reason as 4C/4D (see NAB-005). "
          "TT^dagger and T^dagger T (T being the seed's off-diagonal block, essentially N_orient "
          "itself) are also real-matrix-derived and hence conjugation-closed, so the same predicted "
          "obstruction applies.", height=110)
SHEET_PREFIX += 1

# 007 Hyperedge Algebra (4F)
ws = new_sheet(f"{SHEET_PREFIX} NAB-007 Hyperedge Algebra")
write_title(ws, "4F: HYPEREDGE ALGEBRA -- NOT APPLICABLE", "")
r = block(ws, 5, "Status", "N/A. F_N^derived_v2's relations R are ordinary (binary) bipartite "
          "relations; no hyperedge structure exists in this seed family to build an algebra from.", height=60)
SHEET_PREFIX += 1

# 008 Algebra Minimality
ws = new_sheet(f"{SHEET_PREFIX} NAB-008 Algebra Minimality")
write_title(ws, "MINIMALITY (Section 5)", "")
r = block(ws, 5, "Complexity measure K(A)", "K(A) := dim_C(A) (the algebra's complex vector-space "
          "dimension) -- the simplest well-defined, seed-independent measure available.", height=50)
r = block(ws, r, "A_seed^min", "Comm(D_F) is, by construction, the FULL centralizer -- the largest, "
          "not smallest, algebra commuting with D_F. It is nonetheless minimal in a different sense: "
          "it is the smallest algebra that (a) is generated purely from D_F with zero free "
          "parameters and (b) automatically satisfies first-order. No smaller non-abelian subalgebra "
          "was searched for or constructed this run.", height=110)
r = block(ws, r, "Uniqueness", "Comm(D_F) is a DETERMINISTIC function of D_F once a seed is fixed "
          "(unique per seed). Across DIFFERENT seeds, 56 distinct non-abelian instances exist with "
          "no internal invariant found this run that privileges one over another -- PROVEN NON-"
          "UNIQUE at the seed level (THM-NAB-010), consistent with every prior run in this project "
          "(Track A never selects a single canonical seed).", height=110)
SHEET_PREFIX += 1

# 009 Irreducible Representations
ws = new_sheet(f"{SHEET_PREFIX} NAB-009 Irreducible Reps")
write_title(ws, "IRREDUCIBLE REPRESENTATIONS (Section 6)", "")
rows = [("N=4 non-abelian seeds", "1, 1, 2", "11 seeds", "2"),
        ("N=5 non-abelian seeds", "1, 1, 3", "45 seeds", "3")]
write_table(ws, 5, ["Seed class", "block_dims (irrep dims)", "count", "smallest dim(V_i)>1"], rows, widths=[26,26,14,20])
r = 9
r = block(ws, r, "Selection criterion", "The defining/inclusion representation on H_F^bare=C^N is "
          "used -- selected because it is the UNIQUE faithful representation of A_seed compatible "
          "with the seed's own eigenspace decomposition at this dimension (each block occurs with "
          "multiplicity exactly 1 in every seed found; THM-NAB-003), not because of any physical "
          "target.", height=110)
SHEET_PREFIX += 1

# 010 Hilbert Space
ws = new_sheet(f"{SHEET_PREFIX} NAB-010 Hilbert Space")
write_title(ws, "H_F CONSTRUCTION (Section 7)", "")
r = block(ws, 5, "Construction", "H_F = C^N (+) C^N (particle (+) antiparticle), dim = 2N, N = the "
          "seed's own vertex count. NOT forced to 32 -- for N=4, dim H_F=8; for N=5, dim H_F=10.", height=70)
SHEET_PREFIX += 1

# 011 Left/Right Representations
ws = new_sheet(f"{SHEET_PREFIX} NAB-011 Left Right Reps")
write_title(ws, "PI_L / PI_R REPRESENTATION CANDIDATES (Section 8)", "predefined before testing")
rows = [(k, v["n_oz_pass"], v["n_fo_pass"], REP_REG["n_nonabelian_seeds_tested"]) for k, v in REP_REG["candidates"].items()]
write_table(ws, 5, ["Candidate", "order-zero pass", "first-order pass", "n tested"], rows, widths=[24,18,18,12])
r = 10
r = block(ws, r, "Finding", REP_REG["finding"], height=140)
SHEET_PREFIX += 1

# 012 Real Structure
ws = new_sheet(f"{SHEET_PREFIX} NAB-012 Real Structure")
write_title(ws, "J_F CONSTRUCTION (Section 9)", "")
r = block(ws, 5, "Construction", "Standard swap-conjugate J0, unchanged from ncg_bridge.py / "
          "SEMANTIC-FUNCTOR-BRIDGE-001: J[v,w]=[conj(w),conj(v)]. Not re-derived this run -- the "
          "algebra changed, J did not.", height=70)
r = block(ws, r, "KO-dimension", "Determined algebraically via KO_TABLE lookup against the doubling "
          "sign convention, exactly as in prior runs -- {0,6} mod 8, unaffected by A_seed's abelian/"
          "non-abelian status (THM-NAB-007).", height=80)
SHEET_PREFIX += 1

# 013 Dirac Operator
ws = new_sheet(f"{SHEET_PREFIX} NAB-013 Dirac Operator")
write_title(ws, "D_F CONSTRUCTION (Section 10)", "")
r = block(ws, 5, "Construction", "D_F = N_orient(R) + N_orient(R)^T, unchanged from every prior run "
          "-- derived purely from the seed's canonical orientation, zero free parameters, no Yukawa "
          "couplings, no observed masses. Every nonzero entry has direct seed-level provenance "
          "(R's own edges via N_orient).", height=110)
SHEET_PREFIX += 1

# 014 Grading
ws = new_sheet(f"{SHEET_PREFIX} NAB-014 Grading")
write_title(ws, "GRADING (Section 11)", "")
g = TRIPLE["grading"]
r = block(ws, 5, "gamma_F^2 = 1", str(g["gamma_F_squared_eq_1"]), height=30)
r = block(ws, r, "{gamma_F, D_F} = 0", str(g["anticommutes_with_D_F"]), height=30)
r = block(ws, r, "Holds", str(g["holds"]), height=30)
SHEET_PREFIX += 1

# 015 Order Zero
ws = new_sheet(f"{SHEET_PREFIX} NAB-015 Order Zero")
write_title(ws, "ORDER-ZERO -- FAILS UNIVERSALLY (Section 11)", "")
r = block(ws, 5, "Result", "0/56 non-abelian seeds pass, for all 3 representation candidates "
          "(identity, inner-automorphism, conjugate). Worst-case residual EXACTLY 1.0 in every "
          "case -- proven, not observed (THM-NAB-005 / THM-NAB-ORDER-ZERO-OBSTRUCTION-001).", height=90)
SHEET_PREFIX += 1

# 016 First Order
ws = new_sheet(f"{SHEET_PREFIX} NAB-016 First Order")
write_title(ws, "FIRST-ORDER -- HOLDS UNIVERSALLY (Section 11)", "first time in the entire investigation")
r = block(ws, 5, "Result", "56/56 non-abelian seeds pass, for all 3 representation candidates. "
          "Worst-case residual ~5e-16 (machine precision) in every case -- proven exactly, since "
          "elements of Comm(D_F) commute with D_F by definition (THM-NAB-006).", height=90)
SHEET_PREFIX += 1

# 017 KO Dimension
ws = new_sheet(f"{SHEET_PREFIX} NAB-017 KO Dimension")
write_title(ws, "KO-DIMENSION (Section 9/11)", "")
r = block(ws, 5, "Result", TRIPLE["KO_dimension"]["note"], height=90)
write_table(ws, 8, ["Convention", "KO class"], [("same_sign", TRIPLE["KO_dimension"]["same_sign_convention"]),
                                                  ("opposite_sign", TRIPLE["KO_dimension"]["opposite_sign_convention"])], widths=[20,14])
SHEET_PREFIX += 1

# 018 Faithfulness
ws = new_sheet(f"{SHEET_PREFIX} NAB-018 Faithfulness")
write_title(ws, "FAITHFULNESS (Section 11)", "")
r = block(ws, 5, "Result", "The defining/inclusion representation a |-> diag(a,a) is faithful by "
          "construction (a=0 is the only element mapping to the zero operator, since it's literally "
          "the inclusion A_seed subset M_N(C) embedded block-diagonally). Holds for every seed.", height=90)
SHEET_PREFIX += 1

# 019 Poincare Duality
ws = new_sheet(f"{SHEET_PREFIX} NAB-019 Poincare Duality")
write_title(ws, "POINCARE DUALITY -- DEFERRED (Section 11)", "")
r = block(ws, 5, "Status", TRIPLE["poincare_duality"]["reason"], height=110)
SHEET_PREFIX += 1

# 020 Orientability
ws = new_sheet(f"{SHEET_PREFIX} NAB-020 Orientability")
write_title(ws, "ORIENTABILITY -- DEFERRED (Section 11)", "")
r = block(ws, 5, "Status", TRIPLE["orientability"]["reason"], height=90)
SHEET_PREFIX += 1

# 021 Full Triple
ws = new_sheet(f"{SHEET_PREFIX} NAB-021 Full Triple")
write_title(ws, "COMPLETE FINITE TRIPLE -- WITNESS SEED SUMMARY", "")
rows = [
    ("grading", TRIPLE["grading"]["holds"]),
    ("hermiticity", TRIPLE["hermiticity"]["holds"]),
    ("order-zero (identical pi_R)", TRIPLE["order_zero_identical_pi_R"]["holds"]),
    ("first-order (identical pi_R)", TRIPLE["first_order_identical_pi_R"]["holds"]),
    ("poincare duality", "DEFERRED"),
    ("orientability", "DEFERRED"),
]
write_table(ws, 5, ["Axiom", "Result"], rows, widths=[36, 20])
SHEET_PREFIX += 1

# 022 Seed Sweep
ws = new_sheet(f"{SHEET_PREFIX} NAB-022 Seed Sweep")
write_title(ws, "FULL SEED SWEEP (Section 13)", "")
s = BRIDGE["this_run_summary"]
rows = [("n_seeds_total", s["n_seeds_total"]), ("n_nonabelian_seeds", s["n_nonabelian_seeds"])]
rows += [(f"n_seeds N={N}", s["n_seeds_by_N"][N]) for N in s["n_seeds_by_N"]]
rows += [(f"n_nonabelian N={N}", s["n_nonabelian_by_N"][N]) for N in s["n_nonabelian_by_N"]]
rows += [("order-zero pass fraction (given non-abelian)", s["given_nonabelian__order_zero_pass_fraction"]),
         ("first-order pass fraction (given non-abelian)", s["given_nonabelian__first_order_pass_fraction"]),
         ("both pass fraction (given non-abelian)", s["given_nonabelian__BOTH_pass_fraction"])]
write_table(ws, 5, ["Metric", "Value"], rows, widths=[42, 20])
SHEET_PREFIX += 1

# 023 Controls
ws = new_sheet(f"{SHEET_PREFIX} NAB-023 Controls")
write_title(ws, "CONTROL EXPERIMENTS A-G (Section 14)", "")
rows = []
for k, v in CTRL.items():
    note = v.get("note") or v.get("finding") or v.get("status") or ""
    rows.append((k, str(note)[:300]))
write_table(ws, 5, ["Control", "Finding (truncated)"], rows, widths=[45, 130])
SHEET_PREFIX += 1

# 024 Spectral Connection
ws = new_sheet(f"{SHEET_PREFIX} NAB-024 Spectral Connection")
write_title(ws, "SPECTRAL CONNECTION D_F^2 vs L (Section 18)", "")
r = block(ws, 5, "Result", "D_F is UNCHANGED from prior runs in this construction (only the algebra "
          "A_seed acting on H_F changed, not D_F itself) -- the prior run's exact result "
          "(ncg_df_laplacian_relation.json / test_D_F_squared_not_equal_laplacian) still applies "
          "directly: D_F^2 != L, verified exactly for all 28 seeds at N<=4, no shifted relation "
          "found. Not re-derived; cited as still valid since D_F's construction did not change.", height=140)
SHEET_PREFIX += 1

# 025 Gauge Comparison
ws = new_sheet(f"{SHEET_PREFIX} NAB-025 Gauge Comparison")
write_title(ws, "PHYSICAL TARGET COMPARISON (Sections 15-16) -- STRUCTURAL COMPARISON ONLY", "")
r = block(ws, 5, "Comparison", "A_seed at N=4 has one irrep of dim 2 (matches U(2)'s defining rep "
          "dimension only by coincidence of size, NOT SU(2): A_seed = C (+) C (+) M_2(C) is a "
          "direct sum with two abelian summands, not simple, and U(A_seed) is a compact Lie group "
          "of the WRONG type -- U(1) x U(1) x U(2), not SU(2)). At N=5, one irrep of dim 3 "
          "similarly gives U(1) x U(1) x U(3), not SU(3). Neither construction was targeted or "
          "tuned toward these groups; the comparison is reported ONLY because Sections 15-16 "
          "require it after independent derivation. VERDICT: STRUCTURAL COMPARISON ONLY, not a "
          "derived match -- no DERIVED MATCH claim is made.", height=200)
SHEET_PREFIX += 1

# 026 Theorem Registry
ws = new_sheet(f"{SHEET_PREFIX} NAB-026 Theorem Registry")
write_title(ws, "THEOREM REGISTRY (Section 12)", "")
rows = [(k, v["statement"][:200], v["status"]) for k, v in THM.items()]
write_table(ws, 5, ["Theorem", "Statement (truncated)", "Status"], rows, widths=[30, 130, 24])
SHEET_PREFIX += 1

# 027 Target Independence
ws = new_sheet(f"{SHEET_PREFIX} NAB-027 Target Independence")
write_title(ws, "TARGET-INDEPENDENCE FIREWALL SCAN (Section 21)", "")
rows = [(fp, str(v.get("clean"))) for fp, v in TI["files_scanned"].items()]
write_table(ws, 5, ["File", "Clean (0 forbidden hits)"], rows, widths=[65, 24])
r = 9
r = block(ws, r, "Note", TI["note"], height=110)
SHEET_PREFIX += 1

# 028 Closure Matrix (bridge-closure checklist)
ws = new_sheet(f"{SHEET_PREFIX} NAB-028 Closure Matrix")
write_title(ws, "BRIDGE-CLOSURE 14-POINT CHECKLIST (Section 19)", "")
rows = [
    ("1. non-abelian", "PASS -- 56/259 seeds"),
    ("2. seed-derived", "PASS -- Comm(D_F), zero free parameters"),
    ("3. irrep dim>1", "PASS -- dim 2 (N=4) / dim 3 (N=5)"),
    ("4. canonical representation selection", "PASS -- unique faithful rep, THM-NAB-003"),
    ("5. derived asymmetric L/R representation", "N/A -- proven irrelevant, THM-NAB-004"),
    ("6. seed-derived D_F", "PASS -- unchanged construction"),
    ("7. grading", "PASS"),
    ("8. Hermiticity", "PASS"),
    ("9. reality", "PASS (J0 unchanged, verified in phase2)"),
    ("10. order-zero", "FAIL -- universal, proven (THM-NAB-005/ORDER-ZERO-OBSTRUCTION-001)"),
    ("11. first-order", "PASS -- universal, proven (THM-NAB-006)"),
    ("12. faithfulness", "PASS"),
    ("13. Poincare duality", "DEFERRED (stop condition -- item 10 already failed)"),
    ("14. orientability", "DEFERRED (stop condition)"),
]
write_table(ws, 5, ["Checklist item", "Verdict"], rows, widths=[40, 90])
r = 21
r = block(ws, r, "Exact first failure", "Item 10: order-zero. Per Section 19, STOP here.", height=40)
SHEET_PREFIX += 1

# 029 Next Dependency
ws = new_sheet(f"{SHEET_PREFIX} NAB-029 Next Dependency")
write_title(ws, "EXACTLY ONE NEXT UNRESOLVED UPSTREAM DEPENDENCY (Section 28)", "")
ws["A4"] = BRIDGE["exact_first_unresolved_dependency"]
ws["A4"].font = Font(name="Arial", size=12, bold=True)
ws["A4"].alignment = WRAP
ws.merge_cells("A4:F4")
ws.row_dimensions[4].height = 260

wb.save(OUT)
print("saved", OUT)
print("total sheets:", len(wb.sheetnames))

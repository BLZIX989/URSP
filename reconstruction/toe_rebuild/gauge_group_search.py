"""
Record of the §5.11-mandated search for an independent gauge-group derivation
route (Clifford structures, commutants, Lie algebra recovery, module
decomposition, representation decomposition) across the full source corpus.
Not a computation -- a documented text search, kept as a script for
reproducibility (same methodology as prior runs' corpus searches).
"""
FINDINGS = [
    {"src": "SRC-006 SEIT Updated Whitepaper(1).docx", "row": 895,
     "quote": "Gauge group SU(3)xSU(2)xU(1) | Octonion/Spin(8) route | Open | Inclusion asserted, not derived; E8/SO(10) alternatives not ruled out"},
    {"src": "SRC-006 SEIT Updated Whitepaper(1).docx", "row": 918,
     "quote": "The Octonion/Spin(8) derivation requires proving the graph's Clifford structure matches this algebra -- alternatives (E8, SO(10), F4) are not yet ruled out"},
    {"src": "SRC-007 Theory of Everything - Status Report(1).docx", "row": 986,
     "quote": "The gauge group of the Standard Model...is an experimentally measured structure, not a derive[d]..."},
    {"src": "SRC-008 UCG Specification v5(1).docx", "row": 1421,
     "quote": "THM-ANOM | G_SM = SU(3)xSU(2)xU(1) derivation | DER-QR-006 | CERTIFIED",
     "note": "The ONLY document in the entire corpus asserting CERTIFIED status for this specific claim. Oldest/earliest document among the five found; explicitly superseded by SRC-013/014 below."},
    {"src": "SRC-013 SEF SIT Specification v2.docx (self-labeled 'Post-Audit Revision')", "row": 2394,
     "quote": "The claim that Aut(G)'s commutant on Spec(L) generically yields (3,2,1)-type degeneracy -> SU(3)xSU(2)xU(1) is empirically rejected: 0/200 random block-model graphs produced the pattern"},
    {"src": "SRC-013 SEF SIT Specification v2.docx", "row": 2447,
     "quote": "Gauge embedding choice (AX2) | Selects G=Aut(K)xSpin(8) over alternatives | Input, not derived -- stated openly per Section 5"},
    {"src": "SRC-014 Audit and Recommended Revisions.docx", "row": 2534,
     "quote": "Commutant/Schur gauge extraction, End(E_lambda)=M_m(C)->U(m) | Not generic: 0/200 random block models hit (3,2,1); Cayley graphs give dim(rho)^2, not dim(rho)"},
    {"src": "SRC-014 Audit and Recommended Revisions.docx", "row": 2550,
     "quote": "(3,2,1)->SM gauge group via graph automorphism | Drop the graph-automorphism route. Officially adopt the Spin(8)/octonion route...input, not derivation"},
]

CONCLUSION = (
    "Search performed per Section 5.11's own instruction list (Clifford structures, commutants, "
    "Lie algebra recovery, module decomposition, representation decomposition, stabilizers). "
    "Result: FOUR independent documents (SRC-006, SRC-007 -- the project's own official Status "
    "Report --, SRC-013, SRC-014), spanning the project's own most careful internal audits, "
    "concur that the Standard Model gauge group is NOT derived from graph/spectral structure in "
    "this corpus -- it is variously described as OPEN, 'asserted not derived,' empirically "
    "rejected (0/200 trials, cited independently in two separate documents), or explicitly "
    "relabeled an INPUT axiom (AX2). Exactly ONE document (SRC-008, the earliest, a v1 DER "
    "Registry) claims CERTIFIED status for this specific claim, and it is the SAME claim every "
    "later document explicitly retracts. No 'Route B' -- no alternative Clifford/commutant/Lie-"
    "algebra derivation distinct from the already-rejected automorphism route -- was located "
    "anywhere in the accessible corpus."
)

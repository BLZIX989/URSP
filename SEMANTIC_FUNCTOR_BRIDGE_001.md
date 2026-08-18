# SEMANTIC-FUNCTOR-BRIDGE-001

**Run date:** 2026-08-18 (seventeenth closure run, continuing from the ARBS-retirement investigation)
**Objective:** build `OPEN-024` — the bridge both threads (this session's graph/ARBS work and the
newly-found NCG workbook) independently flagged as missing, connecting Track A's finite relational
seed to Track B's finite noncommutative-geometry spectral triple.
**Executable code:** `reconstruction/toe_rebuild/compiler/ncg_bridge.py`,
`reconstruction/toe_rebuild/run_bridge.py`

## Result: a real, partial bridge — with a precisely diagnosed obstruction, not a dead end

A genuine, non-arbitrary construction was built taking any seed `R ∈ F_N^derived_v2` (Track A) to a
candidate finite spectral triple (Track B), using **only** objects Track A had already derived
(`R`'s own `TH-ARBS-001A` bipartition, its own canonical orientation `N_orient(R)` from run 15) and
**only** constructions Track B's own workbook documents as standard (the particle+antiparticle
doubling from sheet `171_V2_CALC_018_RIGHT_REP_J`). No Standard-Model-specific content — no
hypercharges, no 3 generations, no `dim=32` — entered anywhere; every test used a generic maximal
abelian algebra, the same class of minimal candidate the NCG workbook itself uses for its own closed
"2-point test model" baseline.

**Tested exhaustively over all 259 candidates across every `N` this project has enumerated (2, 3, 4,
5):**

| Axiom | Result |
|---|---|
| Grading + Hermiticity + off-diagonality (Phase 1) | **100% pass**, all 259 |
| Real structure lands in a definite KO-dimension class (Phase 2) | **100% consistent**: KO=0 (same-sign doubling) or KO=6 (opposite-sign doubling), never any other of the 8 possible classes |
| Order-zero condition, generic abelian algebra (Phase 3) | **100% pass**, all 259 |
| First-order condition, generic abelian algebra (Phase 3) | **0% pass** — universal failure |

## The 100% consistency is itself the finding — and it's proven, not just observed

Every one of these four results is **identical across all 259 seeds**, at every `N`. That uniformity
was the signal to check whether they're facts about the *construction method* rather than about which
graph was chosen — and hand-derivation, then direct computational verification, confirms they are:

- **Order-zero passes trivially** because representing the algebra identically on both
  particle/antiparticle copies forces `J·π(b)·J⁻¹ = π(b)` *exactly* (verified to machine precision),
  reducing order-zero to `[π(a),π(b)]=0` — automatic for any diagonal algebra, for any `R`.
- **First-order fails whenever `D_F≠0`.** With that same identity, first-order reduces to requiring
  `[D_F,π(a)]` to itself be diagonal for every generator `a` — which forces `D_F=0` entirely (verified
  directly: an artificial `D_F=0` control case makes first-order hold trivially). Every genuine seed
  in `F_N^derived_v2` has `D_F≠0` (a `Γ`-fixed relation with `N≥2` always has edges), so first-order
  **cannot** hold under this specific combination, for *any* seed, at *any* `N` — a general theorem,
  not a per-graph accident.

## Why this is a real result, not a failure to be patched over

This mirrors — rather than contradicts — how the actual physical NCG construction works. The NCG
workbook's own axioms (`OZ-001`: *"H_F components are A_F-A_F^op **bimodules**"*, not a single
undifferentiated representation) already require the particle and antiparticle sectors to carry
**different** representations of the algebra, not identical copies. This run's bridge used the
simplest possible doubling (identical copies) precisely to get a first, honest, minimal-assumption
answer — and that answer is that the simplest version structurally cannot work, for a provable reason,
independent of which seed is chosen. This is exactly the outcome the project's own discipline calls
for: a real obstruction, precisely located, not smoothed over and not used as an excuse to invent a
patch.

## What this does and doesn't establish

**Does:** a principled, checkable, non-fabricated connection exists between Track A and Track B at the
structural (grading/reality) level, landing in specific, well-defined KO-dimension classes. This is
more than either thread had before — genuinely new, if modest, ground.

**Doesn't:** discriminate between different admissible seeds (all 259 give identical answers), and
doesn't yet satisfy the full finite-triple closure (first-order fails universally under this specific
construction).

## Next dependency

> Build a bridge variant with **genuinely asymmetric** left/right (or particle/antiparticle)
> representations — e.g. a contragredient/conjugate representation on the second copy rather than an
> identical one — and re-test order-zero/first-order. This follows directly from the NCG workbook's
> own bimodule requirement (`OZ-001`); it is not a new axiom invented to force closure, and it was not
> attempted this run given the scope already covered.

## Artifacts

`reconstruction/uoc_semantic_functor_bridge.json` (full results and proofs),
`reconstruction/toe_rebuild/compiler/ncg_bridge.py` (executable construction),
`reconstruction/toe_rebuild/run_bridge.py` (driver, reproducible: `python3 run_bridge.py`).

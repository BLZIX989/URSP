# ARBS-GRAPH-REALIZATION-001

**Run date:** 2026-08-18 (eleventh closure run, continuing from `ARBS-ONTOLOGY-RECOVERY-001.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.0.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.1.xlsx`

## Result: OBSTRUCTION — but a more precisely characterized one than "unknown"

`G_ARBS` — the specific graph the source's shell-1 node `G=(V,E,W)` is supposed to name — **cannot
be uniquely reconstructed from source.** Per this run's own stop condition, that's where the
identity/realization question ends. But the search surfaced two things worth keeping: a genuine,
checkable partial-compatibility result for `tilde_G_k`, and a much sharper picture of *why* the
checkpoint numbers line up.

## A–D. Exact source definition of `G=(V,E,W)`

Every occurrence traced to its full context:

- **`BRIDGE B-001`** (CERTIFIED): *"Given `G=(V,E,W)`, the Laplacian `L=D−A` is uniquely defined..."*
  — conditional on `G` already existing; doesn't construct it.
- **Variable Registry** (3 copies): *"`V`=entities/states; `E`=relations; `W`=relation-strengths.
  `A_ij=w_ij`"* — a semantic schema (what the letters mean), not an instantiation (what the actual
  vertices/edges/weights are).
- **`Graph_ARBS`** (UCG Specification v5, `RF-001`): *"Finite typed weighted hypergraphs
  `G=(V,E,W,σ)` satisfying `TH-ARBS-001A` and `TH-ARBS-001B`"* — this is the closest thing to a
  formal specification anywhere in the corpus, and it names a **category** of admissible graphs
  constrained by two axioms, not a single member.

**Conclusion: `V`, `E`, `W` are defined only semantically, everywhere they appear.** No concrete
vertex list, edge list, or weight formula exists in source.

## E–G. Bipartition, dependency, hypergraph relation

`TH-ARBS-001A` (Bipartite Reciprocity Lock) and `TH-ARBS-001B` (Shell Nilpotency Lock) are the only
two *concrete, checkable* constraints the source actually supplies. Tested against `tilde_G_k`:

- **`TH-ARBS-001A`**: `V` splits into two parts with edges only crossing between them. **SATISFIED**
  — `tilde_G_k`'s global partition `∪L_k` vs `∪R_k` is a valid 2-coloring for every edge, confirmed
  again this run.
- **`TH-ARBS-001B`**: a directed transport matrix, oriented by non-decreasing shell index, must be
  nilpotent. **SATISFIED** — orienting every edge from its lower to higher canonical vertex index
  (the natural construction order) gives a nilpotent directed adjacency matrix for every tested
  shell, with nilpotency index `2k+1` for `G_k`.

No hypergraph-to-graph projection map was found anywhere (consistent with
`ARBS-ONTOLOGY-RECOVERY-001`) — this piece stays OPEN.

## H. Canonical Laplacian

`BRIDGE B-001`'s `L=D−A` is a *general* fact about any graph fitting the schema — not evidence of an
ARBS-specific operator. No alternative (hypergraph Laplacian, typed operator) was found. Consistent
with (not proof of) `L_k=D_k−A_k` remaining the right operator *for `tilde_G_k` specifically*.

## I. Relation between `G_ARBS` and `tilde_G_k` — admissible, not identical

**`tilde_G_k` is not an arbitrary, structurally unrelated graph** — it satisfies both of ARBS's own
concrete admissibility axioms, verified computationally this run. That's real, positive, non-trivial
evidence. But `Graph_ARBS` names a whole *category* of graphs meeting those two axioms — satisfying
them doesn't select `tilde_G_k` uniquely, and no comparison against an actual `G_ARBS` is possible
because none exists to compare against.

A second, independent construction attempt was also found and reviewed: the SIT specification's
`Δ→G` completion (`K_ij` compatibility kernel, optimized selector). It has two explicitly unfixed
free parameters (`λ_C`, `θ`), and — this is the important part — **the source's own empirical test of
its unconstrained limit explicitly states it "converges to near-complete graph, not the claimed
Recursive Bipartite Shell Graph."** This doesn't just fail to help `tilde_G_k`'s case; it confirms
that no clean, parameter-free construction of `G` exists anywhere in the corpus, from any approach
that was actually tried.

## J. Why the checkpoints match

Ruled out: **A/B** (no canonical graph to be identical to or realize). **C** (no projection map
exists). Best-supported answer is a **blend of D and E, more precisely than either alone**: the
checkpoint *values* (`σ16`, `σ17`, `t_H`, ...) were already present in this project's own workbook
history *before* the `K_{2^k,2^k}` construction rule was ever supplied — consistent with an origin
independent of that rule (Outcome E). The rule itself, once supplied and independently implemented
with no checkpoint values in the construction code, reproduced 8 independent checkpoints to
double-precision *and* satisfies both admissibility axioms — stronger than pure coincidence (Outcome
D), but short of proof. The true origin of the original numbers predates what this source corpus
documents, and isn't recoverable from it.

## K. Reclassification

No change to the table built in `ARBS-ONTOLOGY-RECOVERY-001` (workbook sheet 158) — every run 1–9
result stands, unchanged, valid as a `tilde_G_k`-level fact. This run adds one nuance: `tilde_G_k` is
now known to be an *admissible* member of the `Graph_ARBS` category, which is stronger compatibility
evidence than was available before, still short of identity.

## L. Corrected MDCL

```
Γ ≺ ARBS ≺ ARBS shell 1 ≺ G_ARBS [OBSTRUCTION -- only a category (2 axioms) is specified]
                                  ≺ L_ARBS [OPEN] ≺ Spec(L_ARBS) [OPEN]

separately, unchanged and fully valid:
tilde_G_k [ADMISSIBLE member of Graph_ARBS, VERIFIED] ≺ tilde_L_k=D_k-A_k ≺ Spec(tilde_L_k)
                                  ≺ [everything computed in runs 1-9]
```

No proven map connects the two chains — `G_ARBS`'s obstruction means the map's domain isn't even
defined yet.

## M. Closure matrix

| Object | Status |
|---|---|
| `G_ARBS=(V,E,W)` concrete instantiation | **OBSTRUCTION** — not source-supported |
| `Graph_ARBS` category + 2 admissibility axioms | **DERIVED/VERIFIED** |
| `tilde_G_k` satisfies `TH-ARBS-001A` | **VERIFIED** |
| `tilde_G_k` satisfies `TH-ARBS-001B` | **VERIFIED** |
| `tilde_G_k = G_ARBS` (identity) | **NOT ESTABLISHED** — no target exists to compare against |
| SIT `Δ→G` alternative | Reviewed — unfixed params, explicitly fails per source's own test |
| Checkpoint origin | Assessed (blend of D/E); not provable to certainty |
| Runs 1–9 numerics | **PRESERVED, VALID** as `tilde_G_k`-level facts |
| `σ_k`, `Π₀`, `G*`, NCG, flavor, scale | **UNTOUCHED** |
| `PACKET-REFINEMENT-RECOVERY-001` | **NOT ACTIVATED** |

## N. Exactly one next unresolved upstream dependency

> **Recover, from admissible source material not yet located (or genuinely new derivation, not
> invention), a concrete instantiation of `V`, `E`, and `W` for ARBS shell 1's `G` node — OR obtain
> independent, out-of-band documentation establishing the actual origin of the historical spectral
> checkpoints this project has reproduced since its first run.** Neither is resolvable by further
> reading of the currently available corpus, which has now been searched exhaustively for this exact
> question across three consecutive runs.

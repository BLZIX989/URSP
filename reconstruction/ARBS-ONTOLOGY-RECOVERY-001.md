# ARBS-ONTOLOGY-RECOVERY-001

**Run date:** 2026-08-18 (tenth closure run, continuing from `C004I_report.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.9.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.0.xlsx`

## Bottom line

**ARBS, as actually documented in source, is not the graph I've been computing.** It is the
project's own meta-level derivation-pipeline hypergraph — 8 fixed organizational shells running from
`Ω` (Primitives) to Emergent Structures — not a combinatorial graph whose spectrum gets analyzed. The
`K_{2^k,2^k}`/`R_{k-1}×L_k` bipartite-shell graph (`G_k`) computed throughout runs 2–9 is a real,
correctly-verified, self-contained mathematical object, but it has never been shown — by any source
document — to be a realization, projection, or instance of the documented ARBS object. **This is
Case D.**

## A. Exact recovered meaning of ARBS

Found verbatim (`54_SOURCE_TEXT_CORPUS`, rows 1924–2088, part of a "Universal Persistence Graph"
specification): *"The Abelian Recursive Bipartite Shell Typed Dependency Hyper-Graph (ARBS) is the
organizational substrate in which the canonical spine operates. It has four structural properties
that together define it uniquely: Abelian operator composition within shells, recursive self-similar
construction, bipartite separation of objects and operators, and typed dependency edges."*

## B. The full ARBS object

`𝓐 = (N_obj, N_op, E_typed[9 types], H[hyperedges, arity≥3], τ: N→{Object,Operator}, shell:
N→{0,...,7}, feedback: Π₀→G)`. Assembled entirely from recovered source components (below) — nothing
invented from the acronym.

## C. Abelian — exact meaning

`A∘B = B∘A` when `A,B` act on independent subspaces or shells, `[A,B]=0` — **explicitly regional, not
global.** Source-listed examples: heat semigroups `e^{-tL}`, Laplacian powers `L^k`, spectral
projections — all standard functional calculus on a single operator, hence trivially commuting (I
verified this is a general fact, applicable to my own already-computed `L_k` operators too, not
something specific to a "true" ARBS graph). Non-Abelian region: nonlinear dynamics, external forcing,
cross-shell interaction. **`THM-ARBS-ABELIAN-001`: DERIVED/VERIFIED for the stated operator families.**

## D. The recursive operator — not what I've been computing

This is the single most important correction. ARBS's recursion is **feedback**, not growth:
*"The persistence functional `Π₀` at the `k=6` layer feeds back to constrain the organizational graph
`G` at `k=1`, which modifies `L`, which modifies `Spec(L)`, which modifies `Π₀`... Organizational
structures persist because they satisfy the fixed-point condition: `Π₀[G*]` is maximized."* This is a
**fixed-point condition over a fixed 8-stage structure**, not a sequence `G_0⊂G_1⊂G_2⊂...` of
ever-larger graphs. `THM-ARBS-RECURSION-001`: DERIVED/VERIFIED as documented — and explicitly **not**
the mechanism `G_k`'s construction implements.

## E–F. Bipartite/Shell — the naming collision that explains everything

Recovered the complete 8-shell registry table:

| k | Layer | Primary objects |
|---|---|---|
| 0 | Primitives | `Ω, Δ` |
| 1 | Discrete Organization | `G=(V,E,W)` — **the entire graph is ONE node here** |
| 2 | Spectral/Analytical | `L, Spec(L), H(t), δ_spec` |
| 3 | Continuum Geometry | `g_μν, Γ, Δ_M, R_ab, G_ab` |
| 4 | Dynamics/Probabilistic | `ℒ, ℒ*, T_e, F[P‖P_ss]` |
| 5 | Thermodynamic/Info | `P_ss, T_ab, σ` |
| 6 | Persistence | `Π₀, λ_FP` |
| 7 | Emergent Structures | Life, Chemistry, Mind, Galaxies... |

**ARBS's "shell index k" indexes stages of this project's own derivation pipeline** — literally the
`Γ≺ARBS≺G≺L≺Spec(L)≺...≺Π₀≺G*` chain referenced throughout every run since run 1. It is *not* a
combinatorial recursion depth. `G_k`'s "shell" (`S_k=L_k⊔R_k`, growing without bound) shares only the
word with ARBS's shell — the entire graph `G_k` for any single `k`, if anything, could only ever be a
*candidate value* for the ONE node "G" at ARBS's shell `k=1`, never a stand-in for ARBS's shell
structure itself. This single naming collision (word "shell," letter "k," used for two unrelated
indices) is the most likely root cause of the entire `ARBS=G_k` identification tested across 8 prior
runs.

Bipartition: ARBS splits nodes by **semantic role** (Object vs. Operator — states/entities vs.
maps/functions). `G_k` splits vertices by **structural position** (`L_j` vs. `R_j` within a shell) —
no semantic content at all. Different kinds of bipartition, never shown to correspond.

`K_{2^k,2^k}`/`R_{k-1}×L_k` never appears anywhere in the ARBS Hyper-Graph Architecture section —
confirmed again this run, consistent with every prior provenance search.

## G. Type system

Full taxonomy recovered: 2 node types (Object, Operator); 9 edge types — **Dependency**, **Creates/
Generates**, **Transforms**, **Constrains**, **Measures/Spectral**, **Mapping/Functor** (the 6
"primary" types), plus **Feedback** and **Projection** (the stated "+2"), plus **Hyperedge**
(diamond, arity≥3, "Preserves Measure"). Each with documented color, direction, and semantics
(source rows 2064–2073). `G_k` realizes **zero** of these 9 types and **zero** of the 2 node types —
its single undifferentiated edge relation (`A_ij∈{0,1}`, symmetric) doesn't correspond to any of them.

## H. Dependency relation

ARBS's "Dependency" edge (`A→B`: "B uses or requires A") **is** the `≺` relation used throughout this
whole project's MDCL. Governed by the `SDR` axioms (CERTIFIED elsewhere in corpus): irreflexive,
transitive, acyclic — a strict partial order / DAG. `G_k`'s edges are **symmetric** graph adjacency
(`A_ij=A_ji`) — structurally incompatible with an asymmetric strict order. `G_k`'s adjacency and
ARBS's dependency relation are different mathematical objects serving different purposes.

## I. Hypergraph structure

`ARBS HYPER-001`: canonical form `ℋ:(A,B,C)→D`, arity 3, generalizes to arity `k`, certified property
"Preserves Measure" (consistency with `P_ss`). The source's own stated point is that this captures
genuinely irreducible multi-input dependencies — not expressible as pairwise edges without losing the
joint-necessity condition. `G_k`, an ordinary simple graph, cannot represent this at all — confirmed
by inspecting the construction code: no arity-≥3 relation exists anywhere in `build_arbs.py`.

## J. What the projection loses

Moot — **no realization map `ARBS→G_k` was ever defined**, so there is nothing to analyze the losses
of. Recorded honestly as "not applicable, no map exists" rather than answering hypothetically.

## K. Is the graph spectrum genuinely an ARBS consequence?

ARBS's shell `k=2` just says "take whatever `G` occupies shell `k=1` and apply `BRIDGE B-001`
(`G→L`, CERTIFIED) then `B-002` (`L→Spec(L)`, CERTIFIED)." Both bridges are stated for an *arbitrary*
graph — the mechanics are certified regardless of input. What's not established is that `G_k` is the
`G` ARBS's shell `k=1` refers to. So: **`GRAPH_SPECTRUM_VERIFIED = true`** (unquestionably, for the
explicit `G_k`); **`ARBS_SPECTRAL_DERIVATION = OPEN`** (no `G` has been sanctioned as ARBS's own
choice).

## L. Reclassification of every prior result

**Every single numerical result from runs 1–9 is preserved, unchanged, and remains fully valid** — as
a fact about `G_k`. Full table in `arbs_prior_result_reclassification.json` / workbook sheet 158.
Nothing is deleted, nothing is renumbered, no calculation is wrong. Only the label changes: "ARBS
result" → "`G_k` result, ARBS-level interpretation OPEN pending a realization map." This includes
`ARBS-CONSTRUCTION-001`, `ARBS-FULL-SPEC-001`, `σ16/σ17`, `t_H`, `λ_c`, `P_H`, `N_H`, the diffusion
metric, effective resistance, the diameter results, and C-004B through C-004I in full.

## M. Corrected dependency chain

```
Γ ≺ ARBS [8-shell typed dependency hypergraph, feedback-recursive, DOCUMENTED]
     ≺ shell-1 Object Node "G=(V,E,W)" [UNSPECIFIED which G]
     ≺ ??? [NO PROVEN MAP] ???
     ≺ G_k [explicit bipartite-shell graph — well-verified, self-contained, CASE D]
     ≺ B_k ≺ L_k ≺ D_{G_k} ≺ Spec(L_k) ≺ [everything computed in runs 2-9, all valid as G_k-facts]
```

## N. Closure matrix

| Object | Status |
|---|---|
| ARBS ontology | **DERIVED/VERIFIED** — fully documented in source |
| ARBS ↔ `G_k` relationship | **CASE D** — reproduces checkpoints, not a proven realization |
| Abelian, Recursive, Bipartite, Shell, Typed, Dependency, Hypergraph | Each **DERIVED/VERIFIED for ARBS**; each **PROVEN INCOMPATIBLE / FALSIFIED as realized by `G_k`** |
| Realization map `ARBS→G_k` | **Does not exist** |
| All runs 1–9 numerics | **Remain valid**, reclassified as `G_k`-level facts |
| `σ_k`, `Π₀`, `G*`, NCG, flavor, scale | **Untouched**, per stop condition |
| `PACKET-REFINEMENT-RECOVERY-001` | **Not activated** — not required by this run's findings |

## O. Exactly one next unresolved upstream dependency

> **Recover or derive, from admissible source material only, a construction rule or realization map
> for the single Object Node `G=(V,E,W)` that occupies ARBS's shell `k=1`** — determine what specific
> graph (if any is ever named beyond the abstract symbol `G`) the documented ARBS architecture
> actually intends, OR formally establish, with genuine source support (not checkpoint reproduction,
> not directive text asserting recovery), that `K_{2^k,2^k}`/`R_{k-1}×L_k` (`G_k`) is an admissible
> choice for that node. Until this exists, every downstream result computed throughout this project
> remains correctly interpreted as a `G_k`-level fact only — valid, verified, and preserved — but not
> a conclusion about the ARBS object actually documented in source. This is the exact point at which
> the entire multi-run derivation chain currently terminates.

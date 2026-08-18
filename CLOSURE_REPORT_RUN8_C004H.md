# C-004H — ARBS Continuum Compatibility Recovery

**Run date:** 2026-08-18 (eighth closure run, continuing from `CLOSURE_REPORT_RUN7_C004G.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.7.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.8.xlsx`

## The headline: a genuinely new, positive finding — but not a full resolution

C-004G tested ARBS against the source's continuum-refinement axioms using the unit-edge hop-count
metric and found outright incompatibility (unbounded diameter, forced `α=1`). That metric was never
actually labeled canonical in source — it was simply the default choice. Re-running the source
exhaustion search this time against the **certified** metric object turns up something C-004G missed:

**`d(i,j) = diffusion distance`** — `DER-GEO-005`, `CERTIFIED`, also `ENG-011` in the original
Calculation Engine, cross-referenced as "`Spec(L) → diffusion distance → metric`" dozens of times
across every workbook in the corpus. This is exactly the kind of "spectral metric" Section 6 asked
me to test, and it was sitting in source the whole time, untested against ARBS specifically until
now. (Effective resistance, also source-referenced, turns out to be the same quantity —
`R_eff(i,j) = d(i,j)²` exactly, verified to `~1e-12` residual — not independent evidence.)

## Testing it: diameter bounded, metric invariance asymptotic (not exact)

**Diameter.** Computed the diffusion-distance diameter for G0–G8:

| Shell | Diffusion diameter |
|---|---|
| G0 | 1.0000000000 |
| G1 | 1.4142135624 |
| G2 | 1.4577379737 |
| G3 | 1.4469796128 |
| G4 | 1.4334181176 |
| G5 | 1.4288690166 |
| G6 | 1.4288690166 |
| G7 | 1.4288690166 |
| G8 | 1.4288690166 |

**Bounded and convergent** — four shells in a row identical to 10 decimal places. Sharp contrast with
C-004G's hop metric, which is *exactly* unbounded (`diam=2n+1`).

**Induced Metric Invariance.** Tested `d_{k+1}(v_i,v_j) = d_k(v_i,v_j)` for old-vertex pairs under the
same inclusion map. It does **not** hold exactly — but the violation shrinks geometrically:

| Transition | Max violation | Ratio (prev/curr) |
|---|---|---|
| G1→G2 | 0.42265 | — |
| G2→G3 | 0.29886 | **1.41421356...** |
| G3→G4 | 0.21132 | **1.41421356...** |
| G4→G5 | 0.14943 | **1.41421356...** |
| G5→G6 | 0.10566 | **1.41421356...** |
| G6→G7 | 0.07471 | **1.41421356...** |
| G7→G8 | 0.05283 | **1.41421356...** |

The ratio is `√2`, exactly, to 10+ significant figures, six transitions running. The violation is
converging to zero geometrically. This is strong, clean numerical evidence — not a formal proof (no
closed-form asymptotic derivation of the ARBS spectral family is attempted here, consistent with the
instruction not to introduce new continuum machinery) — but far more than "unresolved."

## Why this doesn't close C-004H outright

Two things this run does **not** get to override:

1. **The source's own stated mechanism still doesn't apply.** Primal Edge Scaling needs `R(e)` — a
   set of child edges replacing a parent edge. ARBS still doesn't do that (C-004G, unaffected: old
   edges are carried over completely unchanged). So even though the diffusion metric *behaves* as if
   a limit exists, that behavior isn't licensed by the source's own derivation route for such limits.
2. **The measure still doesn't converge — and this is metric-independent.** C-004F's finding (total
   variation between `(ρ_k)_*π_k` and `π_{k+1}` stabilizing at a fixed ~0.625, not vanishing) doesn't
   depend on which metric is used to talk about distances — it's a statement about the *combinatorial*
   inclusion map and the degree measure alone. **A convergent metric-measure space needs both pieces
   together.** Geometric convergence of the diffusion distance, however clean, doesn't supply a
   convergent measure for the thermodynamic branch specifically.

## Componentwise result (THEOREM C-004H.9)

| Component | Result |
|---|---|
| Edge scaling (Primal Edge Scaling) | **PROVEN INCOMPATIBLE** (unchanged, C-004G) |
| Diameter Stability | **SATISFIED** under the diffusion metric (strong numerical evidence); FALSIFIED under the hop metric |
| Induced Metric Invariance | **ASYMPTOTIC ONLY** under the diffusion metric (clean geometric rate, not exact); fails under any metric preserving old structure verbatim |
| Measure convergence | **PROVEN NON-CONVERGENT** (unchanged, C-004F) — metric-independent |
| Dirichlet form self-consistency | **DERIVED/VERIFIED** (unchanged, C-004F.4) |

**Neither `THEOREM C-004H.9` nor its impossibility form `C-004H.9-F` is promoted.** The honest result
is the componentwise ledger above: genuinely promising on the geometric side (a real, positive
correction to C-004G's scope), still proven non-convergent on the measure side.

## Architectural boundary (per Section 12, unchanged in kind, updated in detail)

- **ARBS = VERIFIED FINITE SPECTRAL SUBSTRATE.** Unaffected, still true.
- **ARBS ≠ VERIFIED CONTINUUM-GENERATING REFINEMENT.** Still true, but now with more nuance: the
  geometric obstruction is weaker than previously shown (a certified metric with promising
  convergence behavior exists), while the measure/thermodynamic obstruction stands exactly as before.
  ARBS is not modified in response to either finding.

## Falsification ledger addition

The unit-edge hop metric tested in C-004G is not retracted — its math is correct for the metric it
tested. But this run establishes it was never the source's own preferred metric for this question;
the diffusion distance is, and behaves qualitatively differently. Recorded as a methodological
correction to scope, not an error in C-004G's arithmetic.

## Target-independence audit

All new objects (diffusion/resistance matrices, diameter trend, invariance-violation trend) are
functions of `(k, L_k)` alone via its spectral decomposition — no reference to `32`, `N_H`, `H_F`,
`D_F`, `J_F`, `γ_F`, `Y_u`, `Y_d`, `Y_e`, `Y_ν`, `V_CKM`, `U_PMNS`, or `Ξ_obs`. **PASS.**

## Exactly one next unresolved upstream dependency

> **Formally prove — not merely numerically demonstrate — that the diffusion-distance metric
> sequence `(V_k,d_k)` is Gromov–Hausdorff convergent.** This requires an asymptotic spectral
> analysis of the ARBS Laplacian family (proving, analytically, that `λ_1(L_k)` and the relevant
> eigenvector overlaps converge at the empirically observed `√2`-geometric rate, rather than only
> confirming it for `k≤8`). **Independently, find or derive a renormalized measure sequence — distinct
> from the raw degree measure `π_k`, which is proven not to converge — that does converge under the
> same refinement map**, since a full metric-measure (measured Gromov–Hausdorff) limit needs both
> pieces together. Neither can be advanced by further reading of currently available source material;
> both require new mathematical derivation beyond what exists in the corpus.

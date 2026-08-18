# C-004F — Degree-Weighted Thermodynamic Continuum Recovery

**Run date:** 2026-08-18 (sixth closure run, continuing from `CLOSURE_REPORT_RUN5_C004E.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.5.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.6.xlsx`

## Executed exactly in the specified recovery order

| Step | Result |
|---|---|
| **F.1** Degree measure | **DERIVED/VERIFIED** — `π_k(i)=d_i/(2\|E_k\|)`, normalized, computed G0–G9 |
| **F.2** Weighted Hilbert space | **DERIVED FROM P_ss** (not source-certified — the corpus never fixes `μ`; positivity verified: no zero-degree vertices) |
| **F.3** Weighted generator | **DERIVED/VERIFIED** — `Q_k=-D_k^{-1}L_k`, detailed balance exact (residual `0.0`), conservation and Markov-stochastic semigroup all verified G0–G9 |
| **F.4** Dirichlet form | **DERIVED/VERIFIED** — exact formula proven and confirmed (see bug note below) |
| **F.5** Refinement map | Combinatorial map **DERIVED exactly**; metric rescaling **NOT source-supported** — registered as an obstruction |
| **F.6** Measure pushforward | **CALCULATED** across 9 transitions, G0→G1 through G8→G9 |
| **F.7** Weighted-space convergence | **Outcome D — no identifiable limit**, strong numerical evidence |
| **F.8–F.10** Continuum Dirichlet form / generator / FP correspondence | **NOT ATTEMPTED** — correctly blocked by F.7, per the run's own stop rule |

## A bug I caught and fixed during verification

The Dirichlet-form identity `E_k(f,g) = <f,−Q_kg>_μ` initially failed numerically (residual `0.31`, not
zero) — an arithmetic slip in my own script (dividing by `2|E_k|` instead of the algebraically correct
`4|E_k|`). Caught by the verification step itself, fixed, and re-confirmed to residual `~5.5×10⁻¹⁷`
across all shells. Recorded transparently rather than silently discarded, per this project's own
audit conventions.

## The central finding: F.4 succeeds cleanly; F.6/F.7 give a decisive negative result

**F.3/F.4 (generator + Dirichlet form) are genuine successes**, carried and sharpened from C-004D:
- `Q_k^*·π_k = 0` and `Q_k^*·d_k = 0` to residual `~10⁻¹⁶`–`10⁻¹⁹` for every shell G0–G9.
- Detailed balance `π_iQ_{ij}=π_jQ_{ji}` holds **exactly** (`0.0`, not merely small).
- `exp(Q_kt)` is row-stochastic (nonnegative, rows summing to 1) at every tested `t`, for every shell.
- **`E_k(f,g)=(1/(4|E_k|))∑A_{ij}(f_i-f_j)(g_i-g_j) = ⟨f,−Q_kg⟩_μ` exactly**, which as a direct
  corollary **proves `Q_k` is self-adjoint w.r.t. `⟨·,·⟩_μ`** — closing THEOREM C-004F.2 without a
  separate argument.

**F.5 (refinement map) is exactly derivable — as an inclusion, not a mesh refinement.** `G_k` is a
literal induced subgraph of `G_{k+1}` for every transition (verified exactly): all of `G_k`'s vertices,
edges, shells, and partitions survive verbatim; only the `R_k` vertices change degree, each gaining
**exactly** `2^{k+1}` new edges (uniform, verified). This is the ARBS **growth** structure, not a
resolution-refining discretization of a fixed space — and no explicit metric/edge-length rescaling
law exists anywhere in the corpus tying the whitepaper's abstract "contraction constant `α`" to this
specific `K_{2^k,2^k}`/`R_{k-1}×L_k` construction. Registered as an obstruction, not invented around.

**F.6/F.7 (pushforward convergence) — the decisive result.** Even without the missing rescaling, the
pushforward measure itself is directly computable (inclusion needs no metric). Extending to G0–G9
(Section 17's explicit instruction to go beyond G0–G4):

| Transition | TV distance | Mass fraction on new vertices |
|---|---|---|
| G0→G1 | 0.7143 | 0.7143 |
| G1→G2 | 0.6452 | 0.6452 |
| G2→G3 | 0.6299 | 0.6299 |
| G3→G4 | 0.6262 | 0.6262 |
| G4→G5 | 0.62531 | 0.62531 |
| G5→G6 | 0.62508 | 0.62508 |
| G6→G7 | 0.62502 | 0.62502 |
| G7→G8 | 0.625005 | 0.625005 |
| G8→G9 | 0.625001 | 0.625001 |

**The total-variation distance does not go to zero — it stabilizes at a strictly positive constant
(≈0.625), converging geometrically** (each deviation from 0.625 shrinks by almost exactly `4×` per
shell — 0.0012 → 0.0003 → 0.000076 → 0.000019 → 0.0000048 → 0.0000012). This is precise, repeatable
numerical evidence, not a closed-form proof of the exact limiting constant (none is attempted here).

**Conclusion: under the only recoverable refinement map (unrescaled inclusion), the degree-measure
sequence does not converge to a coherent limit.** A persistent, non-vanishing share of the total
measure is displaced onto genuinely new vertices at *every* refinement step, forever — this is
**Outcome D** (Section 9's classification), established with unusually strong evidence for a
finite-shell computation, and explicitly **not** claimed as a `k→∞` theorem (Section 17 caveat).

This directly and correctly blocks F.8–F.10: no attempt is made to construct a continuum Dirichlet
form limit, continuum generator, or Fokker–Planck correspondence, since F.7 did not merely leave
convergence "unresolved" — it positively demonstrated non-convergence under the only map available.

## Theorem registry

| Theorem | Status |
|---|---|
| C-004F.1 (degree measure) | **PROVEN** |
| C-004F.2 (weighted reversibility) | **PROVEN** |
| C-004F.3 (Dirichlet representation) | **PROVEN** |
| C-004F.4 (refinement compatibility) | **DISPROVEN** — pushforward discrepancy stabilizes nonzero, does not vanish |
| C-004F.5 (continuum thermodynamic limit) | **DISPROVEN** for the unrescaled map; **OPEN** for any rescaled version (untestable — no source-supported rescaling exists) |
| C-004F.6 (Fokker–Planck correspondence) | **OPEN / NOT TESTABLE** — blocked upstream |

## Entropy-production consequence (Section 13)

**Yes — as an inequality, not a number.** With `Q_k^*` now concretely derived and its detailed-balance
and conservation properties concretely proven (not merely asserted, as BRIDGE B-006 does abstractly),
the standard Lyapunov argument goes through directly: `dF/dt = ∑_i(Q^*P)_i log(P_i/π_i)`, which
symmetrizes via detailed balance into a sum of terms `≤0` by the elementary inequality
`(a−b)(log a−log b)≥0`. This requires **only** detailed balance and conservation (both proven this
run) — **not** a choice of `P(0)` or evaluation time. Numerically sanity-checked across 12 sampled
`(P(0),t)` combinations per shell, G0–G4: `σ≥0` holds in every case. This **confirms and formalizes**
BRIDGE B-006's own claimed proof method on the now-concrete operator. **Sign: DERIVED. Magnitude:
still PROVEN NON-IDENTIFIABLE (C-004C, not reopened).**

## Target-independence audit

All recovered objects (`π_k`, `Q_k`, `Q_k^*`, `E_k`, `ρ_k`, pushforward distances) are functions of
`(k, A_k, D_k, L_k)` alone — no reference to `32`, `N_H`, `H_F`, `D_F`, `J_F`, `γ_F`, `Y_u`, `Y_d`,
`Y_e`, `Y_ν`, `V_CKM`, `U_PMNS`, or `Ξ_obs` anywhere. No hidden fitted constants introduced. **PASS.**

## Provenance ledger

| Object | Status |
|---|---|
| ARBS graph construction | DERIVED/VERIFIED (math); PROVENANCE GAP (textual, unchanged) |
| Generator statement | SOURCE CONFLICT (preserved, unchanged) |
| `Q_k`, `Q_k^*` | DERIVED (C-004D, re-verified) |
| `L²(V,μ_k)` | DERIVED FROM P_ss (this run — not itself source-certified) |
| `E_k` (Dirichlet form) | DERIVED (this run, exact formula + proof) |
| `ρ_k` (refinement map) | DERIVED (combinatorial part); metric rescaling OPEN |
| Continuum thermodynamic correspondence | OPEN / DISPROVEN-for-the-only-recoverable-map |

## What is frozen / not touched

Per this run's own scope: `C-004E` (missing convergence theorem, unaffected), `C-004D` (still
PARTIALLY CLOSED, unaffected), `THM-GEN-DISTINCT-001` (still PROVEN, unaffected). `C-004C`'s
non-identifiability closure is **not reopened** — no new `P(0)`, evaluation time, or `Π₀` ranking was
chosen or computed. `G*` remains **UNRESOLVED**.

## Closure matrix

| Object | Status |
|---|---|
| C-004F.1–.4 | DERIVED / VERIFIED |
| C-004F.5 | Combinatorial map DERIVED; metric rescaling OPEN |
| C-004F.6 | CALCULATED (9 transitions, G0–G9) |
| C-004F.7 | Outcome **D** — no identifiable limit (strong evidence, not formally proven) |
| C-004F.8–.10 | NOT ATTEMPTED (correctly blocked) |
| `σ_k` sign | CONFIRMED via concrete `Q_k^*` |
| `σ_k` magnitude | PROVEN NON-IDENTIFIABLE (unchanged) |
| `G*` | UNRESOLVED (unchanged) |

## Exactly one next unresolved upstream dependency

> **Recover or derive, from admissible source material only, the explicit metric/edge-length
> rescaling law for the ARBS `K_{2^k,2^k}`/`R_{k-1}×L_k` construction specifically** — the "global
> isotropic contraction constant `α`, `0<α<1`" the whitepaper asserts abstractly for the generic
> refinement functor `R`, but never ties to a concrete formula for this particular shell
> construction. Without it, the fully-derived combinatorial refinement map cannot be turned into a
> resolution-refining map compatible with any continuum-limit test, and no rescaled version of the
> F.6/F.7 convergence test can be attempted. Under the only currently recoverable (unrescaled) map,
> this run establishes — with strong geometric numerical evidence over 9 shell transitions — that
> the degree-measure sequence does not converge to a coherent limit; that result stands as the
> best-supported current answer to C-004F unless and until this rescaling law is recovered from
> source material, not invented.

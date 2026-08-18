# C-004E — Discrete-to-Continuum Thermodynamic Generator Correspondence

**Run date:** 2026-08-18 (fifth closure run, continuing from `CLOSURE_REPORT_RUN4_C004D.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.4.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.5.xlsx`

## Exact proof obligation

> `ℒ*_discrete = −LD⁻¹ → ? → ℒ*_continuum = −∇·(P∇log P_ss)` under the project's own continuum-limit
> machinery. Does the framework provide a sequence `G_n → M` and scaling operators `R_n` such that
> `lim_{n→∞} R_n(−L_nD_n⁻¹) = −∇·(P∇log P_ss)`?

## Answer: **NO.**

A focused corpus search (all 9 workbooks + whitepaper) for the project's actual convergence
machinery — the refinement functor `R`, `RF-001`–`RF-005` (Universal Recovery Functor), `BRIDGE
B-004`, Mosco convergence, Gromov–Hausdorff limits, Kato's Representation Theorem, Trotter–Kato, and
`Δ_M = lim L_n` — establishes three findings that together answer the obligation decisively:

**F1 — The only convergence machinery that exists targets a different branch entirely.**
`RF-001`/`RF-003` (CERTIFIED) give a real four-topology convergence chain
`G_n →^{GH} (M,g) ⇒ E_n →^{Mosco} E ⇒ L_n →^{s.r.} L ⇒ T_n(t) →^{s} T(t)`, correctly citing Kato's
First Representation Theorem and Trotter–Kato. But it is built on the **symmetric spectral Laplacian
`L=D−A`** and its Dirac operator/heat semigroup — the same branch already verified throughout this
project's ARBS reconstruction (run 2) — and it targets **geometric** recovery (`g_μν`, the
Laplace–Beltrami limit `Δ_M`), not probability/thermodynamic recovery. The specific geometry bridge
(`BRIDGE B-004`) is itself still `OPEN` in source.

**F2 — The Hilbert space this machinery lives in doesn't cover the thermodynamic operator.**
The corpus states `L` is "a linear operator on `L²(V,μ)`" without ever pinning `μ` down to counting
measure or degree measure explicitly. But tracing every certified construction that actually *uses*
this space (`DER-QR-001`'s Hilbert-space-as-spectral-completion, `DER-SPC-003`'s eigendecomposition,
and this project's own independently-verified ARBS spectral reconstruction) shows `L`'s eigenvectors
are orthonormal only under the **counting-measure** inner product — never redone for the
degree-weighted `L²(V,d)` space in which `−D⁻¹L` (or `L_norm`, proven in C-004D) is naturally
self-adjoint. The `RF`/`B-004` machinery inherits the counting-measure space.

**F3 — The continuum FP equation and the refinement-limit apparatus are never connected at all.**
`ℒ*P = −∇·(P∇log P_ss)` is stated once, as a bare PDE by analogy with standard non-equilibrium
statistical mechanics (row 2116 of the corpus). It is never mentioned alongside `R_n`, `G_n→M`,
Mosco convergence, `Δ_M`, or any other limit apparatus anywhere in the ~450-sheet corpus. `Δ_M` and
`BRIDGE B-004` target `g_μν` — a different recovery goal entirely.

**Conclusion:** this is a genuine missing theorem, not an unresolved detail. The continuum
Fokker–Planck equation and the graph-refinement convergence theory were developed as two entirely
separate pieces of the framework that were never connected — exactly the theorem-level obstruction
the governing instructions anticipated as the legitimate outcome if no convergence map exists.

## Consequence already available: THM-GEN-DISTINCT-001 (promoted to canonical)

Per this run's directive, the C-004D finding is formalized as a standing, ARBS-independent
structural theorem:

> **For any connected, unweighted, undirected graph `G=(V,E)` with `L=D−A`:**
> 1. `ker(L)=span{1}` (standard), so `−L` has **uniform** stationary measure.
> 2. A reversible generator `ℒ*_therm` with stationary measure `P_ss ∝ d` must satisfy
>    `ℒ*_therm·d=0`, i.e. `d ∈ ker(ℒ*_therm)`.
> 3. `d ∈ ker(L)` **iff `G` is regular.** Verified this run: `‖L·d‖ = 0` exactly for G0 (regular);
>    `‖L·d‖ = 4.90, 25.77, 145.41, 822.50` for G1–G4 respectively (irregular, growing with size).
> 4. Therefore **`−L ≠ c·ℒ*_therm`** for any scalar `c`, for any irregular connected graph — the
>    spectral and thermodynamic generators are structurally distinct operators whenever the graph is
>    irregular. This is general, not an ARBS-specific numerical accident.
> 5. The unique reconciling operator, given only the graph's edges and detailed balance w.r.t.
>    `P_ss ∝ d`, is `ℒ*_therm = −LD⁻¹` (derived in C-004D), similar to `L_norm=D^{-1/2}LD^{-1/2}`.

**Status: PROVEN**, algebraically and numerically. Recommended for the canonical Universal Rosetta
Stone theorem registry as a standing result, independent of the ARBS shell-selection question.

## What is frozen / not touched this run

Per the directive, everything at or above C-004D stands unchanged: `C-004D` remains **PARTIALLY
CLOSED**; `σ_k` remains **PROVEN NON-IDENTIFIABLE** (C-004C, not reopened); no new `P(0)`, evaluation
time, or `Π₀` ranking was computed; `G*` remains **UNRESOLVED**.

## Closure matrix

| Object | Status |
|---|---|
| C-004E (discrete-to-continuum FP correspondence) | **OPEN** — precise theorem-level obstruction identified |
| THM-GEN-DISTINCT-001 | **PROVEN**; recommended for canonical promotion |
| C-004D (discrete generator reconciliation) | Unaffected, still PARTIALLY CLOSED |
| C-004C (σ_k identifiability) | Not reopened; PROVEN NON-IDENTIFIABLE stands |
| G* | UNRESOLVED (unchanged) |

## Exactly one next unresolved upstream dependency

> **Construct (or formally register as a new, explicitly named open bridge, alongside `BRIDGE
> B-004`) a discrete-to-continuum convergence theorem for the thermodynamic branch specifically**: a
> sequence `G_n → M`, scaling operators `R_n`, and a proof (Mosco convergence, Gromov–Hausdorff, or
> an equivalent route already admissible in this project) that `lim R_n(−L_nD_n⁻¹)` converges to some
> explicit continuum operator — built in the **degree-weighted `L²(V,d)`** Hilbert space (where
> `−D⁻¹L` is actually self-adjoint), not simply re-used from the existing counting-measure `RF`
> apparatus, which this run confirmed lives in a different reference measure entirely. Only after
> that convergence theorem exists can one ask whether its limit matches the specific PDE
> `ℒ*P=−∇·(P∇log P_ss)` already asserted in source. Until then, `σ_k` has a derived discrete
> generator (C-004D) but no verified continuum meaning, and no further attempt to pin down
> `P(0)`/evaluation time for C-004C should proceed.

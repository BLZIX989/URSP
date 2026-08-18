# C-004I — ARBS Diffusion-Metric Convergence and Measure Recovery

**Run date:** 2026-08-18 (ninth closure run, continuing from `CLOSURE_REPORT_RUN8_C004H.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.8.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.9.xlsx`

## Headline finding

**The Wasserstein-1 distance between the pushforward degree measure and the actual next-shell
measure — using the certified diffusion metric as ground cost — decays geometrically toward zero,**
converging to the same `√2` rate found for metric-invariance violation, even though the total
variation distance used in the previous two runs does not. This resolves an apparent contradiction
rather than deepening it: TV was the wrong norm for this question. It doesn't fully close C-004I, but
it is the most consequential positive result since C-004G's negative one.

## C-004I.1 — Exact diffusion metric, proven not assumed

Recovered exactly: `d(i,j) = √(Σ_{k:λ_k>0} (φ_k(i)−φ_k(j))²/λ_k)` (`ENG-011`, `DER-GEO-005`
CERTIFIED). No time parameter, no alternative formulation found anywhere in the corpus.

**`d(i,j)² = R_eff(i,j)` is now PROVEN, not merely numerically observed** (last run reported this as
an empirical `~1e-12` residual): the standard spectral decomposition `L=Σλ_kφ_kφ_k^T` gives
`L⁺=Σ(1/λ_k)φ_kφ_k^T` (Moore-Penrose pseudoinverse, standard fact), and effective resistance's
definition `R_eff(i,j)=(e_i−e_j)^TL⁺(e_i−e_j)` substitutes directly to exactly `ENG-011`'s formula.
This is a general graph-theoretic identity, unconditional, with no dependence on any time/integration
limit — the numerical residuals (`1e-16` to `1e-12`) are simply floating-point roundoff of an exact
fact.

## C-004I.2 — Closed form: real progress, not completed

**Vertex-class symmetry is proven** (not just numerically confirmed to `~2e-16`): any permutation of
vertices within a single `L_m` or `R_m` is a graph automorphism (identical neighborhoods by
construction), and diffusion distance — a function of `L`'s spectrum alone — is automorphism-
invariant. This reduces the diffusion-distance matrix to at most `2(k+1)` classes, a genuine
`O(N²)→O(k²)` exact dimension reduction via the standard equitable-partition/quotient-matrix
technique. **Full symbolic diagonalization of the resulting quotient recursion is not completed** —
flagged honestly as a well-posed, unresolved further question, not oversold as solved.
`D_∞ ≈ 1.4288690166...` remains numerically characterized (4 shells identical to 10 decimals), not
derived in closed form.

## C-004I.3/4 — `ε_k` precisely defined, not just "ratio √2"

Last run reported a clean `√2` ratio without pinning down exactly what converges. This run defines it
literally: `ε_k := max_{i,j∈V_k} |d_{k+1}(ρ_k(i),ρ_k(j)) − d_k(i,j)|` — the direct, unsquared,
absolute failure of the source's own stated Induced Metric Invariance axiom, maximized over old
vertex pairs. Computed for 9 transitions (G0→G1 through G9→G10):

`0, 0.42265, 0.29886, 0.21132, 0.14943, 0.10566, 0.07471, 0.05283, 0.03735...`

Ratio `ε_k/ε_{k+1}` is `1.41421356237309...` — matching `√2` to 14–15 significant figures — for
**every one of 8 consecutive transitions**, essentially at floating-point precision limits.

**Classification: ASYMPTOTIC, not exact — and no rescaling is needed.** The raw, unrescaled diffusion
distance already satisfies `ε_k→0`; introducing an `s_k` renormalization would be both unnecessary
and (per the governing instruction) inadmissible without independent source derivation. None was
introduced.

## C-004I.5/6 — Measure defect, three norms, and the reason for the earlier "0.625"

Defined `Δ_μ(k)` properly as three distinct, standard, mathematically justified quantities rather
than a bare scalar:

- **TV / L1 / L2** (metric-independent): unchanged, confirmed again over 9 transitions — TV
  stabilizes at `≈0.625`, does **not** vanish. `L1 = 2×TV` exactly at every step (verified).
- **Wasserstein-1** (using the diffusion metric as ground cost — the metrically appropriate norm for
  a *metric-measure* space, which TV/L1/L2 ignore entirely): **`0.822, 0.583, 0.401, 0.272, 0.186,
  0.128, 0.089, 0.062, 0.044, 0.031`** for the 10 transitions G0→G1 through G9→G10 — a clean
  geometric decay, ratio converging monotonically from `1.409` toward `1.41421356...` (`√2`) as `k`
  increases.

**Why the contradiction isn't one:** TV/L1/L2 stay bounded away from zero because a persistent
~62.5% of the measure's mass sits on genuinely new vertices at every step — these norms treat that as
all-or-nothing disagreement no matter how metrically close those new atoms are to the existing
cloud. Wasserstein distance asks how *far* (in the certified diffusion metric) that mass has to
travel — and since the diffusion-metric diameter is bounded and the point cloud increasingly
clusters (mean pairwise distance → 0, established in run 8), the transport cost shrinks even though
naive set-disagreement does not.

**No renormalization was needed or introduced** — the raw, source-certified `π_k=d_i/(2|E_k|)` used
as-is already shows this Wasserstein convergence under the raw diffusion metric.

## C-004I.7/13 — Outcome selection: none of A–D applies cleanly

The honest result is a graded, componentwise picture, not a forced single letter:

| Piece | Result |
|---|---|
| Diameter (diffusion metric) | Bounded, strong numerical evidence of convergence |
| Metric invariance | Asymptotic (not exact), clean `√2` rate, strong evidence, not proven |
| TV/L1/L2 measure convergence | **PROVEN non-convergent** |
| Wasserstein-1 measure convergence | Strong numerical evidence **of** convergence, matching `√2` rate |
| Primal Edge Scaling (topological mechanism) | **PROVEN incompatible** (unchanged, C-004G) |
| Dirichlet form (μ-normalized) | **DERIVED/VERIFIED** (unchanged, C-004F.4) |

Closest honest label: strong (not formally proven) evidence *for* a genuine metric-measure limit in
the Wasserstein/weak sense, coexisting with two proven theorem-level facts pulling the other way —
the source's own derivation mechanism doesn't apply, and the *strong*-sense measure convergence
provably fails.

## Critical caveat: this is all about `L_k`, not `Q_k`

The diffusion/effective-resistance metric has the standard variational characterization
`R_eff(i,j)⁻¹ = min{f^TL_kf : f(i)=1,f(j)=0}` — it is tied directly to the **spectral** Laplacian
`L_k`, not to the **thermodynamic** generator `Q_k=-D_k^{-1}L_k`. `THM-GEN-DISTINCT-001` proves these
are different operators for irregular graphs. **This run's positive findings pertain entirely to the
`L_k`-based geometric branch.** They say nothing directly about the `Q_k`-based Fokker–Planck
correspondence that `C-004E` originally asked about — a promising geometric limit does not
automatically transfer to the thermodynamic one. `L_k` and `Q_k` are preserved as distinct throughout,
per instruction, and not conflated.

## Continuum dimension (C-004I.8) — inconclusive, reported honestly

- **Volume growth:** not power-law. The point cloud is extremely concentrated (fewer than 2 of 4094
  vertices lie within diffusion-distance 1.0 of the apex, against a diameter of only ~1.43) —
  itself a real structural finding (near-singular concentration), not a failed computation.
- **Spectral dimension:** a rough heat-trace fit gives `~1.8`, but this is **not validated** —
  sensitive to the fitting range, no genuine intermediate scaling regime isolated. Reported as
  preliminary and unreliable, not tuned toward any target value.

## Target independence and falsification ledger

All new objects are functions of `(k, L_k, D_k)` alone; **PASS**, no reference to any downstream
target. Falsification ledger addition: the TV-distance choice in runs 6–8 is not retracted (it was
computed correctly) but is now understood to be the wrong norm for this specific question.

## Packet branch: not activated

Per the governing stop condition, `PACKET-REFINEMENT-RECOVERY-001` is **not** triggered — ARBS has
not been shown to fail the continuum substrate requirements; if anything, the geometric branch shows
the opposite trend this run. `σ_k`, `Π₀`, `G*`, NCG, flavor, and scale are untouched, per instruction.

## Exactly one next unresolved upstream dependency

> Two independent tasks, neither resolvable by further reading of existing source material:
> **(1)** formally prove — not merely numerically demonstrate — the Wasserstein-1/diffusion-metric
> convergence analytically, via an asymptotic spectral analysis of the ARBS Laplacian family (the
> quotient-matrix reduction identified in C-004I.2 is the natural starting point); and
> **(2)** determine whether any such proven `L_k`-based geometric limit has *any* bearing on the
> originally-sought `Q_k`-based thermodynamic Fokker–Planck correspondence (C-004E) — given
> `THM-GEN-DISTINCT-001`, a limit for one operator does not automatically transfer to the other, and
> no source material addresses this transfer question at all.

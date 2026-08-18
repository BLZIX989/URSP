# C-004D — Thermodynamic Generator Reconciliation

**Run date:** 2026-08-18 (fourth closure run, continuing from `CLOSURE_REPORT_RUN3_C004C.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.3.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.4.xlsx`

## Note on this run's starting point

This run's directive arrived with a substantial pre-worked derivation (Theorem C-004D.1, an operator
table, and a numeric table of `λ₁(L)`/`λ₁(L_norm)` for G0–G4) attributed to prior analysis. Rather
than taking it on faith, every claim was **independently recomputed from scratch** in
`reconstruction/c004d_generator.py` against the already-certified `A`, `D`, `L` matrices for G0–G4.
All of it checks out — the recomputed `λ₁(L)` and `λ₁(L_norm)` values match to full double precision,
and the additional identities (matrix-level, not just spectral) were verified directly. One further
corpus check was also run per the explicit request not to miss anything: confirming the exact source
citations for the generator inconsistency (below), which sharpens the claim from "the two statements
seem to conflict" to a direct, quotable textual contradiction.

## A. Exact operator identities (proven and verified)

**Theorem C-004D.1** (proven algebraically, verified numerically for G0–G4):

- `L = D − A` is the certified spectral Laplacian: symmetric, `L ⪰ 0`, `L·1 = 0`.
- The reversible continuous-time random-walk generator compatible with the graph's own edges and
  BRIDGE B-005's own invoked detailed-balance condition is **uniquely derived** (not assumed) as
  `Q = −D⁻¹L`, giving `Q_ij = A_ij/d_i` (Section 5 derivation, `reconstruction/c004d_generator.py`).
  Verification: `π_iQ_ij = π_jQ_ji` for `π = P_ss = d/(2|E|)` holds exactly because `A` is symmetric.
- `Q* = Qᵀ = −LD⁻¹`. Verified: `Q*·d = 0` (residual `~1e-16`), so `P_ss = d/(2|E|)` is recovered
  exactly from `Q*`.
- `L_norm = D^{-1/2}LD^{-1/2}` is **similar** to `−Q`: `L_norm = D^{1/2}(−Q)D^{-1/2}`, verified
  exactly for every shell — hence `Spec(−Q) = Spec(L_norm)` (confirmed numerically, `<1e-6` residual).

## B. Exact non-identities

- `Q ≠ −L` and `Q* ≠ −L` as **matrices** for every irregular shell (G1–G4), confirmed by direct
  Frobenius-norm comparison (not merely eigenvalues) — `‖Q−(−L)‖_F` is 4.36, 15.36, 46.96, 137.16 for
  G1–G4 respectively, all clearly nonzero.
- `Spec(L) ≠ Spec(L_norm)` for G1–G4.
- `P_uniform ≠ P_degree` for G1–G4 (`‖·‖₁` up to 0.353 at G4).
- **G0 is the single exceptional regular case**: all of the above identities collapse to *exact*
  equality (`‖Q−(−L)‖_F = 0`, `P_uniform = P_degree` exactly) — matching Theorem C-004D.1's own
  regular-graph exception clause.

## C. Numerical reconciliation, G0–G4

| Shell | Regular? | λ₁(L) | λ₁(L_norm) | ratio | λ_max(L) | λ_max(L_norm) | Spec(L)=Spec(L_norm)? |
|---|---|---|---|---|---|---|---|
| G0 | Yes | 2.0000 | 2.0000 | 1.000 | 2.0000 | 2.0000 | Yes |
| G1 | No | 0.7639 | 0.5286 | 1.445 | 5.2361 | 2.0000 | No |
| G2 | No | 0.4955 | 0.2373 | 2.089 | 10.4941 | 2.0000 | No |
| G3 | No | 0.3913 | 0.1506 | 2.599 | 20.9882 | 2.0000 | No |
| G4 | No | 0.3432 | 0.1140 | 3.009 | 41.9763 | 2.0000 | No |

(`λ_max(L_norm)=2` exactly for every irregular shell is the standard fact that the normalized
Laplacian spectrum lies in `[0,2]` with max `=2` iff the graph is bipartite — every ARBS shell is
bipartite by construction, so this is expected, not a new discovery.)

## D. Stationary distributions

Verified for every shell: `L·1=0` (exact), `Q*·d=0` (residual `~1e-16`, i.e. `P_ss=d/(2|E|)` is
exactly stationary under `Q*`), `−L·P_uniform=0` (exact). Degree sequences confirm irregularity:
G0 `{1}`; G1 `{1,2,3}`; G2 `{1,3,4,6}`; G3 `{1,3,6,8,12}`; G4 `{1,3,6,12,16,24}`.

## E. Spectral comparison

See table C above. `Spec(L)` and `Spec(L_norm)` diverge increasingly with shell size (ratio
`λ₁(L)/λ₁(L_norm)` grows from 1.45 at G1 to 3.01 at G4) — the spectral gap on the *thermodynamic*
scale shrinks relative to the *spectral* scale as the graph grows more irregular.

## F. H-theorem compatibility

The H-theorem (BRIDGE B-006) requires its stated `P_ss` to actually be stationary under whatever
generator `P(t)` evolves under, for the log-sum inequality proof to hold. Using `−L` would make
B-006's own cited `P_ss=d/(2|E|)` **wrong** for irregular graphs, breaking the theorem's own
hypothesis. Using `Q*=−LD⁻¹` (detail-balanced by construction w.r.t. that exact `P_ss`) satisfies it.
This resolves the operator ambiguity C-004C surfaced: **`σ`'s generator is `L*_therm`, not `L`.**

## G. Time-scale implications

`t_H`, `λ_c`, `δ_spec` all belong to the **spectral** branch (`L`) and are unaffected by this run.
`σ` belongs to the **thermodynamic** branch (`L*_therm`). `Π₀ = (δ_spec−λ_c)/σ` therefore **mixes
quantities from two different generators** — confirmed directly (Section 14). Classification:
**C — dimensionally/structurally admissible (C-004C's dimensional audit already passed on unit
grounds) but not proved equivalent or compatible as a meaningful ratio.** No source theorem
addresses this; not forced to equivalence here.

## H. Updated dependency chain

```
Γ ≺ ARBS ≺ G_k ≺ A_k, D_k ≺ L_k ≺ Spec(L_k) ≺ t_H,k ≺ λ_c,k ≺ δ_spec,k
                                    │
                                    ├── (thermodynamic branch, reconciled this run)
                                    ▼
                        L_k ≺ D_k⁻¹L_k ≺ ℒ_k ≺ ℒ*_k ≺ P_ss,k ≺ F_k ≺ σ_k
                                    │
                                    ▼
                    [reunite, unresolved: Section 14 classification C]
                              Π₀(G_k) ≺ G*  ≺ P_H^(32) ≺ Φ_H ≺ ... [all still blocked]
```

## I. C-004D closure status

**PARTIALLY CLOSED.**

- **GENERATOR RECONCILED BY DEGREE NORMALIZATION**: `ℒ_therm = −D⁻¹L` (not `−L`) is the correct
  discrete thermodynamic generator for irregular ARBS shells — derived, not assumed, from the
  graph's own edges plus BRIDGE B-005's own detailed-balance condition.
- **Discrete-to-continuum correspondence** with the source's registered
  `ℒ*P = −∇·(P∇log P_ss)` remains **OPEN** — not proved, not invented around. `Q*` is the standard
  discrete master-equation form associated with a detail-balanced reversible chain, but literal
  convergence to that specific continuum differential operator under mesh refinement is a separate
  limit statement this run does not attempt (the analogous limit for the spectral branch, BRIDGE
  B-004, is itself independently OPEN in source).

## Falsification / provenance ledger (additions)

- **`ℒ_therm = −L`**: FALSIFIED for G1–G4 (irregular); holds exactly for G0 (regular) — the
  exceptional case anticipated by the theorem, not a contradiction of it.
- **Textual inconsistency in source, precisely located**: row 2024 of `54_SOURCE_TEXT_CORPUS`
  ("The generator is −L for the continuous-time random walk") directly conflicts with the CERTIFIED
  `BRIDGE B-005` (rows 1954–1957, 2137: stationary measure `P_ss=d/(2|E|)` via Perron-Frobenius +
  detailed balance) for any non-regular graph. Both statements are quoted verbatim in workbook sheet
  73. This is preserved as a documented corpus inconsistency, not silently resolved in either
  direction.

## C-004C status (unchanged, not reopened)

Per Section 19 of the governing instructions, no new `P(0)`, evaluation time, or `σ_k` value was
chosen or computed this run, and no `Π₀` ranking was recalculated. `σ_k` remains **PROVEN
NON-IDENTIFIABLE** exactly as closed in `CLOSURE_REPORT_RUN3_C004C.md`; this run only resolves which
operator `σ`'s definition actually refers to, sharpening (not reopening) that closure.

## Exactly one next unresolved upstream dependency

> **Prove or disprove that the discrete reversible-chain generator `ℒ*_therm = −LD⁻¹`, derived this
> run from the graph's own edges and BRIDGE B-005's certified detailed-balance condition, is the
> correct discrete realization of the source's registered continuum expression
> `ℒ*P = −∇·(P∇log P_ss)` — i.e., establish (or formally register as a separate open bridge,
> analogous to BRIDGE B-004's heat-kernel-to-geometry limit) the discrete-to-continuum correspondence
> for the thermodynamic branch specifically.** This is logically prior to any future attempt to pin
> down `P(0)`/evaluation time for `σ_k` (C-004C), since such a choice would otherwise be made
> relative to an operator whose continuum meaning is still unverified.

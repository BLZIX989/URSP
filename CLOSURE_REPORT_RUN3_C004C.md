# C-004C — Entropy-Production Recovery

**Run date:** 2026-08-18 (third closure run, continuing from `CLOSURE_REPORT_RUN2.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.2.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.3.xlsx`

## Task

Determine whether the existing ARBS/UOC mathematics uniquely determines the per-shell entropy
production `σ_k` in `Π₀(G_k) = [δ_spec(G_k) − λ_c,k] / σ_k`. Calculate it if derivable; record the
sign if only that is derivable; prove non-identifiability if `σ_k` requires unfixed free data.

## What was found

A corpus-wide search (all 9 source workbooks + whitepaper) turned up the genuine source definition
of `σ` (already partially found last run) plus three new, decisive facts:

1. **`σ = −dF/dt ≥ 0`** (BRIDGE B-006, CERTIFIED), `F[P] = ∫P log(P/P_ss) dμ`, the KL-divergence
   dissipation rate of a trajectory `P(t)` solving `∂_tP = ℒ*P`. This is a **theorem about
   existence and sign**, not a formula that reduces to one number per graph.
2. **The one place a Π-type initial condition was ever actually chosen** in the corpus (`BRIDGE
   B-007`/`C-008`, representation-invariance test) used `a(0)=e₁` — an arbitrary unit-vector choice
   — on `K₃,₃`, a **different, unrelated test graph**, for a one-off illustrative computation. This
   is direct evidence against a canonical rule: when the source's own authors needed a number, they
   picked one for that example rather than citing a general prescription.
3. **A generator inconsistency (`GAP-GENERATOR-001`, new this run)**: BRIDGE B-006 states the
   stationary measure is the **degree distribution** `P_ss(i)=d_i/(2|E|)`, proved via
   Perron–Frobenius on "the transition matrix." But the ARBS spectral reconstruction already
   certified elsewhere in this project (`DER-SPC-002`: `L=D−A`; `DER-SPC-004`: `K_t=exp(−tL)`) uses
   the plain combinatorial Laplacian, whose stationary state under `exp(−tL)` is the **uniform**
   distribution for a connected graph — these coincide only for *regular* graphs (constant degree).
   G0–G4 are not regular (degrees vary substantially across `L_k`/`R_k` and across `k`). No
   registry entry reconciles the two operators. This means even fixing `P(0)` and `t` would not be
   enough — which generator to evolve under is itself ambiguous.
4. **The source's own registry marks the surrounding functional as OPEN, independent of `σ`**:
   `DER-ORG-007` ("Organizational Persistence Functional Recovery") and `DER-OPEN-003` ("Π_O
   Rigorous Derivation") both register `Π_O = f(σ, C, Spec(L))`'s well-definedness itself as
   `[OPEN]` — not merely `σ`'s numeric value.
5. **`H_FP` hyperedge registry entry** explicitly lists "initial distribution" as a required-but-
   unsupplied input for even the simpler object `P_ss`, confirming this gap is acknowledged, not
   overlooked, by the project's own registries.

A distinct, explicitly OPEN alternative coupling `Π_O = 1 − exp(−σ·δ_spec/λ_c)` also exists
(`DER-TD-005`) — preserved separately per the rule against merging distinct definitions sharing a
symbol; not used to close anything here.

## Sign result (proven)

The H-theorem's sign conclusion (`σ ≥ 0`, strictly `> 0` whenever `P(t) ≠ P_ss`) holds for **any**
admissible generator and initial condition — it is the one thing about `σ_k` that does not depend
on the unfixed free data. Combined with the already-established fact that
`δ_spec(G_k) − λ_c,k < 0` for every `k=0..4` (prior run):

> **`Π₀(G_k) < 0` for every shell G0–G4.** Sign only — magnitude and ranking remain open.

## Non-identifiability demonstration

Rather than stop at assertion, `reconstruction/sigma_nonidentifiability_demo.py` computes `σ(t)`
concretely using the certified heat semigroup `exp(−tL)` already used throughout ARBS (one literal
resolution of `GAP-GENERATOR-001`, explicitly **not** claimed canonical), sampled at 2 illustrative
starting nodes × 3 illustrative times, across all 5 shells:

**`argmax_k Π₀(G_k)` takes 3 different values (G0, G1, or G2) across just 6 sampled combinations —
never G3.** This is a concrete existence proof that the ranking is **not parameter-invariant**: it
depends materially on the unfixed initial condition and evaluation time. No claim is made about
what the "true" ranking is under any canonical choice, because no such choice exists in the source
material — the demonstration exists only to convert the non-identifiability claim from assertion
into a computed fact.

## Closure matrix

| Object | Status |
|---|---|
| `σ_k` (specific per-shell number) | **PROVEN NON-IDENTIFIABLE** |
| `σ_k` (sign) | **PROVEN SIGN-ONLY**: `σ_k > 0` (generic case) |
| `Π₀(G_k)` (sign) | **PROVEN SIGN-ONLY**: `< 0` for all `k=0..4` |
| `Π₀(G_k)` (magnitude/ranking) | **OPEN** |
| `OPEN-020E.2` | **REMAINS OPEN** — outcome D; `argmax` not evaluable, demonstrated parameter-dependent |
| `G*` | **UNRESOLVED** (unchanged) |
| `GAP-GENERATOR-001` | **OPEN** (new) — B-006's stationary measure vs. the certified Laplacian's actual stationary state |

## Falsification / rejection ledger (additions)

- **`lim_{t→∞} σ(t)` as a candidate**: REJECTED. Not source-supported, and degenerate — `F(t)→0` as
  `P(t)→P_ss` under any admissible generator, so this candidate gives `σ_∞=0` identically for every
  shell, making `Π₀` undefined (division by zero) for all `k`. Recorded to show it was considered
  and excluded, not adopted.
- No fitted-parameter or ad hoc scalar (`‖L‖`, `trace(L)`, mean eigenvalue, etc.) was substituted
  for `σ`; Section 18 prohibits this and none is needed to reach a decisive result here.

## Provenance ledger

- Mathematical reproducibility of the ARBS graph construction and full spectra: **VERIFIED**
  (unchanged from run 2).
- `σ`'s functional form (the H-theorem) and its sign: **SOURCE-EXACT / CERTIFIED**.
- `σ`'s reduction to a specific per-shell number: **no source provenance exists**; the only
  precedent for choosing free data at all is an ad hoc, example-specific choice on an unrelated
  graph.

## Updated canonical dependency chain

```
Γ ≺ ARBS ≺ G_k ≺ A_k ≺ B_k ≺ L_k ≺ D_G,k ≺ Spec(L_k) ≺ p_A,k ≺ t_H,k ≺ λ_c,k ≺ δ_spec,k
   ≺ σ_k   [PROVEN NON-IDENTIFIABLE — chain blocked here]
   ≺ Π_0(G_k)  [sign only: < 0 for all k; magnitude OPEN]
   ≺ G*   [UNRESOLVED]
   ≺ P_H^(32) ≺ Φ_H ≺ D_F ≺ NCG ≺ flavor ≺ continuum ≺ scale   [ALL BLOCKED, not attempted]
```

## Exactly one next unresolved upstream dependency

> **Resolve `GAP-GENERATOR-001` and fix the free data `(P(0), t)` for the entropy-production
> functional `σ = −dF/dt`.** Specifically: (a) determine, from admissible source material only,
> which generator `ℒ*` the Fokker–Planck evolution `∂_tP=ℒ*P` in BRIDGE B-006 actually refers to,
> and reconcile its stationary measure with the certified ARBS Laplacian `L=D−A` used everywhere
> else in this project (they currently disagree for non-regular graphs); and (b) supply a
> canonical, target-independent rule fixing the initial distribution `P(0)` and evaluation time (or
> time-reduction rule) for each shell `G_k`. Until both are supplied by source material — not
> invented here — `σ_k`, `Π₀(G_k)`'s magnitude, and `G*` all stay blocked at this exact point.

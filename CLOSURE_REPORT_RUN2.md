# ARBS-CONSTRUCTION-001 — Graph Reconstruction and Spectral Reproduction

**Run date:** 2026-08-18 (second closure run, continuing from `CLOSURE_REPORT.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.1.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.2.xlsx`
**New source material this run:** `Combined_Compiler_Theories_Whitepaper.docx` and four `UOC_ToE_*` workbooks
(several hundred sheets total), archived under `source/`.

## What was done

1. **Implemented the graph construction exactly as directed**: `S_k = L_k ⊔ R_k`, `|L_k|=|R_k|=2^k`,
   intra-shell `K_{2^k,2^k}`, inter-shell `R_{k-1} × L_k`, `G_n = ⋃_{k=0}^n S_k`. Code:
   `reconstruction/build_arbs.py`. No checkpoint value (32, σ16, σ17, N/E targets) appears anywhere
   in the construction code — only `k`, shell cardinalities, and the two edge rules.
2. **Verified all structural and algebraic invariants (P1–P11)** for G0–G4: vertex/edge counts,
   symmetry, no self-loops, `L=D−A`, bipartiteness, connectedness (`dim ker L=1`), `L=BBᵀ`, the
   Dirac-squared block identity, and the `±σ_j ↔ λ_j=σ_j²` pairing. **All PASS, all five shells**
   (`reconstruction/proof_obligations_P1_P11.json`).
3. **Computed the complete spectra** (Laplacian eigenvalues and positive Dirac singular values) for
   G0–G4 and exported them as CSV + NumPy (`reconstruction/{adjacency,incidence,laplacian,dirac,spectra}/`).
4. **Compared against the 8 independent checkpoints already on record** (σ16/σ17 for G3, the
   degenerate boundary for G4, and t_H for all five shells, cross-checked via `λ_c=1/t_H`). t_H was
   **re-solved independently** from the complete spectrum by root-finding on
   `p_A(t)=mean(exp(-2tλ_j))=1/2`, not copied from the checkpoint sheet. **Every comparison matches
   to double-precision tolerance** (typically ~1e-13, worst case ~5e-11) — see
   `reconstruction/checkpoint_comparison.json` and `reconstruction/full_analysis_results.json`.
5. **Searched the newly supplied corpus for the construction's provenance.** Result, reported
   honestly regardless of the strong numerical match: the exact `K_{2^k,2^k}` / `R_{k-1}×L_k` rule
   does not appear anywhere in the ~3,000-row raw text corpus (`54_SOURCE_TEXT_CORPUS` sheet of
   `UOC_ToE_Canonical_Theory_of_Everything_Master_v1.0.xlsx`). The corpus's own source definitions
   (`ARBS-DEF-001`) describe ARBS as an Object-node/Operator-node bipartite typed-dependency graph —
   a different object. More strikingly, the same corpus contains an internal, dated
   **"Audit and Recommended Revisions"** document that states plainly: *"f(S_m), the shell-hierarchy
   fractal replacement rule, is asserted but never specified anywhere in the eight-document corpus
   (confirmed by exhaustive keyword and functional search)"* and that the source's own tested
   selector *"converges to near-complete graph, not the claimed Recursive Bipartite Shell Graph."*
   This is preserved as a transparency note (sheet 57), not as a reason to withhold the result: the
   construction was executed exactly as directed, and its output is judged by whether it reproduces
   the checkpoints — which it does, to double precision, across 8 independent numeric quantities.
6. **Re-executed C-004B and OPEN-020E.2** now that complete spectra exist:
   - `N_H(G_k) = rank(P_H,k)`, previously OPEN for lack of `λ_max`, is now directly computable:
     **`N_H = 0` for every shell G0–G4** — `λ_max(L_k) < λ_c,k` in every case, so the canonical
     threshold's horizon sector is empty everywhere, not just failing to isolate the G3 boundary.
     `C-004B = FALSIFIED FOR 32-BOUNDARY COMPATIBILITY` is confirmed and strengthened.
   - `rank(1_[λ16,λ17)(L_3))` = 1 (a single Laplacian eigenvalue between two adjacent sorted values,
     as any half-open interval between neighbors must contain). The **"32-state" language** is
     shown to correspond instead to the projector onto the **first 16 nonzero ±σ Dirac pairs**
     (`rank = 32`, confirmed by direct computation) — well-defined and isolated precisely because
     `σ16 < σ17` with a nonzero gap, but **why index 16 specifically** is the physically selected
     cutoff remains a separate, unresolved question: no target-independent selector in the source
     material picks out `k=16`.
   - Searched the new corpus for `δ_spec` and `σ` (the two objects OPEN-020E.2's `Π₀` formula
     needs) and found genuine source definitions this time: `δ_spec = λ₁(L)` (CERTIFIED, B-002,
     now directly computable from the complete spectra) and `σ` = entropy production, defined
     dynamically as `σ = −dF/dt` along a Fokker–Planck-type solution `P(t)` (CERTIFIED as existing
     and non-negative by an H-theorem, B-006) — but **never reduced to a static per-graph scalar**
     anywhere in the corpus: no fixed initial condition `P(0)` or evaluation time is recorded.
     `Π₀(G_k)` therefore **still cannot be evaluated** (Outcome D), but the blocking object has
     narrowed precisely: `δ_spec` is now known; only `σ_k` remains undefined, and inventing a choice
     of `P(0)`/time here would be exactly the fabrication this run's governing instructions forbid.
7. **G\* remains unresolved.** `N_H(G_k)` is identically 0 for all five shells (no distinguishing
   signal), `Π₀` cannot be evaluated for any shell, and no substrate-only uniqueness theorem exists
   in the source material (`BR-026`/`AU-002` both still OPEN there). Per Section 21's own rule, G3
   is **not** promoted on the strength of the spectral reconstruction succeeding — a favorable
   numerical result is not a proof.

## Final status

**ARBS-CONSTRUCTION-001 = DERIVED / VERIFIED.** Both the graph construction (P1–P11 all pass) and
the spectral reconstruction (8/8 independent checkpoints reproduced to double precision) succeeded.
This is a genuinely new, positive result — the prior run's STOP point (missing graph construction)
is resolved.

**G\* = UNRESOLVED** (unchanged). Reconstructing the graph and its spectrum does not, by itself,
answer which shell is physically selected; that question was never blocked on the graph's existence,
it is blocked on a selector theorem that still does not exist.

## Closure matrix (this run)

| Target | Result | Status | Dependencies |
|---|---|---|---|
| ARBS graph construction G0–G4 | All P1–P11 checks PASS | **DERIVED / VERIFIED** | Sections 1–4 rules only |
| Complete spectra {λ_k,j}, {σ_k,j} | Computed for all 5 shells | **DERIVED / VERIFIED** | Graph construction |
| Checkpoint reproduction (8 independent values) | All match to <2e-10 | **VERIFIED** | Complete spectra |
| C-004B | N_H(G_k)=0 for all k; canonical threshold empty everywhere | **FALSIFIED FOR 32-BOUNDARY COMPATIBILITY (confirmed, strengthened)** | Complete spectra |
| rank(P_boundary), G3 | 1 (Laplacian interval); 32 (Dirac ±pairs, first 16) | **CALCULATED** | Complete G3 spectrum |
| OPEN-020E.2 / Π₀(G_k) | Outcome D | **OPEN** — δ_spec now known; σ_k (entropy production) still undefined | δ_spec resolved; σ_k blocked |
| G* promotion | Not promoted | **UNRESOLVED** | No uniqueness theorem; N_H uninformative (=0 everywhere) |

## Falsification / provenance ledger (additions)

- **Construction provenance vs. numerical match**: the exact `K_{2^k,2^k}`/`R_{k-1}×L_k` rule is
  absent from the source corpus's own definitions and is explicitly flagged elsewhere in that same
  corpus as never having been specified — yet it reproduces 8 independent checkpoints to double
  precision when executed exactly as directed. Both facts are preserved side by side; neither is
  suppressed in favor of the other.
- **C-004B strengthened**: not merely "does not select the G3 boundary" but "produces an empty
  horizon sector for every one of the five tested shells."

## Proof-obligation ledger (updated)

| ID | Statement | Status this run |
|---|---|---|
| OBL-ARBS-CONSTRUCT | Recover/derive the ARBS graph construction | **RESOLVED** (executed, verified) |
| OBL-DELTA-SPEC | Define δ_spec(G_k) | **RESOLVED**: δ_spec = λ₁(L_k), computed for all shells |
| OBL-SIGMA-K | Define σ_k (entropy production, static) | **STILL OPEN** — dynamically defined in source, no static reduction given |
| OBL-GSTAR-SELECTOR | Prove a substrate-only uniqueness theorem for G* | **STILL OPEN** |

## Exactly one next unresolved upstream dependency

> **Define a concrete, per-shell, target-independent numeric value for `σ_k` (entropy production)
> as it enters `Π₀ = (δ_spec − λ_c)/σ`: the source defines `σ = −dF/dt` dynamically along a
> Fokker–Planck-type solution `P(t)` of `∂_t P = ℒ*P` relative to the stationary measure
> `P_ss(i) = d_i/(2|E|)`, but fixes neither an initial condition `P(0)` nor an evaluation time/rule
> reducing this to one number per graph. Until this is supplied by the source material (not
> invented here), `Π₀(G_k)` cannot be evaluated for any k, and the shell-selection question (G*)
> stays blocked on this together with the still-open substrate-only uniqueness theorem
> (`AU-002`/`BR-026`).**

# Universal Rosetta Stone — Closure / Derivation Run

**Run date:** 2026-08-18
**Master artifact (input):** `source/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.0.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.1.xlsx`
**Repository state at session start:** a single-line `README.md` only — no prior source code,
CSV, or checkpoint files existed in `BLZIX989/URSP`. All project state came from the four
supplied `.xlsx` files, now archived under `source/`.

## What was done

1. Loaded all four supplied workbooks (`MASTER_CALCULATION_WORKBOOK_v1.0`, `Master_Workbook`,
   `FULL_UNIFICATION_MATRIX`, `MDCL_Complete`) and inspected every sheet (108 sheets total)
   for the objects required by the governing instructions: the complete ARBS spectra
   `{λ_k,j}`/`{σ_k,j}` for k=0..4, the canonical ARBS recursive graph construction rule, and
   any additional numeric checkpoints beyond what v1.0 already lists.
2. Confirmed the repository itself carried no additional source material.
3. Independently re-verified, with exact rational/high-precision arithmetic (`mpmath`, 50
   significant digits) and, in the workbook, with live Excel formulas, every numeric checkpoint
   already present in v1.0: `σ² = λ` for the G3 boundary and the degenerate G4 boundary,
   `λ_c = 1/t_H` for G0–G4, the ordering `λ16 < λ17 < λ_c(G3)`, and `Δσ` for G3. All checks are
   internally self-consistent at double-precision tolerance (~1e-16 residuals, consistent with
   the source values having been produced in double precision). See `artifacts/checkpoint_verification.json`.
4. Searched explicitly for `ARBS-FULL-SPEC-001` — the ID the workbook itself cites as the
   provenance for every structural and spectral checkpoint — across all four workbooks and the
   repository. **No object with that ID, and no adjacency/incidence data or construction
   algorithm of any kind, exists anywhere in the supplied material.** Only the following are
   present: scalar `(N,E)` pairs per shell, four scalar `σ` values (G3, G4 boundary), and five
   scalar `(t_H, λ_c)` pairs. There is no edge list, no adjacency matrix, no recursion rule, and
   no full eigenvalue/singular-value array for any shell.
5. Per Section 5/20 of the governing instructions, **stopped exactly at this point**. No
   eigenvalues were invented, no graph was reverse-engineered from the target checkpoints, and
   no downstream step (C-004B's `N_H(G_k)`, `rank(P_boundary)`, OPEN-020E.2, G* promotion, finite
   NCG closure, flavor, continuum, or scale) was attempted, since each is strictly downstream of
   the missing datum in the governing dependency order `Γ ≺ ARBS ≺ G★ ≺ ...`.
6. Recorded everything above as new, fully-populated audit sheets appended to v1.1 (sheets
   48–56). No existing sheet or cell in the original 47 was altered or deleted.

One incidental observation, explicitly quarantined and **not used for any calculation**: the
five reported `(N,E)` pairs — `(2,1),(6,7),(14,31),(30,127),(62,511)` — exactly match the closed
form `N_k = 2^(k+2)−2`, `E_k = 2^(2k+1)−1`. This is a pattern-match over 5 points, not a
source-derived construction rule, and adopting it to generate a graph would be exactly the
forbidden move of shaping upstream structure to fit a known downstream/checkpoint outcome. It is
recorded in the Falsification Ledger as `OPEN / PROPOSED`, quarantined.

## A. Updated master workbook

`workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.1.xlsx` — all 47 original
sheets preserved verbatim, plus 9 new sheets:

| # | Sheet | Content |
|---|---|---|
| 48 | Spectral Reconstr Audit | Exhaustive per-file search log; STOP finding |
| 49 | Arithmetic Verification | Live formulas re-deriving σ²=λ, λ_c=1/t_H, ordering test |
| 50 | Threshold Candidate Table | Every source-supported threshold definition found (Section 8) |
| 51 | OPEN-020E.2 Audit | Π₀ evaluability test → Outcome D |
| 52 | Falsification Ledger | C-004B falsification; quarantined N/E pattern |
| 53 | Proof Obligation Ledger | 5 open obligations, dependency-ordered |
| 54 | Closure Matrix | Target / Result / Status / Dependencies |
| 55 | Canonical Dep Chain (Run) | ≺-chain state reached vs. blocked, this run |
| 56 | Next Dependency | The single next unresolved upstream target |

**Note on formula recalculation:** sheet 49's formulas (`=1/B{row}`, `=B{row}^2`, `=ABS(...)`,
`=IF(...)`, `=AND(...)`) could not be pre-computed by LibreOffice in this sandboxed execution
environment — `soffice --headless` hangs indefinitely (>5 min, confirmed on even a trivial
one-formula file) and never completes a conversion or macro pass here, for reasons unrelated to
this workbook's content. The formulas are simple, syntactically standard, and their results are
independently confirmed to full precision in `artifacts/checkpoint_verification.json` (produced
by the equivalent computation in `mpmath`, 50 digits). Opening the file in Excel or a working
LibreOffice instance will populate the cached values on first recalculation; nothing has to
change in the formulas themselves.

## B. Machine-readable numerical artifacts

- `artifacts/verify_checkpoints.py` — reproducible high-precision verification script.
- `artifacts/checkpoint_verification.json` — its output: every check, its inputs, and its
  pass/fail result.
- No spectral arrays (`{λ_k,j}`) or matrices (`G_k`, `B_k`, `L_k`, `D_{G,k}`) are included,
  because none exist in the source material and none were invented (Section 5, requirement 9).

## C. Closure matrix

| Target | Result | Status | Dependencies |
|---|---|---|---|
| Checkpoint arithmetic self-consistency | All checks pass (<1e-10 tolerance) | VERIFIED | Existing v1.0 checkpoints |
| C-004B (λ_c selects G3 32-boundary) | λ_c(G3)=23.135 > λ17(G3)=8.118 | **FALSIFIED FOR 32-BOUNDARY COMPATIBILITY** | λ_c=1/t_H; G3 boundary checkpoints |
| Complete ARBS spectra {λ_k,j}, k=0..4 | Cannot be reconstructed | **OPEN** | Missing ARBS construction rule |
| N_H(G0)…N_H(G4) | Cannot be calculated | OPEN | Requires complete spectra |
| rank(P_boundary) for G3 | Cannot be certified | OPEN | Requires full G3 eigenbasis |
| OPEN-020E.2 Π₀(G_k) / argmax | Outcome **D** — not evaluable | OPEN | δ_spec(G_k), σ_k both undefined in source |
| G* promotion (G*=G3) | Not promoted | **G\* UNRESOLVED** | No substrate-only uniqueness theorem found; BR-026 open |
| P_H^(32), rank=32 | Not attempted | BLOCKED | Requires G* derived |
| NCG / flavor / continuum / scale closure | Not attempted | BLOCKED | All strictly downstream of G* |

## D. Canonical dependency chain (this run)

```
Γ  ≺  ARBS (checkpoints only, NOT full construction)  ≺  G_k structural checkpoints (VERIFIED self-consistent)
   ≺  Spec(L_k) complete spectra  [NOT REACHED]
   ≺  G* (shell selection)        [NOT REACHED — G3 remains CANDIDATE only]
   ≺  P_H^(32), rank=32           [NOT REACHED]
   ≺  finite NCG closure          [NOT REACHED]
   ≺  Y_f, V_CKM, U_PMNS          [NOT REACHED]
   ≺  continuum closure           [NOT REACHED]
   ≺  absolute scale              [NOT REACHED]
```

## E. Numerical registry (newly calculated this run)

All in `artifacts/checkpoint_verification.json` and workbook sheet 49; summary:

- `λ_c(G_k) − 1/t_H(G_k)` residuals: G0 3.0e-16, G1 1.1e-16, G2 2.6e-16, G3 2.9e-16, G4 −3.8e-16 (all consistent).
- `σ16(G3)² − λ16(given)` = −2.4e-16; `σ17(G3)² − λ17(given)` = 2.0e-16 (consistent).
- `σ_G4² − 12` = 2.9e-15 (consistent with the reported degenerate boundary).
- `λ16(G3) < λ17(G3) < λ_c(G3)` = **True** (re-confirms C-004B falsification).

## F. Falsification ledger

1. **`λ_c = 1/t_H` as a 32-boundary selector — FAILED.** `λ_c(G3) = 23.1346 ≫ λ17(G3) = 8.1177`;
   the canonical threshold lies strictly above the entire observed boundary interval. Carried
   forward and re-confirmed: `C-004B = FALSIFIED FOR 32-BOUNDARY COMPATIBILITY`.
2. **`N_k=2^(k+2)−2, E_k=2^(2k+1)−1` as the canonical ARBS construction rule — NOT ADMITTED.**
   Reproduces all 5 checkpoints exactly, but has no source provenance; adopting it would be
   inventing the missing dependency. Quarantined as `OPEN / PROPOSED`, unused.

## G. Proof-obligation ledger

| ID | Statement | Blocks |
|---|---|---|
| OBL-ARBS-CONSTRUCT | Recover/derive the canonical ARBS recursive graph construction rule | Everything downstream |
| OBL-DELTA-SPEC | Define δ_spec(G_k) from an actual source registry entry | OPEN-020E.2 |
| OBL-SIGMA-K | Define the σ_k normalization in Π₀ | OPEN-020E.2 |
| OBL-GSTAR-SELECTOR | Prove a substrate-only uniqueness theorem selecting G* | G* promotion, everything downstream |
| BR-026 (source) | Horizon-selection projector generating selector | same as OBL-GSTAR-SELECTOR |

## H. Exactly one next unresolved upstream dependency

> **Recover or derive the canonical ARBS recursive graph construction rule
> (`ARBS-FULL-SPEC-001`): an explicit, target-independent algorithm producing the
> adjacency/incidence data of G0, G1, G2, G3, G4 — sufficient to build `L = D − A` and `B` with
> `B Bᵀ = L` directly from the construction, without reference to the 32-state target, the
> reported `(N,E)` checkpoints, or the reported `σ16/σ17` checkpoints.**

## Final governing test (Section 21)

*Does the substrate mathematics itself produce N_H = 32 without 32 entering any upstream
selector?*

**Answer: NO — not resolved either way.** The only target-independent selector with a complete
source definition (`λ_c = 1/t_H`) is falsified for this purpose (Section F.1). No other selector
in the source material is complete enough to test. The question cannot currently be answered
because the one object every downstream calculation needs — the actual ARBS graph — is not
present in any supplied source file. Per Section 20/21: the failure is preserved, not forced;
`G* ≠ G3` is not claimed and `G* = G3` is not claimed — **G\* is unresolved**, and G3 remains
recorded only as an independently verified spectral *candidate*, exactly as it was in v1.0.

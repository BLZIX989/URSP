# UOC-C0-SEED-CANONICALITY-002

**Run date:** 2026-08-18 (fourteenth closure run, following up `UOC-C0-MINIMAL-SEED-CLOSURE-001`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.3.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.4.xlsx`
**Computation:** `reconstruction/seed_closure/recompute.py`, `registry.py`, `closure.py`

## 1. Executive result

**CASE B, with a genuine and important structural finding.** Complete dependency closure does
**not** reduce `F_N/≅` to a single isomorphism class in general. Applying only the filters that are
*actually* independently derived from already-certified UOC dependencies (not invented for this run)
gives:

| N | `|F_N/≅|` (all fixed points) | `|F_N^derived/≅|` (after DERIVED-only filters) |
|---|---|---|
| 2 | 6 | **1** |
| 3 | 70 | **2** |
| 4 | 2462 | **6** |

`N=2` alone would look like a unique seed (**Case A** at that single size) — but the same
derivation applied at `N=3,4` gives 2 and 6 survivors respectively, so **general uniqueness fails**
and the honest verdict across the tested range is **Case B**: a surviving, non-unique family. Per
§11's own governing instruction, `N=2`'s apparent uniqueness is **not** promoted to a general theorem.

**The more important finding**, surfaced by actually running §9's spectral closure against these
survivors rather than skipping it: **the two independently-derived structural requirements are
logically incompatible with the historically-certified spectral machinery.** Every `F_N^derived`
survivor is, by construction, acyclic (nilpotent, `TH-ARBS-001B`). But every certified prior-run
spectral/persistence/thermodynamic construction (`Spec(L)`, heat kernel, diffusion distance) was
built and verified exclusively on **symmetric** weighted graphs. A nonempty **symmetric** relation
always contains a mutual edge pair `i↔j`, which is a directed 2-cycle — **incompatible with
acyclicity for any nonempty relation.** `Symmetric ∩ Acyclic = {∅}` exactly, at every `N` tested.
This is reported below as its own labeled result, not folded silently into the filter count.

## 2. C0 enumeration audit

Recomputed independently — **not** trusted from the prior run — using a structurally different
isomorphism method: `networkx` VF2 exact isomorphism on `DiGraph`s (with self-loop support),
cross-checked against the original permutation-minimization canonical form.

| N | raw relations | raw `Γ`-fixed relations | iso-classes (original method) | iso-classes (networkx VF2, independent) |
|---|---|---|---|---|
| 2 | 16 | 12 | 6 | **6** |
| 3 | 512 | 420 | 70 | **70** |
| 4 | 65536 | 59088 | 2462 | **2462** |

**No correction required.** Both methods agree exactly at every `N`. See
`reconstruction/seed_recompute_crosscheck.json`.

## 3. Corrections to previous analysis

None required to the fixed-point counts themselves (§2). One genuine **process correction** made
*during this run*, caught before it reached the report: the first draft of the active-filter set
included `symmetric` (labeled `DERIVED-CONDITIONAL`) among the canonical constraints, which produced
`F_N^derived = 0` at every `N` (an apparent falsification). Re-reading §6's own rule — *"Only:
VERIFIED, DERIVED, CALCULATED may be used as active canonical constraints"* — `CONDITIONAL` is a
distinct, listed status, not one of those three. `symmetric` was removed from the active set
accordingly (it remains fully reported in §9, just not used to eliminate candidates), giving the
`1/2/6` result in §1 instead. This is exactly the "recompute before using, do not blindly trust"
discipline the protocol demands, applied to my own intermediate output, not just the prior run's.

## 4. Fixed-point candidate registry

Full per-record registry: `reconstruction/seed_candidate_full_registry.json` (6 + 70 + 2462 = 2538
records, each with all fields listed in §3 of the protocol: adjacency matrix, degree sequences,
degree multiset, loop count, edge count, weak/strong connectivity, functionality,
injectivity/surjectivity, symmetry, antisymmetry, transitivity, acyclicity, component count,
`|Aut(R)|`, rigidity, adjacency spectrum (raw, generally complex — real/imaginary parts both
computed), symmetrized-adjacency spectrum, symmetrized-Laplacian spectrum, normalized-Laplacian
spectrum, spectral gap, rank, nullity, characteristic polynomial, minimal polynomial of the
symmetrized adjacency matrix).

## 5. Intrinsic invariant matrix

See §4's artifact. Two representation-invariance facts verified computationally, not assumed:
- `nilpotent_by_power == acyclic` (matrix-power nilpotency test vs. DFS cycle detection) —
  asserted with **zero exceptions** across all 2538 records.
- Every invariant reported is a function of the isomorphism class, not the raw labeling (verified
  directly in §12).

## 6. Selector / admissibility lattice

All filters tested, with **candidate count before/after** and **exact mathematical justification**
(`reconstruction/seed_filter_lattice.json`):

| Filter | Status | N=2 before→after | N=3 before→after | N=4 before→after |
|---|---|---|---|---|
| `rigid` (`Aut=1`) | UNJUSTIFIED | 6→6 | 70→70 | 2462→2462 |
| `minimal edge count` | UNJUSTIFIED (HEURISTIC ONLY, no threshold derivable) | — | — | — |
| `functional` | UNJUSTIFIED | 6→1 | 70→3 | 2462→6 |
| `weakly connected` | UNJUSTIFIED | 6→5 | 70→60 | 2462→2327 |
| `strongly connected` | UNJUSTIFIED | 6→1 | 70→20 | 2462→985 |
| `irreflexive` | **DERIVED** (logical consequence of `TH-ARBS-001A`) | 6→1 | 70→7 | 2462→136 |
| `reflexive` | UNJUSTIFIED, and incompatible with the derived result above | 6→1 | 70→7 | 2462→136 |
| `symmetric` | **DERIVED-CONDITIONAL** (precondition for reusing certified spectral machinery unmodified — not an unconditional seed requirement) | 6→2 | 70→4 | 2462→16 |
| `antisymmetric` | UNJUSTIFIED | 6→5 | 70→30 | 2462→430 |
| `transitive` | UNJUSTIFIED | 6→5 | 70→20 | 2462→111 |
| `acyclic` (`TH-ARBS-001B`, nilpotency) | **DERIVED** | 6→1 | 70→3 | 2462→17 |
| `bipartite` (`TH-ARBS-001A`) | **DERIVED** | 6→1 | 70→4 | 2462→23 |
| `nontrivial spectral gap` | UNJUSTIFIED (no certified threshold) | 6→5 | 70→60 | 2462→2327 |
| `Laplacian nullity=1` (connected) | UNJUSTIFIED | 6→5 | 70→60 | 2462→2327 |

`reflexive`/`irreflexive` and `nontrivial-spectral-gap`/`Laplacian-nullity=1` show matching counts at
every `N` by coincidence of this candidate pool, not because the pairs are the same condition or the
same records — each was individually verified against the raw registry to rule out a computation bug
before being reported here.

**Do not read this table as a ranked funnel** — most rows are independent, non-nested tests on the
*same* starting set `F_N`, not sequential eliminations; only the `DERIVED` rows are actually chained
(§14).

## 7. Derivation-status matrix

| Status | Filters carrying it |
|---|---|
| **DERIVED** | `irreflexive`, `acyclic`/`TH-ARBS-001B`, `bipartite`/`TH-ARBS-001A` |
| **DERIVED-CONDITIONAL** | `symmetric` (conditional on reusing unmodified certified spectral machinery) |
| **UNJUSTIFIED / PROPOSED / HEURISTIC ONLY** | `rigid`, `minimal edge count`, `functional`, `weakly/strongly connected`, `reflexive`, `antisymmetric`, `transitive`, `nontrivial spectral gap`, `Laplacian nullity=1` |
| **BLOCKED** | Persistence (`Π_R`, both notions found in corpus), geometry/curvature (§11) |

Per §0.4/§0.6, **only the three `DERIVED` rows entered the active canonical calculation.**

## 8. `D_R`, `T_R`, `C_R` reconstruction

Recomputed for every one of the 2538 records using only the canonical C0 constructions:

- **`D_R`**: coarsest equitable (color-refinement) partition — well-defined for every record
  (**PROVEN**, unconditional).
- **`T_R`**: unique successor `τ(x)=y` **only** when `R` is functional. Functional-`F_N` counts:
  `1/3/6` at `N=2/3/4` (see §6 table). For non-functional `R` (the overwhelming majority), the only
  canonically available transformation object is `Aut(R)` (a group, generally non-unique — no
  arbitrary function was substituted for a nonfunctional relation, per the explicit prohibition in
  §4 of the protocol). Classified: **CONDITIONAL** (functional case), **PROPOSED-ONLY** otherwise
  (the "canonical transformation object" for a nonfunctional relation is `Aut(R)`, not a function).
- **`C_R`**: `C_R(T):=1[T(R)=R]` — well-defined for every record (**PROVEN**).

## 9. Spectral closure

Computed `A_R`, `A_sym,R`, `D_R`, `L_R=D_R-A_sym,R`, `Spec(A_R)` (raw, complex-valued in general),
`Spec(A_sym,R)`, `Spec(L_sym,R)`, `Spec(L_norm,sym,R)` for **every** record.

- **Observed vs. required, explicitly separated** (`reconstruction/seed_spectral_closure.json`):
  `symmetric ⟹ real spectrum` verified with zero exceptions (a required mathematical fact for
  symmetric matrices). Among **non**-symmetric candidates, a real spectrum is still **observed**
  surprisingly often (`4/4`, `57/66`, `1464/2446` at `N=2/3/4`) — but this is **not** a general
  requirement of the certified machinery, only an empirical fact about this particular candidate pool
  (flagged exactly per §7's instruction to keep "observed" separate from "required").
- **The `F_N^derived` survivors' raw adjacency spectrum is trivial** — every one of the 9 survivors
  (1+2+6) is nilpotent by construction (§1), and nilpotent matrices have **all-zero** eigenvalues
  necessarily (not a discovery, a direct consequence of nilpotency). The raw adjacency spectrum
  therefore carries **zero** distinguishing information among the derived survivors; the
  symmetrized-Laplacian spectrum is the only spectral quantity that differentiates them (e.g. four
  of the six `N=4` survivors share the identical symmetrized-Laplacian spectrum
  `[0, 0.293, 1.0, 1.707]` despite being non-isomorphic as *directed* graphs — symmetrization
  discards orientation information, a genuine spectral-degeneracy finding, not an error).
- **No non-arbitrary spectral admissibility requirement was found or invented.** `F_N^(spectral) =
  F_N^derived` unchanged — no new elimination performed at this step, honestly reported as such
  rather than manufacturing a spectral filter to look productive.

## 10. Persistence closure

**BLOCKED.** Both persistence notions present anywhere in this corpus are open, not just one:

- SIT's `Π(K):=Σ_{n:λ_n<λ_gap}√λ_n` — undefined without `λ_gap`, itself established as an unfixed,
  undocumented free parameter in this project's own prior runs (`ARBS-GRAPH-REALIZATION-001`,
  `KIJ-THETA-IMAGE-RECOVERY-001`).
- The Architecture-layer `Π_O = f(σ,C,Spec(L))` — separately recorded `OPEN` in source
  (`DER-ORG-007`: "coupling equation proposed... not executed").

**Consequence:** `F_N^(persistence) = F_N^(spectral)` unchanged. No candidate elimination possible
here without inventing `λ_gap`, which §0.3/§0.4 forbid. Full detail:
`reconstruction/seed_persistence_geometry_closure.json`.

## 11. Persistence → geometry closure

Diffusion distance `d(i,j)` (which depends only on `Spec(L)`, **not** on the blocked `Π`) is
computable for the symmetric candidates in principle — but the derived survivors are never
symmetric (§1's incompatibility finding), so this step is moot for them specifically without first
resolving the symmetric/acyclic tension.

**Metric tensor `g_μν` and curvature: BLOCKED.** A 2-, 3-, or 4-point discrete metric space does not
support a meaningful continuum curvature tensor — this machinery was only ever exercised in prior
runs on the *growing* `tilde_G_k` family at large shell index (thousands of vertices), never on a
handful of points. This is exactly the unresolved `N→∞`/canonical-family question of §12, not a new
obstruction — recorded as `BLOCKED`, missing dependency = resolution of §12, no ad hoc interpolation
introduced.

## 12. Isomorphism-invariance audit

138 permutation trials (20 random candidates per `N`, 3 random relabelings each): canonical form and
`|Aut(R)|` preserved **exactly** in all 138/138 trials (`reconstruction/seed_isomorphism_invariance_audit.json`).
`Selector(PRP⁻¹) = Selector(R)` verified directly, not assumed.

## 13. N-scaling audit

| Quantity | N=2 | N=3 | N=4 |
|---|---|---|---|
| `|F_N|` | 6 | 70 | 2462 |
| `|F_N^derived|` | **1** | **2** | **6** |

`|F_N^derived|` is **not constant** across the tested range — it grows (1→2→6), the same
qualitative pattern as the unfiltered family. **No infinite-limit theorem is inferred from `N≤4`**,
per explicit instruction. The apparent `N=2` uniqueness is reported as a scale-specific fact, not
extrapolated.

## 14. Surviving candidates

All 9 `F_N^derived` survivors, exact adjacency matrices (`reconstruction/seed_derived_survivors.json`
for IDs, `seed_candidate_full_registry.json` for full records):

```
N=2 (1 survivor):  [[0,0],[1,0]]

N=3 (2 survivors): [[0,0,0],[0,0,0],[0,1,0]]
                    [[0,0,0],[0,0,1],[1,0,0]]

N=4 (6 survivors): [[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,1,0,0]]
                    [[0,0,0,0],[0,0,0,0],[0,1,0,0],[1,0,1,0]]
                    [[0,0,0,0],[0,0,0,0],[0,1,0,0],[1,1,0,0]]
                    [[0,0,0,0],[0,0,0,1],[0,1,0,0],[1,0,0,0]]
                    [[0,0,0,0],[0,0,0,1],[1,0,0,0],[1,0,0,0]]
                    [[0,0,0,0],[0,0,0,1],[1,1,0,0],[1,0,0,0]]
```

All are rigid (`Aut(R)=1`), sparse (2–4 edges), directed acyclic, bipartite-underlying.

## 15. Unique-seed test

Per the §Final Certification Rule's seven conditions: condition 1 (*exactly one isomorphism class
survives*) holds **only at `N=2`**, fails at `N=3,4`. **No unique-seed certification is issued.**

## 16. Family-seed test (uniqueness failed)

§12's request: is there a canonical refinement `R_N ↪ R_{N+1}`? A structural pattern is visible but
**not proven as a categorical construction** this run: every `F_N^derived` survivor is a sparse DAG
on a bipartite skeleton, and the `N=2` survivor's edge `(1,0)` appears as a sub-pattern inside several
`N=3`/`N=4` survivors under some relabeling — but no canonical (representation-invariant, uniquely
defined) embedding map was constructed or proven, and **no claim of a direct/inverse/projective
system is made.** This is left explicitly **OPEN**, not asserted, per §12's own instruction not to
assume a limit exists without proof.

## 17. Blocked dependencies

- Persistence `Π_R` — blocked on `λ_gap` (open, established in prior runs).
- Metric/curvature — blocked on insufficient `N` / unresolved family-vs-limit question (§16).
- Canonical `R_N↪R_{N+1}` embedding — not constructed, left open.

## 18. Falsified conditions

- **`Symmetric ∩ Acyclic = {∅}`** for any nonempty relation — a genuine structural incompatibility
  between the (conditionally-derived) spectral-reuse requirement and the (unconditionally-derived)
  `TH-ARBS-001B` nilpotency requirement, proven directly (mutual edge ⟹ 2-cycle ⟹ not nilpotent).
- Naive assumption that `N=2`'s unique survivor generalizes: **falsified** by direct computation at
  `N=3,4`.

## 19. Verified results

- `F_2=6, F_3=70, F_4=2462` — cross-validated by two independent isomorphism methods, zero
  discrepancy.
- `nilpotent ⟺ acyclic` for the tested candidates — verified with zero exceptions.
- Isomorphism-invariance of canonical form and `|Aut(R)|` — verified, 138/138.
- `F_N^derived = 1, 2, 6` at `N=2,3,4` under the three genuinely `DERIVED` filters.

## 20. Proposed results (not certified)

- `symmetric` as a spectral-machinery precondition (CONDITIONAL, not used for elimination).
- Every filter listed `UNJUSTIFIED` in §6/§7 — reported with exact survivor counts for future use,
  never used to certify a seed.

## 21. Next dependency

> **Resolve the `symmetric`/`acyclic` incompatibility discovered this run** — either by finding an
> independently-certified extension of the spectral/persistence machinery to genuinely asymmetric
> (directed) graphs (so the `TH-ARBS-001B`-derived survivors become spectrally tractable on their own
> terms), or by finding a source-derived reason the seed need not itself carry the nilpotency
> requirement directly (e.g. nilpotency applies to a *transport operator derived from* `R`, not `R`
> literally, reopening the symmetric branch) — **or** extend the exhaustive enumeration past `N=4` to
> determine whether `|F_N^derived|` keeps growing (as `N=2→3→4`'s `1→2→6` suggests) or eventually
> stabilizes. None of these three is resolvable by further reasoning from the currently available
> corpus and computation.

## Final certification

Per the protocol's own Final Certification Rule: **`R*` is NOT certified as "the correct seed."**
Exactly one isomorphism class survives only at `N=2`; the same derivation gives 2 and 6 survivors at
`N=3,4`, so condition 6 (*survives the tested N-scaling*) fails. The surviving family
(`reconstruction/seed_derived_survivors.json`) is reported in full, together with the precise
unresolved dependency (§21) that would need to close before uniqueness could be certified.

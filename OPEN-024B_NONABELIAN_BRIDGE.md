# OPEN-024B (non-abelian) — Commutant NCG Functor Bridge

**Run date:** 2026-08-18 (continuing directly from `OPEN-024B` asymmetric, frozen and reused, not
re-derived)
**Executable code:** `reconstruction/toe_rebuild/compiler/ncg_nonabelian_bridge.py`,
`reconstruction/toe_rebuild/run_nonabelian_bridge.py`, `reconstruction/toe_rebuild/run_nonabelian_full.py`

## Frozen prior results (reused, not re-run as open)

`SEMANTIC-FUNCTOR-BRIDGE-001` and `OPEN-024B` (asymmetric) jointly proved
`THM-ASYM-BRIDGE-OBSTRUCTION-001`: for **any** representation (symmetric or asymmetric) of the
maximal abelian algebra `A_F = ℂ^N`, first-order forces `D_F=0`. This is not re-tested here. This
run changes **exactly one** ingredient: the algebra.

## Result: a canonical non-abelian algebra closes first-order but breaks order-zero — Outcome B

`A_seed := Comm(D_F)`, the commutant of the seed's own already-derived Hermitian `D_F`, is
canonically derivable with zero free parameters (standard linear algebra: `D_F` Hermitian ⟹
`Comm(D_F) = ⊕_λ End(E_λ)` over its eigenspace decomposition). It is **non-abelian for 56/259
seeds** (11/23 at N=4, 45/231 at N=5, 0/1 at N=2, 0/4 at N=3) — the first genuinely non-abelian,
seed-derived structure found in the entire investigation. For every one of these 56 seeds:
**first-order holds exactly** (residual ~5×10⁻¹⁶, the first time first-order has ever held in this
project) but **order-zero fails exactly** (residual = 1.0, exact, for every representation
candidate tested). Both are proven as general theorems, not merely observed.

## 2. Non-abelian structure (per the task's own definition)

Non-abelian requires ∃a,b with `[a,b]≠0` **and** ∃ irrep of dim >1. Both hold: `Comm(D_F)` has
block structure `(1,1,2)` at N=4 and `(1,1,3)` at N=5 whenever degenerate — one multi-dimensional
irrep (dim 2 or 3) plus two 1-dimensional (scalar/abelian) blocks. Center = number of blocks (3 in
both cases, since each block contributes one central idempotent). Full per-seed data:
`nonabelian_seed_algebra_registry.json`.

## 3. Target-independence firewall

Construction inputs were exclusively `D_F` (seed-derived, proven Hermitian in prior runs), its
eigenspace decomposition, and the unchanged swap-conjugate `J0`. Scan of the construction files
(`ncg_nonabelian_bridge.py`, `run_nonabelian_bridge.py`) for SU(3)/SU(2)/U(1)/G_SM/hypercharge/
color/weak isospin/quarks/leptons/generations/CKM/PMNS/Standard Model: **zero hits, both files
clean**. Physical target terms appear only in §16 below and in the firewall documentation itself.
Full detail: `nonabelian_target_independence.json`.

## 4. Candidate-generation mechanisms (Section 4, dependency order)

- **4A (endomorphism algebra, `M_N(ℂ)`):** trivially non-abelian but carries zero seed information
  (doesn't depend on `R` at all). Tested as **Control F** (§14): both order-zero and first-order
  fail (first-order residual 2.0) — a strictly worse starting point than 4B.
- **4B (commutant, `Comm(D_F)`):** the construction used. Prioritized because it is the smallest
  non-arbitrary algebra that (a) is seed-derived (depends on `R` via `D_F`) and (b) automatically
  satisfies first-order by definition (`[D_F,a]=0` for `a∈Comm(D_F)`).
- **4C/4D (path/incidence, relation-composition):** not independently constructed. Since these
  would also be built from `R`'s real adjacency matrix, `THM-NAB-ORDER-ZERO-OBSTRUCTION-001` (§12)
  predicts the same order-zero obstruction recurs for any non-abelian algebra they might produce —
  reported as a predicted, not independently verified, consequence.
- **4E (bipartite operator algebra, `T:H_R→H_L`):** same deferral as 4C/4D, same reasoning.
- **4F (hyperedge algebra):** **N/A** — `F_N^derived_v2`'s relations are ordinary binary
  relations; no hyperedge structure exists to build an algebra from.
- **4G (typed dependency algebra):** not applicable to this seed family for the same reason as 4F.

## 5. Minimality

`K(A) := dim_ℂ(A)`. `Comm(D_F)` is the *full* centralizer (largest, not smallest, algebra
commuting with `D_F`), but minimal in the sense of using zero free parameters and automatically
satisfying first-order. `Comm(D_F)` is a **deterministic function of `D_F`** — unique per seed —
but 56 inequivalent non-abelian instances exist across seeds with no internal invariant found this
run that privileges one. **STATUS: PROVEN NON-UNIQUE** at the seed level (`THM-NAB-010`), consistent
with every prior run (Track A never selects one canonical seed).

## 6. Representation recovery

Irreps: at N=4, dims `(1,1,2)`; at N=5, dims `(1,1,3)`. Smallest `dim(V_i)>1` is 2 (N=4) / 3 (N=5).
Selection criterion is internal: the defining/inclusion representation on `H_F^bare=ℂ^N` is the
**unique** faithful representation compatible with the seed's own eigenspace decomposition, since
every non-abelian seed found has each block occurring with multiplicity exactly 1 (`THM-NAB-003`).

## 7. `H_F`

`H_F = ℂ^N ⊕ ℂ^N`, dim `2N`, determined by the seed's own vertex count — **not** forced to 32 (dim
8 at N=4, dim 10 at N=5).

## 8. Asymmetric `π_L≠π_R`

Tested three predefined, seed-motivated candidates for `π_R`: **identity** (`π_R=a`), **inner
automorphism** (`π_R(a)=UaU⁻¹` for `U` unitary within each block — by Skolem–Noether this exhausts
*every* automorphism of a full matrix-algebra block, so it is the entire "genuinely different
representation" freedom available when each irrep has multiplicity 1, which is always the case
here), and **conjugate** (`π_R(a)=conj(a)`, ℝ-linear but not ℂ-linear — same caveat as the prior
asymmetric run). **All three give the identical verdict** on every one of the 56 non-abelian seeds:
order-zero fails (residual exactly 1.0), first-order holds (residual ~5×10⁻¹⁶) — proven
basis-independent (`THM-NAB-004`), not merely a coincidence of which representative was tried.
Full data: `nonabelian_representation_registry.json`.

## 9. `J_F` / KO-dimension

Standard swap-conjugate `J0`, unchanged from `ncg_bridge.py`. KO-dimension: `{0,6} mod 8`,
determined by the same external doubling-sign convention as every prior run, unaffected by
`A_seed`'s abelian/non-abelian status (`THM-NAB-007`).

## 10. `D_F`

Unchanged: `D_F = N_orient(R) + N_orient(R)ᵀ`. Zero free parameters, no Yukawa couplings, every
nonzero entry traces directly to `R`'s own edges.

## 11. Complete finite triple (witness: N=4 seed, `block_dims=(1,1,2)`)

| Axiom | Result |
|---|---|
| Grading (`γ_F²=1`, anticommutes with `D_F`) | **PASS** |
| Hermiticity | **PASS** |
| Reality (`J0`, unchanged) | **PASS** (phase-1/2 verification reused) |
| Order-zero | **FAIL** (residual 1.0, exact) |
| First-order | **PASS** (residual ~5×10⁻¹⁶) |
| Faithfulness | **PASS** (inclusion representation) |
| Poincaré duality | **DEFERRED** (stop condition — order-zero fails first) |
| Orientability | **DEFERRED** (stop condition) |

Full data: `nonabelian_spectral_triple_registry.json`.

## 12. Theorem registry (`nonabelian_theorem_registry.json`)

- **THM-NAB-001–004:** non-abelian algebra exists (PROVEN), multi-dim irrep exists (PROVEN),
  representation is canonical (PROVEN), order-zero/first-order verdict is representation-choice
  invariant (VERIFIED).
- **THM-NAB-ORDER-ZERO-OBSTRUCTION-001 (PROVEN, general):** for *any* subalgebra `A⊆M_N(ℂ)` with
  `conj(A)=A` (automatic for any real-matrix-derived algebra — true of every Track A construction),
  combined with `π(a)=diag(a,a)` (or the inner-automorphism/conjugate variants) and the standard
  swap-conjugate `J`, order-zero holds **iff `A` is abelian**. *Proof:* `Jπ_R(b)J⁻¹ = diag(conj(b),
  conj(b))`, so order-zero reduces to `[a,conj(b)]=0 ∀a,b∈A`; since `conj:A→A` is a bijective
  involution, this is equivalent to `[a,c]=0 ∀a,c∈A`, i.e. `A` abelian. □ This is a **general no-go
  theorem covering every candidate mechanism in §4A–4G**, not an artifact of the commutant
  construction specifically.
- **THM-NAB-005 (PROVEN):** order-zero fails on all 56/56 non-abelian seeds, all 3 representation
  candidates — direct corollary of the theorem above.
- **THM-NAB-006 (PROVEN):** first-order holds on all 56/56 non-abelian seeds, all 3 candidates
  (`[D_F,a]=0` by definition for `a∈Comm(D_F)`, independent of seed or `π_R` choice).
- **THM-NAB-007 (VERIFIED):** KO-dimension unchanged, `{0,6}`.
- **THM-NAB-008/009 (OPEN, deferred):** Poincaré duality, orientability — not evaluated (no closed
  triple exists).
- **THM-NAB-010 (PROVEN NON-UNIQUE):** `A_seed` unique per seed, non-unique across seeds, no
  internal selector found.

## 13. Full seed sweep

| N | n_seeds | n_nonabelian | given non-abelian: OZ pass | FO pass | BOTH |
|---|---|---|---|---|---|
| 2 | 1 | 0 | — | — | — |
| 3 | 4 | 0 | — | — | — |
| 4 | 23 | 11 | 0/11 | 11/11 | 0/11 |
| 5 | 231 | 45 | 0/45 | 45/45 | 0/45 |

**Totals: 56/259 seeds non-abelian; 0/56 order-zero pass; 56/56 first-order pass; 0/56 both pass.**
Zero exceptions across N and across all 3 representation candidates (168 total pass/fail
evaluations for order-zero, 168 for first-order).

## 14. Controls (A–G)

- **A (remove relation, `D_F=0`):** `Comm(D_F)=M_N(ℂ)`, maximally non-abelian but physically
  vacuous (no seed relation at all).
- **B (randomize edges, same N/edge-count):** 23/50 random sparse bipartite trials at N=4 also show
  eigenvalue degeneracy — **honest finding: degeneracy is not unique to `F_N^derived_v2`'s rigid
  Γ-fixed structure; it is fairly generic for sparse 0/1 matrices at this size.**
- **C (randomize relation preserving bipartition):** subsumed by B (B's construction already
  respects a fixed bipartition coloring).
- **D (randomize topology preserving degree sequence):** implemented as vertex relabeling
  (permutation similarity) — **honestly flagged as uninformative**, since permutation similarity
  trivially preserves the spectrum of `D_F`; a genuine degree-preserving rewiring was not
  implemented this run.
- **E (maximal abelian algebra):** reference to the prior run's result (order-zero always passes,
  first-order always fails).
- **F (generic `M_N(ℂ)`, same dimension, not seed-derived):** **both order-zero and first-order
  fail** (first-order residual 2.0, vs machine precision for `Comm(D_F)`) — isolates that
  first-order's pass is specifically because `A⊆Comm(D_F)`, not a generic property of any
  non-abelian algebra of the right size.
- **G (asymmetric→identical):** covered by the "identity" representation candidate in §8 — order-zero
  fails there too, so asymmetry was never masking a real pass.

Full data: `nonabelian_control_results.json`.

## 15–16. Physical target comparison — structural comparison only, no derived match

At N=4, `A_seed = ℂ⊕ℂ⊕M_2(ℂ)` — a direct sum with two abelian summands, **not simple**; `U(A_seed) =
U(1)×U(1)×U(2)`, not `SU(2)`. At N=5, `A_seed=ℂ⊕ℂ⊕M_3(ℂ)`, giving `U(1)×U(1)×U(3)`, not `SU(3)`. The
matching irrep *dimensions* (2, 3) are the only coincidence; the group structure does not match
`SU(2)` or `SU(3)` (those are simple, unitary-determinant subgroups; `U(A_seed)`'s factors are the
full unitary groups of each block, with extra abelian `U(1)` factors from the 1-dim blocks, and no
determinant constraint). Construction was completely target-independent (§3); this comparison is
reported only because the task requires it after independent derivation. **VERDICT: STRUCTURAL
COMPARISON ONLY — no DERIVED MATCH claim.**

## 17–18. Information-theoretic / spectral connection

`A_seed=Comm(D_F)` is by definition already fully encoded by `D_F`, which is itself already encoded
by `R`'s canonical orientation — no independent information beyond `D_F`'s own spectrum multiplicity
structure. `D_F` itself is **unchanged** in this run's construction, so the prior run's exact,
already-proven result applies directly and was not re-derived: `D_F² ≠ L` (verified exactly for all
28 seeds at N≤4, no shifted relation either — `ncg_df_laplacian_relation.json`,
`test_D_F_squared_not_equal_laplacian`).

## 19. Bridge-closure test (14-point checklist)

Non-abelian ✓, seed-derived ✓, irrep dim>1 ✓, canonical selection ✓, asymmetric L/R N/A (proven
irrelevant) ✓, seed-derived `D_F` ✓, grading ✓, Hermiticity ✓, reality ✓, **order-zero ✗ — FIRST
FAILURE**, first-order ✓ (not reached by the stop rule, but tested and passes), faithfulness ✓,
Poincaré duality DEFERRED, orientability DEFERRED. **Per Section 19: STOP at order-zero.**

## 20. "Do not patch failure" compliance

`D_F` was not altered to force order-zero (its construction is unchanged from every prior run).
`J_F` was not altered — three natural, predefined `J`-compatible representation choices were tested
and all failed identically, which was reported as a proof, not patched around. The algebra was not
enlarged by fiat to force closure. The failure is reported as `THM-NAB-ORDER-ZERO-OBSTRUCTION-001`,
a general theorem, exactly as this section requires.

## 21. Target-independence firewall — see §3.

## 22. Numerical reproducibility

All computations exact-arithmetic-adjacent: `numpy.linalg.eigh` on real-symmetric `D_F` (machine
precision, ~1e-15), tolerance 1e-8 for commutator tests, tolerance 1e-6 for eigenvalue-degeneracy
detection. Every theorem's numerical claim is backed by an exact analytic proof (§12), not solely a
pass-rate. Randomized controls (B, D, inner-automorphism trials) use fixed seeds
(`np.random.default_rng(20260818)`, `123`, `7`, `42`) for reproducibility.

## 23. Artifacts

`OPEN-024B_NONABELIAN_BRIDGE.md` (this file), `reconstruction/nonabelian_seed_algebra_registry.json`,
`nonabelian_representation_registry.json`, `nonabelian_spectral_triple_registry.json`,
`nonabelian_theorem_registry.json`, `nonabelian_control_results.json`,
`nonabelian_target_independence.json`, `nonabelian_bridge_results.json`,
`nonabelian_projection_map.json`. Executable: `reconstruction/toe_rebuild/compiler/ncg_nonabelian_bridge.py`,
`reconstruction/toe_rebuild/run_nonabelian_bridge.py`, `reconstruction/toe_rebuild/run_nonabelian_full.py`.
16/16 tests passing (`reconstruction/toe_rebuild/tests/test_compiler.py`).

## 24. Workbook

`workbook/build_v2_9.py` → `Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.9.xlsx`, 309
sheets (280 preserved + 29 new `NAB-001`…`NAB-029`).

## 25. Required tables — see §11 (finite triple), §13 (seed sweep), §14 (controls), §12 (theorem
registry) above.

## 26. Final report — questions A–S

**A.** `A_seed := Comm(D_F)`, the commutant of the seed's own Hermitian Dirac operator.
**B.** Standard external linear algebra: `Comm(D_F)=⊕_λEnd(E_λ)` over `D_F`'s eigenspace
decomposition — non-abelian iff `D_F` has a repeated eigenvalue.
**C.** 3 blocks (2 scalar + 1 non-trivial) at both N=4 and N=5 — center dim = 3.
**D.** `(1,1,2)` at N=4, `(1,1,3)` at N=5.
**E.** 2 (N=4) / 3 (N=5).
**F.** Unique faithful representation compatible with the seed's own eigenspace decomposition
(multiplicity-1 blocks in every seed found) — internal, not physical.
**G.** `ℂ^N⊕ℂ^N`, dim `2N` (8 at N=4, 10 at N=5) — not forced to 32.
**H.** `π_L=` inclusion; `π_R∈{identity, inner-automorphism, conjugate}` — all three proven
equivalent in verdict (`THM-NAB-004`).
**I.** Standard swap-conjugate `J0`, unchanged from prior runs.
**J.** `D_F = N_orient(R)+N_orient(R)ᵀ`, unchanged, zero free parameters.
**K.** `{0,6} mod 8`, unchanged, set by the doubling convention not by non-abelian-ness.
**L.** **NO** — fails universally, 0/56, proven (`THM-NAB-005`/`ORDER-ZERO-OBSTRUCTION-001`).
**M.** **YES** — holds universally, 56/56, proven (`THM-NAB-006`) — first time in this project.
**N.** Not tested — deferred per the stop condition (order-zero fails first).
**O.** Not tested — same deferral.
**P.** `Comm(D_F)` is canonical *given a seed*; non-unique *across* seeds (`THM-NAB-010`).
**Q.** Survives inner-automorphism and conjugate-representation controls identically (same
residuals) — but the D_F=0 control (A) and the M_N(ℂ) control (F) both show the result is
NOT vacuous or generic: F fails first-order too, proving `Comm(D_F)`'s specific structure is
load-bearing.
**R.** No — `U(A_seed)` is `U(1)×U(1)×U(d)`, not simple, not `SU(2)`/`SU(3)` (§15–16). Structural
comparison only.
**S.** Order-zero, per `THM-NAB-ORDER-ZERO-OBSTRUCTION-001`: closing the bridge would require
either (a) a fundamentally different real structure `J` not of swap-conjugate form, or (b) a
genuinely representation-*inequivalent* `π_R`, which requires an algebra with multiple inequivalent
irreps of compatible dimension — a structure none of the 259 admissible seeds through N=5 possess.

## 27. Outcome classification

**B — canonical non-abelian algebra + triple; exactly one axiom (order-zero) remains unresolved**,
for a proven general reason, not an open question awaiting more computation.

## 28. Stop condition

Stopping here, at order-zero, per Section 19/28's explicit instruction. Not proceeding to
matter/generations/Yukawa/CKM/PMNS/constants/cosmology, since the finite non-abelian NCG bridge is
not closed.

## 29. Governing-principle compliance

This run changed exactly one structural ingredient (the algebra, `A_F=ℂ^N` → `A_seed=Comm(D_F)`)
from the frozen prior result. A non-abelian algebra *did* emerge, canonically, and was derived
(§2–§10). It did not close the triple; the reason is proven, not assumed (§12). Several
non-canonical instances exist across seeds (56), and no internal seed invariant was found to select
one canonically — recorded honestly as `THM-NAB-010`, PROVEN NON-UNIQUE, per this section's own
instruction.

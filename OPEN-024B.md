# OPEN-024B — Asymmetric NCG Functor Bridge

**Run date:** 2026-08-18 (eighteenth closure run, continuing from `SEMANTIC-FUNCTOR-BRIDGE-001`)
**Executable code:** `reconstruction/toe_rebuild/compiler/ncg_asymmetric_bridge.py`,
`reconstruction/toe_rebuild/run_asymmetric_bridge.py`

## Result: the obstruction is deeper than "symmetric vs asymmetric" — it's the algebra

`SEMANTIC-FUNCTOR-BRIDGE-001` proved that identical particle/antiparticle representations force
`D_F=0`. This run tested the natural next question — does genuine asymmetry fix it? — with a
predefined, declared-in-advance search space (per this run's own §6/§13): `identity` (control),
`conjugate`, `orientation_reversed` (seed-derived, from `R`'s own bipartition), and
`random_diagonal_perm` (a structureless negative control). All four, across all 259 seeds, both KO
sign conventions: **order-zero passes universally, first-order fails universally.** Asymmetry alone
does not help.

## A. Exact representation convention used

`π(a) = diag(π_L(a), π_R(a))` block-diagonal on `H_F = ℂ^N ⊕ ℂ^N`, with `π_L(a) = diag(a)` fixed
and `π_R` varying across the four candidates below.

## B. The candidate search space (declared before testing)

| Candidate | Formula | Classification |
|---|---|---|
| `identity` | `π_R(a)=π_L(a)` | GENERIC — the previous run's failing baseline |
| `conjugate` | `π_R(a)=conj(π_L(a))` | GENERIC |
| `orientation_reversed` | swap `X0`/`X1` diagonal entries (defined only when `\|X0\|=\|X1\|`) | **SEED-DERIVED** |
| `random_diagonal_perm` | fixed pseudorandom permutation | GENERIC, negative control |

**Validity audit** (performed *after* computation, reported honestly rather than hidden): `conjugate`
is **not** actually a valid ℂ-algebra representation — it's ℂ-antilinear, not ℂ-linear (verified
directly: `π_R(i·a) ≠ i·π_R(a)`). It's a legitimate ℝ-algebra automorphism, and its result is reported,
but the rigorous test of "genuinely different ℂ-linear representations" rests on the other three.

## C–F. Search space size and results

2072 test instances (259 seeds × 4 candidates × 2 sign conventions, minus `orientation_reversed`'s
undefined cases — defined only for balanced bipartitions, which never occur at odd `N` and only
sometimes at even `N`). **Order-zero: 100% pass. First-order: 0% pass. Zero exceptions.**

## G. The analytic theorem

**`THM-ASYM-BRIDGE-OBSTRUCTION-001`, proven, not observed:** for any pair of ℂ-linear representations
of the maximal abelian algebra `A_F=ℂ^N` (any bijective relabeling of the one-hot generators on each
side, independently), the first-order condition forces `D_F=0` — **regardless of whether `π_L=π_R`
or `π_L≠π_R`.** The proof (`reconstruction/ncg_first_order_proofs.json` has the full eight-step
derivation) shows the standard swap-conjugate `J_F` makes the first-order commutator decompose into
two *independent* blocks, one depending only on `π_L`, the other only on `π_R` — and each
independently requires the centralizer argument (the centralizer of the full diagonal algebra in
`M_N(ℂ)` is exactly the diagonal algebra itself) to force `D_F=0`. **The true cause is that `A_F` is
abelian — every irreducible representation is 1-dimensional — not that the two sectors match.** This
is a sharper, more general result than the previous run's, not a mere repetition of it.

## H–N. Direct answers

**H.** `D_F` cannot remain nonzero under this algebra class, proven in general. **I.** The bridge is
seed-sensitive at the level of the *objects* it constructs (`D_F`'s rank/spectrum,
`orientation_reversed`'s definedness) but seed-*insensitive* in the first-order pass/fail outcome
(uniform failure, for a reason independent of `R`'s specific topology). **J.** KO-dimension is
*not* uniquely selected by the seed — exactly two classes (0, 6 mod 8) are reachable, determined by
an external doubling-convention choice, unchanged from the previous run and unaffected by the
representation question. **K.** `D_F²=L` was tested directly and is **false** — checked exactly for
all 28 seeds at `N≤4`, zero matches, no shifted (`+cI`) relation either. **L, M.** Poincaré duality and
orientability are **deferred**, per this run's own stop condition (§32) — no closed finite triple
exists to test them against, and even the source NCG workbook's own intended target candidate leaves
both explicitly `OPEN`. **N.** No finite algebra is selected; the tested (abelian) class is proven
inadmissible in general, and a non-abelian candidate is the correctly-diagnosed but not-yet-built next
step.

## O. Reclassification of the previous (symmetric) bridge

`OPEN-024`'s "closed for symmetric representation" finding is **subsumed**, not superseded, by this
run's more general result: closed for *any* representation of an abelian algebra. Neither result shows
Track A cannot generate NCG in principle — both show a specific, minimal-assumption construction
cannot, for a precisely proven reason.

## P. Corrected MDCL fragment

```
R (Track A seed) -> bipartition, N_orient -> D_F, gamma_F [PROVEN, general, any seed]
                                            -> J_F (swap-conjugate) -> KO in {0,6} [PROVEN, seed-independent]
                                            -> pi(A_F=C^N), any faithful representation
                                            -> order-zero [PROVEN, always holds]
                                            -> first-order [PROVEN, NEVER holds for abelian A_F]
                                            -> STOP (per THM-ASYM-BRIDGE-OBSTRUCTION-001)

Poincare duality, orientability, finite algebra selection: DEFERRED, contingent on a non-abelian
algebra bridge not yet built.
```

## Q. Exactly one next unresolved upstream dependency

> **Build and test a bridge variant using a genuinely non-abelian candidate algebra** — one containing
> at least one multi-dimensional irreducible representation, derived from the seed's own structure
> (e.g. a coarser block structure over the bipartition rather than a per-vertex diagonal) rather than
> an externally-motivated choice like `ℍ` or `M₃(ℂ)`. This is the precise, minimal condition
> `THM-ASYM-BRIDGE-OBSTRUCTION-001`'s proof identifies as necessary for first-order to have any chance
> of closing with `D_F≠0` — not a guess, a direct consequence of the theorem. Not attempted this run,
> per the stop condition.

## Artifacts

`ncg_asymmetric_axioms.json`, `ncg_asymmetric_representations.json`, `ncg_first_order_proofs.json`,
`ncg_representation_equivalence.json`, `ncg_df_laplacian_relation.json`, `ncg_ko_dimension.json`,
`ncg_algebra_enumeration.json`, `ncg_poincare_duality.json`, `ncg_orientability.json`,
`ncg_asymmetric_bridge.json` (top-level summary + status registry), all in `reconstruction/`. Executable:
`reconstruction/toe_rebuild/compiler/ncg_asymmetric_bridge.py`,
`reconstruction/toe_rebuild/run_asymmetric_bridge.py`. 12/12 tests passing
(`reconstruction/toe_rebuild/tests/test_compiler.py`, ~33s).

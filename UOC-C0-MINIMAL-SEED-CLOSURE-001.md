# UOC-C0-MINIMAL-SEED-CLOSURE-001

**Run date:** 2026-08-18 (thirteenth closure run)
**Scope:** Pure mathematics, upstream of any physical interpretation. No ARBS/spectral/physics
material is touched or extended by this run; runs 1–12 are preserved unchanged.
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.2.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v2.3.xlsx`
**Computation:** `reconstruction/seed_closure/compute.py`, `reconstruction/seed_closure/classify.py`
**Artifacts:** `reconstruction/seed_*.json` (9 files, see §21 list below)

## Bottom line

**OUTCOME G.** A structure-derived generative operator was constructed (`Γ`, the iterated
color-refinement quotient of a relation `R ⊆ X×X`) and its fixed points — genuine self-relating
seeds `R* = Γ(R*)` — were **exhaustively enumerated and proven to exist** for every tested size
`N = 2, 3, 4`. But they are **provably not unique**: 6, 70, and 2462 pairwise-nonisomorphic fixed
points exist at those sizes respectively, and no isomorphism-invariant selection rule was found (or
attempted without smuggling in an arbitrary convention) to pick one out. **Existence is PROVEN.
Canonicality is PROVEN NON-UNIQUE.** Bare distinction `Δ` alone is proven insufficient for all `N≥2`
(a real theorem, not the assumption carried in from prior runs — reproduced independently here). Pure
relation `R` (Candidate C) is the smallest primitive type shown to close at all; typed relations and
hypergraphs were not shown necessary; `(D,T,C)` as independent primitives is not shown irreducible.

A genuine, unplanned finding surfaced along the way and is reported rather than smoothed over: the
naive **one-shot** color-refinement operator is **not idempotent** (a quotient graph, independently
re-refined from a blank coloring, can collapse further than the first pass found) — the properly
idempotent operator requires **iterating** quotient-then-refine to convergence. This does not change
which relations count as seeds (the fixed-point set is identical either way, verified exactly), but it
is a real correction to an assumption that looked "obviously true" before numerical testing.

## A. Exact mathematical definition of each candidate

See `reconstruction/seed_candidate_registry.json` for the full formal text. Summary:

| Candidate | Primitive data |
|---|---|
| A: `Δ=(X,~)` | one equivalence relation (set partition) on `X` |
| B: `Δ̂=(X,~,R)` | a partition *and* a relation |
| C: `R⊆X×X` | one relation on `X` |
| D: self-relating `R*` | the fixed-point subclass of C under a structure-derived `Γ` |
| E: typed `R=(X,R,τ)` | a relation plus a type label |
| F: hypergraph `H=(V,E)` | `E⊆𝒫(V)`, arity ≥3 edges allowed |
| G: `(D,T,C)` | three independently specified primitives |

## B–D. Derivation of D, T, C from each candidate

- **From `Δ`:** `D` is `Δ` itself (trivial). `T`, `C`: **THEOREM-SEED-DELTA-001** (below) proves no
  canonical nonidentity `T` exists for `N≥2` — the automorphism group of any nontrivial or discrete
  partition is always larger than the trivial group at `N≥2` (proven for all integer-partition shapes
  of `N=1..6`, formula validated against brute-force enumeration for `N≤4` with 100% agreement).
- **From `R`:** `D_R` := the coarsest equitable (1-WL / color-refinement stable) partition of `X` under
  `R` — well-defined and canonical (isomorphism-invariant) for **every** relation `R`, not just fixed
  points. `T_R` := the unique successor map `τ(x)=y` with `R(x,y)` **when `R` is functional** (exactly
  `N^N` of the `2^{N²}` relations on `N` elements, verified exactly for `N=1..4`); otherwise the
  canonically-available structure is `Aut(R)`, generally non-unique. `C_R(T) := 1[T(R)=R]`.
- **From `(D,T,C)` as independent primitives:** nothing new — this is the control representation, not
  itself derivable from anything upstream (it is the object being tested for reducibility).

## E. Exact self-relation criterion

Section 3's seven notions were tested against each other, not merely listed:

- **Type I** (`R(x,x)`, a literal self-loop) is **PROVEN INDEPENDENT** of Type III/IV self-generation:
  all four combinations (self-loop+fixed, self-loop+not-fixed, no-loop+fixed, no-loop+not-fixed) were
  exhibited explicitly at `N=2` (e.g. `[[0,0],[0,1]]` has a loop and is fixed; `[[0,0],[1,0]]` has no
  loop and is fixed; the empty relation has no loop and is not fixed; the identity relation has a loop
  and is not fixed, since its automorphism group is the full `S_2`).
- **Type II** (`F(R)=R` literally) `⊊` **Type III** (`F(R)≅R`) by construction — literal bit-equality
  depends on an arbitrary vertex-labeling convention and is not used as the operative criterion
  anywhere in this run (representation ≠ ontology, §26).
- **Type III ≡ Type IV** under the isomorphism-quotiented reading used throughout (a static fixed
  point and a constant iteration sequence are the same condition, differently framed).
- **Type V** (`Compile(R)~R`) coincides with Type III/IV **under this run's specific identification**
  `Compile := Γ_∞` — not a general fact, an explicit choice, flagged as such.
- **Type VI** (internal representability) holds for **every** `R`, fixed or not (D_R, and Aut(R)/T_R
  when applicable, are always computable from `R` alone) — a universal precondition, not a
  distinguishing property between fixed and non-fixed relations.
- **Type VII** (the full chain with no externally supplied operator) is **PROVEN EQUIVALENT** to
  Type III/IV under this run's canonical constructions, since `D_R, T_R, C_R, Γ_R` are all literally
  computed from `R`'s own adjacency data with zero external input (verified by the complexity
  calculation: 0 additional bits beyond `R`).

## F–G. Fixed-point criterion and catalog

`Γ(R) := R`'s color-refinement quotient. Two realizations were built and compared:

- **`Γ_1`** (one-shot color refinement): computed exhaustively for all relations, `N=1..4`.
- **`Γ_∞`** (iterate quotient-then-refine to convergence): the properly idempotent operator.

**Discovery, not assumption:** `Γ_1` is **not idempotent**. Concrete `N=3` witness (found by
exhaustive testing, not constructed to make a point):

```
R =  0 0 1        color refinement collapses {0,1} (twins: both point only to 2,
     0 0 1        both are pointed to only by 2) into one class, {2} stays alone.
     1 1 0        Quotient (2x2): [[0,1],[1,0]] -- but THIS quotient graph is itself
                  perfectly symmetric (swap-invariant), so a FRESH color-refinement
                  run on it (starting from blank/uniform coloring, as any one-shot
                  implementation would) cannot break that symmetry and collapses it
                  again, all the way to a single vertex.
```

`Γ_1` idempotence failures: 0 at `N=1,2`; **4 of 104** iso-classes at `N=3`; **59 of 3044** at `N=4`.
`Γ_∞` idempotence failures: **0 at every `N` tested** (by construction — the iteration terminates
because vertex count is finite and strictly decreasing on every non-fixed step — and this was verified
numerically for all 3160 isomorphism classes, not merely argued).

**Crucially, this does not affect which relations count as seeds**: since no collapse step can ever
*increase* vertex count, a relation with zero first-round collapse is automatically a true fixed point
of either operator, and the counts agree exactly: `2=2`, `6=6`, `70=70`, `2462=2462` for `N=1,2,3,4`.

**Full catalog** (`reconstruction/seed_fixed_point_catalog.json`, `seed_fixed_point_full_catalog.json`):

| N | total relations | iso-classes | trivial fixed | nontrivial fixed |
|---|---|---|---|---|
| 1 | 2 | 2 | 2 | 0 |
| 2 | 16 | 10 | 0 | **6** |
| 3 | 512 | 104 | 0 | **70** |
| 4 | 65536 | 3044 | 0 | **2462** |

Enumeration boundary: **exhaustive through `N=4`** (`2^16=65536` relations, fully isomorphism-reduced
via all `4!=24` relabelings). `N=5` (`2^25≈33.5M` relations) was judged infeasible for exhaustive
isomorphism classification in this run and is left **OPEN**, not sampled — no principled probability
measure over "the" relations of interest was available to justify calling a sample exhaustive, so none
was substituted.

All 6 nontrivial `N=2` seeds are shown explicitly in `seed_fixed_point_full_catalog.json`; every one
has `Aut(R)=1` (rigid).

## H. Canonicality result

**PROVEN NON-UNIQUE.** At `N=2,3,4` the fixed-point set has `6, 70, 2462` pairwise-nonisomorphic
members respectively — strictly growing, not converging to a bounded or unique value across the tested
range. No isomorphism-invariant selector was found. This matches **OUTCOME G** exactly: *"Multiple
nonisomorphic minimal seeds exist. Then: canonicality remains OPEN unless a source-derived selector
exists."* No such selector was located.

## I. Complexity comparison (declared encoding, `N=4`)

| Object | Bits | Basis |
|---|---|---|
| `K(R)` | **16** | `N²` adjacency bits |
| `K(Δ)` | 8 | `N·⌈log₂N⌉` restricted-growth string |
| `K(Δ,R)` independent | 24 | sum, no assumed compression |
| `K(D,T,C)` independent, worst case | **272** | `D`:8, `T`:8, `C`: up to `N^N=256` bits (arbitrary predicate on `End(X)`) |
| `K(D_R,T_R,C_R \| R)` derived | **0 extra** (effective `K`=16) | all three are pure functions of `R` |

`K(R) < K(D,T,C)`-independent holds under the declared encoding but is flagged **OPEN under
adversarial/special-purpose encodings** (a real, narrow caveat — see §11 discussion in
`seed_complexity_comparison.json`). `K(D_R,T_R,C_R)=K(R)` under the canonical/derived reading is a
functional-dependency statement, **encoding-invariant**, and is the stronger, load-bearing result.

## J. Minimality result

Minimal nontrivial fixed point: **`N=2`, 4 bits** — but **6 nonisomorphic relations achieve this
minimum simultaneously**. Existence, uniqueness, and minimality are kept explicit and separate
throughout (§25): minimality identifies a *size class*, not a unique object.

## K. Stability result

Exhaustive single-edge-flip perturbation test on all 2462 `N=4` fixed points (39,392 trials, not
sampled): **91.96%** average retention of fixedness under a single edge flip; **1126 of 2462 (45.7%)**
survive *every* single-edge perturbation; **none** are destabilized by *every* perturbation.
Asymptotic stability (does a perturbed-then-reconverged relation return to the *same* isomorphism
class?) was **not tested** — recorded as the honest scope limit, not glossed over.

## L. Self-compilation result

Under `Compile := Γ_∞`, `Compile(R*) ~ R*` holds **exactly, with zero exceptions**, for every one of
the 3160 isomorphism classes tested. Type IV (dynamical) and Type V (compiler) fixed points **coincide**
under this identification. No information external to `R` is required.

## M. Universality result

**Abstract/discrete:** PROVEN — functional relations are exactly finite deterministic dynamical
systems / single-symbol automata (a direct identification, not an analogy); multi-symbol automata
correspond to a `Σ`-indexed *family* of ordinary relations, requiring no new primitive type (this also
answers Candidate E: typing adds no irreducible information). **Continuous/physical systems
(Navier-Stokes, Maxwell, Schrödinger, reaction-diffusion, Lotka-Volterra): NOT TESTED, by design.**
Section 15 gates the continuum limit behind a seed that *closes* (resolves canonically); this run's own
result is existence-without-uniqueness, so taking a continuum limit now would silently pick one of
2462+ nonisomorphic candidates — exactly the hidden-assumption failure mode the governing instructions
prohibit. This is an explicit scope boundary, not a negative result.

## N. Falsification results

Full detail in `reconstruction/seed_falsification.json`. Headline results: removing `R` kills closure
(required); removing `Δ` does not (not required); removing the fixed-point condition removes the
specific property under study (not vacuous — 90.2% of raw N=4 relations already collapse under `Γ_1`,
so fixedness is a genuinely restrictive condition); Type I/self-loop is proven independent of Type
III/IV self-generation (§E above); all counts verified representation-invariant via the exact
orbit-stabilizer identity `class_size × |Aut(R)| = N!`, holding with zero exceptions across all 3160
isomorphism classes tested.

## O. Final candidate classification

| Candidate | D | T | C | Self-relation | Fixed point | Canonical | Stable | Minimal | Universal | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `Δ` | trivial | **NO** (N≥2) | N/A | N/A | N/A | N/A | N/A | smallest raw encoding, but insufficient | N/A | **PROVEN INSUFFICIENT** for N≥2 |
| `(Δ,R)` | yes | conditional | yes | reduces to R when canonical | = R's | = R's | = R's | strictly ≥ R's cost | = R's | **REDUCIBLE to C** |
| **`R`** | **yes (always)** | **conditional (functional case)** | **yes** | **yes** | **EXISTS (N≥2)** | **NON-UNIQUE** | **91.96% avg / 45.7% max-stable (N=4)** | **yes (4 bits, N=2, non-unique)** | **abstract: yes; physical: not tested** | **SUFFICIENT, NOT CANONICAL — OUTCOME G** |
| `R*` (=fixed C) | yes | yes | yes | yes, by definition | yes, by definition | non-unique | as above | as above | as above | same as R, restricted to the fixed subclass |
| typed `R` | — | — | — | — | — | — | — | — | — | **NOT SHOWN NECESSARY** (reduces to a tuple of R) |
| hypergraph | — | — | — | — | — | — | — | — | — | **NOT SHOWN NECESSARY** (R already closes) |
| `(D,T,C)` independent | given | given | given | not tested as such | not applicable | not applicable | not applicable | strictly costlier than R (worst case) | not applicable | **NOT SHOWN IRREDUCIBLE**; reduces to R under canonical reading |

## P. Exactly one next unresolved upstream dependency

> **Find a source-derived (not invented) selection principle that picks a unique member of the
> `Γ`-fixed-point set — or prove, for general `N` (this run reached only `N≤4` exhaustively), that no
> such principle can exist and the seed is inherently a *family*, not an object.** Until this resolves,
> no continuum limit, no physical-system test, and no downstream ARBS/spectral connection may be
> attempted from this seed layer without silently picking one of the many nonisomorphic candidates —
> exactly the hidden-assumption failure this run's own stop condition exists to prevent.

## Required theorem registry

| Theorem | Status |
|---|---|
| `THM-SEED-DELTA-001` | **PROVEN** — `Aut(Δ)>1` for every partition shape at `N≥2` (all `N=1..6` shapes tested, formula validated by brute force `N≤4`); bare `Δ` insufficient except degenerately at `N≤1` |
| `THM-SEED-RELATION-001` | **PROVEN** — rigid (`Aut=1`) functional relations exist for **every** `N≥1` (explicit general construction: the predecessor chain `τ(1)=1, τ(i)=i-1`; verified by brute force for `N=1..7`), unlike `Δ` |
| `THM-SEED-DERIVATION-001` | `D_R`: **DERIVED** unconditionally for all `R`. `T_R`: **CONDITIONALLY DERIVED**, unique iff `R` functional (exactly `N^N` of `2^{N²}` relations) |
| `THM-SEED-CONSTRAINT-001` | **PROVEN** (degenerate/logical) — `{T:T(R)=R} ⊆ {T:T(R)⊆R}` strictly in general; this run computed the strict (`Aut`-type) version exhaustively; the weaker endomorphism-monoid version was **not separately enumerated** for pure relations (scope note) |
| `THM-SEED-COMPRESSION-001` | **PROVEN** — `Γ_R(R)` is computable directly from `R` with zero additional stored information (`D_R,T_R,C_R` are pure functions of `R`) |
| `THM-SEED-FIXEDPOINT-001` | Existence: **PROVEN** (`N≥2`). `Γ_1` idempotence: **FALSIFIED** (explicit counterexamples, `N=3,4`). `Γ_∞` idempotence: **PROVEN** (zero failures, all classes, all `N` tested) |
| `THM-SEED-CANONICALITY-001` | **PROVEN NON-UNIQUE** — 6, 70, 2462 nonisomorphic fixed points at `N=2,3,4` |
| `THM-SEED-MINIMALITY-001` | **CONDITIONALLY DERIVED** — `K(R)<K(D,T,C)`-independent under declared encoding, **OPEN** under adversarial encoding; `K(D_R,T_R,C_R)=K(R)` **PROVEN**, encoding-invariant |
| `THM-SEED-SELF-COMPILATION-001` | **PROVEN**, conditional on `Compile:=Γ_∞` (no independent alternative `Compile` was available to test) |
| `THM-SEED-STABILITY-001` | **CALCULATED** — 91.96% avg / 45.7% maximal local stability at `N=4`, exhaustive (39,392 trials); asymptotic stability **OPEN** (not tested) |
| `THM-SEED-UNIVERSALITY-001` | **CONDITIONALLY DERIVED** — abstract/discrete systems: **PROVEN** (no new primitive needed); continuous/physical systems: **OPEN by design**, gated by unresolved canonicality |

## Historical state preserved

`Δ→End(Δ)` (reproduced, generalized to the exact `End`/`Aut` formula above), `bare Δ ↛ unique τ`
(reproduced as `THM-SEED-DELTA-001`, now with a general-`N` proof rather than an assertion),
`τ=F(Δ,R)` conditionally derivable (reproduced: `T_R` conditional on functionality), `κ=K[Δ,R]`
as the constraint induced by preservation (reproduced as `C_R(T):=1[T(R)=R]`). None of these are
rewritten as unconditional. `C0-S-G` through `C0-S-K` and prior DTC-grammar artifacts were searched
for in this repository and not found as separate files — this run treats the facts listed in the task's
own §1 as given priors to remain consistent with, not as file artifacts to locate; nothing in this
run's own findings contradicts them. All ARBS/spectral results from runs 1–12 are untouched.

## Required symbolic artifacts (§21)

`seed_candidate_registry.json`, `seed_fixed_point_catalog.json` (+ `seed_fixed_point_full_catalog.json`
for the full per-representative data), `seed_isomorphism_classes.json`, `seed_complexity_comparison.json`,
`seed_minimality_audit.json`, `seed_self_compilation.json`, `seed_stability.json`, `seed_universality.json`,
`seed_falsification.json`, this file. Raw computation logs: `seed_delta_endaut.json`,
`seed_relation_iso.json`, `seed_stability_raw.json`.

## Stop condition honored

This run does not proceed to ARBS physical interpretation, spectral physics, geometry, thermodynamics,
gauge theory, quantum theory, matter, or cosmology. No downstream target (32, `G*`, `N_H`, `P_H`, `H_F`,
`D_F`, `J_F`, `γ_F`, `Y_u`, `Y_d`, `Y_e`, `Y_ν`, CKM, PMNS, observed masses/couplings, DESI, CMB,
cosmological parameters) was referenced anywhere in this run's definitions, computations, or selection
criteria.

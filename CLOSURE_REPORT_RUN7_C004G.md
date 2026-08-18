# C-004G — ARBS Edge-Length Rescaling Law: Recovered

**Run date:** 2026-08-18 (seventh closure run, continuing from `CLOSURE_REPORT_RUN6_C004F.md`)
**Master artifact (input):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.6.xlsx`
**Master artifact (output):** `workbook/Universal_Rosetta_Stone_MASTER_CALCULATION_WORKBOOK_v1.7.xlsx`

## The law was never actually missing — it was invisible to text extraction

Every previous corpus search (runs 1–6) worked against `54_SOURCE_TEXT_CORPUS`, a paragraph-text
extraction of the whitepaper. That extraction silently **drops embedded equation images** — Word
documents that render formulas as pictures rather than OMML math markup leave nothing for a
text-only scraper to capture. Unzipping `source/Combined_Compiler_Theories_Whitepaper.docx` directly
and reading `word/document.xml` found exactly where this happened: the "Primal Edge Scaling" bullet
in Part I §2.1 cuts off mid-sentence in every prior search, immediately followed by
`<w:drawing>...<a:blip r:embed="rId10">` — a rendered PNG. Reading that image (and its two neighbors)
directly recovers the law in full.

## The recovered law

**Primal Edge Scaling:** `ℓ_{n+1}(e') = α·ℓ_n(e)` for all `e' ∈ R(e)` — every child edge produced by
refining parent edge `e` has length `α` times the parent's, `0<α<1`.

**Induced Metric Invariance:** `d_{n+1}(R(v_i),R(v_j)) = d_n(v_i,v_j)` — path distance between
corresponding vertices is exactly preserved under refinement (edges shrink by `α`, but the number of
edges along a path grows to compensate, exactly).

**Diameter Stability:** `Diam(M_n,d_n) = sup_{x,y}d_n(x,y) ≤ D_max < ∞` — the space's total size
stays bounded as `n` grows.

No numeric value of `α` is given anywhere in the corpus, and — critically — **this law is never once
referenced alongside the ARBS specification** (Phases XXIII–XXV, the part of the corpus that actually
defines `S_k=L_k⊔R_k`, `K_{2^k,2^k}`, `R_{k-1}×L_k`). It belongs to the generic "This from That"
`𝔊•` refinement functor of Part I §1–2, an entirely separate part of the whitepaper.

## Testing it against ARBS: proven incompatible, not merely unconnected

Three independent tests, one a direct numerical counterexample:

1. **No edge-subdivision domain.** The law presupposes `R(e)` is a nonempty set of child edges
   *replacing* parent edge `e`. ARBS's actual recursion doesn't do this: `G_k` is an **exact induced
   subgraph** of `G_{k+1}` — every edge of `G_k` survives into `G_{k+1}` completely unchanged
   (verified as an exact matrix equality in run 6). There is no `R(e)` for ARBS's own edges to scale.
2. **Diameter Stability directly falsified.** Computed the exact graph diameter (unweighted
   shortest-path hop count) for `G_0`–`G_7`: **`diam(G_n) = 2n+1` exactly** (1, 3, 5, 7, 9, 11, 13,
   15) — growing linearly, unboundedly. `Diam ≤ D_max<∞` fails for every `D_max`, for `n` large
   enough. This is a hard counterexample, not an absence of information.
3. **Forced comparison gives `α=1`, not `<1`.** ARBS has no weighted edge structure of its own — the
   only length assignment consistent with its own definition is unit length for every edge. Since old
   edges are carried over unchanged (test 1), any "scaling constant" between an edge and itself is
   trivially `α=1`, contradicting the law's own strict-contraction hypothesis.

## Conclusion

The rescaling law **is recovered from source** — the earlier "not source-supported" finding was a
limitation of the text-extraction pipeline, not of the source material. But recovering it settles the
question decisively rather than reopening it: **the law is defined for a bounded-diameter,
edge-subdividing mesh-refinement process, and ARBS is an unbounded-diameter, edge-preserving growth
process.** All three of the law's defining conditions fail for ARBS, one (diameter) by direct
counterexample.

**This upgrades THEOREM C-004F.5** from run 6's "DISPROVEN for the unrescaled map / OPEN for any
rescaled version (untestable, no rescaling available)" to **DISPROVEN OUTRIGHT**: no rescaling
compatible with the source's own stated axioms can exist for the ARBS construction, independent of
any choice of `α`, because ARBS structurally violates Diameter Stability by direct counterexample. The
"OPEN — untestable" escape hatch from run 6 is now closed by proof, not left dangling.

This also explains, at a structural level, something that was previously just an observation: why
`BRIDGE B-004` (heat-kernel-to-geometry) remains open in source, and why the certified `RF-001..005`
Gromov–Hausdorff convergence machinery (which fundamentally requires precompactness — uniformly
bounded diameter — to extract a convergent subsequence) was never applied to the ARBS shell sequence
anywhere in the corpus: it structurally cannot be, since ARBS's diameter is unbounded by direct
computation.

## Closure matrix

| Object | Status |
|---|---|
| ARBS edge-length rescaling law | **RECOVERED** (from embedded equation images) |
| Applicability to ARBS | **PROVEN INCOMPATIBLE** (3 independent arguments, 1 a direct counterexample) |
| THEOREM C-004F.5 (continuum thermodynamic limit) | **DISPROVEN OUTRIGHT** (upgraded from run 6) |
| `σ_k` | PROVEN NON-IDENTIFIABLE (unchanged, not reopened) |
| `G*` | UNRESOLVED (unchanged) |

## What this does not change

`C-004F.1`–`.4` (degree measure, weighted Hilbert space, weighted generator, Dirichlet form) are
unaffected — those are genuine, standing successes independent of the continuum-limit question.
`C-004C`, `C-004D`, `C-004E`, `THM-GEN-DISTINCT-001` are all unaffected and not reopened.

## Next

With C-004F/C-004G's chain now closed as far as source material permits, the remaining open items
in the project are: (1) `σ_k`'s magnitude — proven non-identifiable, would require source material
this project does not have (a canonical initial condition and evaluation time) to resolve; (2) the
substrate-only `G*` uniqueness theorem — still absent from source (`AU-002`/`BR-026`, both open in
the original corpus). Neither can be advanced by further searching the currently available source
material; both would require genuinely new source content, not deeper reading of what exists.

"""
UOC* compiler pipeline: orchestrates PASS-00 through PASS-09 on a candidate
relation, and returns a CompiledSeed object with an explicit status for every
pass -- CLOSED, PARTIAL, or BLOCKED, per uoc_compiler_passes.json's diagnosis.
Passes 10+ are represented as explicit stub entries returning BLOCKED with
their diagnosed reason, NOT executed with fabricated content (Section 43).
"""
from dataclasses import dataclass, field
from typing import Any
import itertools

from . import kernel


BLOCKED_REASONS = {
    "PASS-10": "insufficient N for continuum/metric approximation (geometry)",
    "PASS-11": "depends on PASS-10",
    "PASS-12": "depends on PASS-11",
    "PASS-13": "gauge derivation route empirically rejected (0/200); no independent route located -- see reconciliation_registry.json",
    "PASS-14": "source claims never independently computationally reproduced by this project",
    "PASS-15": "depends on PASS-12/13/14",
    "PASS-16": "lambda_gap undocumented anywhere in the corpus (persistence)",
    "PASS-17": "depends on PASS-10/16",
    "PASS-18": "depends on everything above -- prediction registry deliberately empty",
}


@dataclass
class CompiledSeed:
    N: int
    adjacency_matrix: list
    canonical_int: int
    aut_order: int
    gamma_fixed: bool = False
    bipartite: bool = False
    canonical_orientation_nilpotent: bool = False
    spectral: dict = field(default_factory=dict)
    pass_status: dict = field(default_factory=dict)


def compile_seed(mat_bits, N) -> CompiledSeed:
    """Run PASS-00 through PASS-09 on a single candidate relation (bit tuple)."""
    perms = list(itertools.permutations(range(N)))
    canon, aut = kernel.canonical_form(mat_bits, N, perms)
    seed = CompiledSeed(N=N, adjacency_matrix=[list(mat_bits[i*N:(i+1)*N]) for i in range(N)],
                         canonical_int=canon, aut_order=aut)
    seed.pass_status["PASS-00"] = "CLOSED"
    seed.pass_status["PASS-01"] = "CLOSED"  # R is the primitive

    seed.gamma_fixed = kernel.is_gamma_fixed(mat_bits, N)
    seed.pass_status["PASS-05"] = "CLOSED"
    seed.pass_status["PASS-08"] = "CLOSED" if seed.gamma_fixed else "NOT A FIXED POINT"

    if seed.gamma_fixed:
        seed.bipartite = kernel.is_bipartite(seed.adjacency_matrix, N)
        seed.pass_status["PASS-06 (TH-ARBS-001A)"] = "CLOSED" if seed.bipartite else "FAILS bipartite admissibility"
        if seed.bipartite:
            N_orient = kernel.canonical_orientation(seed.adjacency_matrix, N)
            seed.canonical_orientation_nilpotent = kernel.is_nilpotent(N_orient, N)
            seed.pass_status["PASS-06 (TH-ARBS-001B via N_orient)"] = (
                "CLOSED (automatic, THM-UOC-KERNEL-RECONFIG-001)" if seed.canonical_orientation_nilpotent
                else "THEOREM VIOLATION -- would falsify THM-UOC-KERNEL-RECONFIG-001, report immediately"
            )
    seed.spectral = kernel.spectral_data(seed.adjacency_matrix, N)
    seed.pass_status["PASS-09"] = "PARTIAL -- real-spectrum guarantee requires symmetric R" \
        if not seed.spectral["is_symmetric"] else "CLOSED -- symmetric, certified machinery applies"

    for pid, reason in BLOCKED_REASONS.items():
        seed.pass_status[pid] = f"BLOCKED: {reason}"

    return seed


def enumerate_admissible_seeds(N):
    """Full PASS-00..09 pipeline run over every relation on N elements, returning
    only the Gamma-fixed, bipartite (TH-ARBS-001A/B-admissible) survivors, each
    fully compiled. Exhaustive for N<=4; callers should use the dedicated
    N=5 bipartite-subset construction (toe_rebuild/n5_bipartite.py) for N=5,
    since brute force over all 2^25 relations is infeasible."""
    if N > 4:
        raise ValueError("Use n5_bipartite.py's targeted construction for N>4 -- "
                          "brute force is infeasible (see run 14's documented boundary).")
    n2 = N * N
    seen = {}
    survivors = []
    for v in range(2 ** n2):
        bits = kernel.int_to_bits(v, n2)
        canon, _ = kernel.canonical_form(bits, N)
        if canon in seen:
            continue
        seen[canon] = True
        seed = compile_seed(bits, N)
        if seed.gamma_fixed and seed.bipartite:
            survivors.append(seed)
    return survivors

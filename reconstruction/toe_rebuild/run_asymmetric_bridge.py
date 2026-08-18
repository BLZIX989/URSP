"""
Full exhaustive sweep of the asymmetric representation search space
(compiler/ncg_asymmetric_bridge.py) over all 259 seeds in F_N^derived_v2,
N=2,3,4,5.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compiler import kernel, enumerate_admissible_seeds
from compiler import ncg_asymmetric_bridge as ab
from run_bridge import get_n5_candidates

all_results = {}
for N in [2, 3, 4, 5]:
    print(f"=== N={N} ===")
    if N <= 4:
        seeds = enumerate_admissible_seeds(N)
        mats = [s.adjacency_matrix for s in seeds]
    else:
        mats = get_n5_candidates()
    print(f"  {len(mats)} candidates")

    agg = {c: {"tested": 0, "undefined": 0, "order_zero_pass": 0, "first_order_pass": 0}
           for c in ab.REPRESENTATION_CANDIDATES}

    for mat in mats:
        res = ab.full_asymmetric_sweep(mat, N)
        for candidate in ab.REPRESENTATION_CANDIDATES:
            for same_sign in [True, False]:
                key = f"{candidate}__same_sign={same_sign}"
                r = res[key]
                bucket = agg[candidate]
                if r["status"] == "UNDEFINED_FOR_THIS_SEED":
                    bucket["undefined"] += 1
                else:
                    bucket["tested"] += 1
                    if r["order_zero_holds"]:
                        bucket["order_zero_pass"] += 1
                    if r["first_order_holds"]:
                        bucket["first_order_pass"] += 1

    all_results[N] = {"n_candidates": len(mats), "by_representation": agg}
    print(json.dumps(all_results[N], indent=2))

with open("/home/user/URSP/reconstruction/uoc_asymmetric_bridge_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("\nsaved uoc_asymmetric_bridge_results.json")

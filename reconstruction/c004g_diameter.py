"""
Computes the exact graph diameter (unweighted hop-count shortest path) of
G0..G7 to directly test the source's own 'Diameter Stability' axiom
(Diam(M_n,d_n) <= D_max < infinity) against the ARBS shell construction.
"""
import numpy as np
import json
from scipy.sparse.csgraph import shortest_path
from scipy.sparse import csr_matrix
from arbs_light import analyze_light

results = {}
for n in range(8):
    r = analyze_light(n)
    A = csr_matrix(r["A"])
    D = shortest_path(A, method="D", unweighted=True, directed=False)
    diam = int(D.max())
    results[f"G{n}"] = {"N": r["N"], "diameter_hops": diam, "predicted_2n+1": 2 * n + 1,
                         "matches_prediction": diam == 2 * n + 1}
    print(f"G{n}: N={r['N']} diameter={diam} predicted(2n+1)={2*n+1} match={diam==2*n+1}")

with open("/home/user/URSP/reconstruction/c004g_diameter.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved c004g_diameter.json")

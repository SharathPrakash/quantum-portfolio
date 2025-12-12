import cirq
import numpy as np
from collections import Counter

q =cirq.LineQubit(0)
sim=cirq.Simulator()

angles=[0,np.pi/6,np.pi/4,np.pi/2,np.pi]

for angle in angles:
    circuit = cirq.Circuit(
        cirq.ry(angle)(q),
        cirq.measure(q,key='m')
    )

    result = sim.run(circuit,repetitions=1000)
    counts=Counter(result.measurements['m'][:,0])
    p1=counts.get(1,0)/1000
    print(f"Ry({angle:.2f}) -> P(1) ~ {p1:.3f}")

import cirq
import numpy as np
from collections import Counter

q = cirq.LineQubit(0)
sim = cirq.Simulator()

circuit = cirq.Circuit(
    cirq.H(q),
    cirq.rz(np.pi/2)(q),
    cirq.measure(q, key='m')
)

print(circuit)
result = sim.run(circuit, repetitions=1000)
print(result.histogram(key='m'))

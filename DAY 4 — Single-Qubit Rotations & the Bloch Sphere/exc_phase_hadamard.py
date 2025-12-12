import cirq
import numpy as np

q = cirq.LineQubit(0)
sim = cirq.Simulator()

circuit = cirq.Circuit(
    cirq.H(q),
    cirq.rz(np.pi)(q),
    cirq.H(q),
    cirq.measure(q, key='m')
)

print(circuit)
print(sim.run(circuit, repetitions=1000).histogram(key='m'))

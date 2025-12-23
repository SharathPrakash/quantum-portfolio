import cirq
import numpy as np
from collections import Counter

# Two qubits
q0, q1 = cirq.LineQubit.range(2)

circuit = cirq.Circuit()

# 1️⃣ Initialize superposition
circuit.append([cirq.H(q0), cirq.H(q1)])

# ---- ORACLE ----
# Mark |11> by phase flip
circuit.append(cirq.CZ(q0, q1))

# ---- DIFFUSION OPERATOR ----
circuit.append([cirq.H(q0), cirq.H(q1)])
circuit.append([cirq.X(q0), cirq.X(q1)])
circuit.append(cirq.CZ(q0, q1))
circuit.append([cirq.X(q0), cirq.X(q1)])
circuit.append([cirq.H(q0), cirq.H(q1)])

# 2️⃣ Measure
circuit.append(cirq.measure(q0, q1, key='result'))

print("Mini Grover Circuit:")
print(circuit)

# Simulate
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1000)

counts = Counter(tuple(r) for r in result.measurements['result'])
print("\nMeasurement counts:")
for state, count in sorted(counts.items()):
    print(f"{state}: {count}")

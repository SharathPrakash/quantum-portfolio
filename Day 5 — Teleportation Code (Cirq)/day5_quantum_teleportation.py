import cirq
import numpy as np

# Qubits
q0, q1, q2 = cirq.LineQubit.range(3)

circuit = cirq.Circuit()

# 1️⃣ Prepare arbitrary state on q0 (state to teleport)
theta = np.pi / 3
circuit.append(cirq.ry(theta)(q0))

# 2️⃣ Create Bell pair between q1 and q2
circuit.append(cirq.H(q1))
circuit.append(cirq.CNOT(q1, q2))

# 3️⃣ Bell measurement on q0 and q1
circuit.append(cirq.CNOT(q0, q1))
circuit.append(cirq.H(q0))

# 4️⃣ Measure q0 and q1
circuit.append(cirq.measure(q0, key='m0'))
circuit.append(cirq.measure(q1, key='m1'))

# 5️⃣ Conditional corrections on q2 (Bob)
circuit.append(cirq.X(q2).with_classical_controls('m1'))
circuit.append(cirq.Z(q2).with_classical_controls('m0'))

print("Quantum Teleportation Circuit:")
print(circuit)

# Simulate
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1000)

print("\nMeasurement results:")
print(result)

import cirq
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create 2 qubits
q0, q1 = cirq.LineQubit.range(2)

# Step 2: Build the Bell State circuit
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key="m")
)

print("\nCircuit:")
print(circuit)

# Step 3: Run the circuit locally
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=200)
counts = result.histogram(key="m")

print("\nMeasurement counts:")
print(counts)

# Step 4: Plot histogram
plt.bar(counts.keys(), counts.values())
plt.xlabel("State")
plt.ylabel("Count")
plt.title("Bell State Measurement Histogram")
plt.savefig("bell_histogram.png")

print("\nSaved output to bell_histogram.png")


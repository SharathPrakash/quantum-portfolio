import cirq

q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key="m")
)

print("Circuit:\n", circuit)
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=20)
print("Results:", result)


import cirq

#create 1 qubit
q=cirq.LineQubit(0)

#Create a circuit
circuit=cirq.Circuit()

#Apply Superposition using Hadamard gate
circuit.append(cirq.H(q))

#Measure the qubit
circuit.append(cirq.measure(q, key='result'))

#Print the circuit
print("Circuit:")
print(circuit)

#Simulate the circuit
simulator=cirq.Simulator()
result=simulator.run(circuit, repetitions=10)
#Print the results
print("\nMeasurement Results:")
print(result)
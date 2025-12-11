# day3_exercises.py
# Day 3 exercises: measurement, probabilities, and entanglement behaviour
# Requires: cirq, numpy
import cirq
import numpy as np
from collections import Counter

def run_sim(circuit, repetitions=100):
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=repetitions)
    return result

# -----------------------
# Exercise 1: Measure a superposition (H then measure) 100 times
# -----------------------
def exercise_1(repetitions=100):
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.H(q),
        cirq.measure(q, key='m')
    )
    print("Exercise 1 circuit:\n", circuit)
    res = run_sim(circuit, repetitions=repetitions)
    counts = Counter(tuple(r) for r in zip(*[res.measurements['m'][:,0]]))
    # convert counts to friendly form
    formatted = {str(k[0]): v for k, v in counts.items()}
    print(f"Repetitions: {repetitions}, counts:", formatted)
    print("Expected: roughly 50/50 for '0' and '1' when using H.\n")

# -----------------------
# Exercise 2: Bias the qubit (rotation around Y) and measure 1000 times
# -----------------------
def exercise_2(angle=0.5, repetitions=1000):
    # angle in radians for RY
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.ry(angle)(q),   # rotate around Y by `angle` radians
        cirq.measure(q, key='m')
    )
    print("Exercise 2 circuit:\n", circuit)
    res = run_sim(circuit, repetitions=repetitions)
    counts = Counter(res.measurements['m'][:,0])
    p1 = counts.get(1, 0) / repetitions
    p0 = counts.get(0, 0) / repetitions
    print(f"Angle (rad): {angle:.4f}")
    print(f"Counts (0,1): ({counts.get(0,0)}, {counts.get(1,0)})")
    print(f"Estimated probabilities -> P(0)={p0:.4f}, P(1)={p1:.4f}")
    # Theoretical probabilities from state: |psi> = cos(theta/2)|0> + sin(theta/2)|1>
    # For ry(angle) the mapping: theta = angle (Cirq's ry uses the standard).
    theo_p1 = np.sin(angle/2)**2
    theo_p0 = np.cos(angle/2)**2
    print(f"Theoretical approx -> P(0)={theo_p0:.4f}, P(1)={theo_p1:.4f}\n")

# -----------------------
# Exercise 3: Measure BEFORE applying a gate vs H then measure
# -----------------------
def exercise_3(repetitions=200):
    q = cirq.LineQubit(0)

    # Circuit A: H -> measure
    circ_a = cirq.Circuit(cirq.H(q), cirq.measure(q, key='m'))

    # Circuit B: measure -> H
    # Note: measuring an initial |0> collapses to |0>, then H acts on that definite state
    circ_b = cirq.Circuit(cirq.measure(q, key='m'), cirq.H(q), cirq.measure(q, key='m2'))

    print("Exercise 3 - Circuit A (H -> measure):\n", circ_a)
    res_a = run_sim(circ_a, repetitions=repetitions)
    counts_a = Counter(res_a.measurements['m'][:,0])
    print(f"Circuit A counts (0,1): ({counts_a.get(0,0)}, {counts_a.get(1,0)})")

    print("\nExercise 3 - Circuit B (measure -> H -> measure):\n", circ_b)
    res_b = run_sim(circ_b, repetitions=repetitions)
    # res_b has two measurement keys; the first 'm' is the initial measure, the second 'm2' is after H
    pre_counts = Counter(res_b.measurements['m'][:,0])
    post_counts = Counter(res_b.measurements['m2'][:,0])
    print(f"Circuit B initial measurement counts (m): ({pre_counts.get(0,0)}, {pre_counts.get(1,0)})")
    print(f"Circuit B after-H measurement counts (m2): ({post_counts.get(0,0)}, {post_counts.get(1,0)})")
    print("\nExplanation: Measuring first collapses to a definite 0 (since the qubit starts at |0>),\nso the subsequent H acts on a definite state and you'll see deterministic/expected results.\n")

# -----------------------
# Exercise 4: Create Bell state, measure both qubits
# -----------------------
def exercise_4(repetitions=300):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, key='m0'),
        cirq.measure(q1, key='m1')
    )
    print("Exercise 4 circuit:\n", circuit)
    res = run_sim(circuit, repetitions=repetitions)
    # Build tuple counts (m0,m1)
    pairs = [tuple(row) for row in np.hstack((res.measurements['m0'], res.measurements['m1']))]
    counts = Counter(pairs)
    print("Counts for (q0, q1):")
    for pair, cnt in sorted(counts.items()):
        print(f"{pair}: {cnt}")
    print("Expected: mostly (0,0) and (1,1) with roughly equal frequency (Bell state).\n")

# -----------------------
# Exercise 5: Measure only q0 in Bell state, then apply H to q1 and measure q1
# (mid-circuit measurement)
# -----------------------
def exercise_5(repetitions=500):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, key='m0'),  # measure q0 (collapses the pair)
        # q1 is now in a definite state depending on m0; apply H to q1 and measure
        cirq.H(q1),
        cirq.measure(q1, key='m1')
    )
    print("Exercise 5 circuit (measure q0 mid-circuit, then H on q1, then measure q1):\n", circuit)
    res = run_sim(circuit, repetitions=repetitions)
    # analyze joint outcomes of m0 then m1
    pairs = list(zip(res.measurements['m0'][:,0], res.measurements['m1'][:,0]))
    counts = Counter(pairs)
    print("Counts (m0, m1):")
    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")
    print("\nInterpretation:")
    print("- Measuring q0 collapses the Bell pair into either |00> or |11>.\n"
          "- If collapsed to |00>, q1 = |0>. H on q1 makes it (|0>+|1>)/√2 → measure ~50/50.\n"
          "- If collapsed to |11>, q1 = |1>. H on q1 makes it (|0>-|1>)/√2 → measure ~50/50 too.\n"
          "So you expect roughly 4 equally likely (m0,m1) combos if you look across many runs\n"
          "but m0 will be 0 or 1 about half the time and m1 will be roughly 50/50 conditioned on either.\n")

# -----------------------
# Exercise 6: Probability estimation convergence
# -----------------------
def exercise_6():
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q, key='m'))
    print("Exercise 6 circuit:\n", circuit)
    for reps in [10, 100, 1000, 10000]:
        res = run_sim(circuit, repetitions=reps)
        counts = Counter(res.measurements['m'][:,0])
        p1 = counts.get(1, 0) / reps
        p0 = counts.get(0, 0) / reps
        print(f"Repetitions: {reps:5d} -> P(0)={p0:.4f}, P(1)={p1:.4f}")
    print("\nYou should see the estimated probabilities approach 0.5 as repetitions increase.\n")

# -----------------------
# Bonus: Reconstruct distribution analytically and verify
# -----------------------
def bonus_reconstruct():
    # Example: after H on |0> -> state is (|0> + |1>)/sqrt(2)
    # Probabilities are |amplitude|^2 => both 0.5
    print("Bonus analytic check:")
    alpha = 1/np.sqrt(2)
    beta = 1/np.sqrt(2)
    print(f"Amplitude alpha={alpha:.4f}, beta={beta:.4f}")
    print(f"P(0) = |alpha|^2 = {abs(alpha)**2:.4f}, P(1) = |beta|^2 = {abs(beta)**2:.4f}\n")
    # Verify by simulation quickly
    exercise_1(repetitions=1000)

# -----------------------
# Main: run all exercises (or call specific ones)
# -----------------------
if __name__ == "__main__":
    print("Running Day 3 exercises. You can call individual functions instead if you prefer.\n")
    exercise_1(100)
    exercise_2(angle=0.5, repetitions=1000)
    exercise_3(200)
    exercise_4(300)
    exercise_5(500)
    exercise_6()
    bonus_reconstruct()

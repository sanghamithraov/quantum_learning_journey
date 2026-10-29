import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# ============================================================
# WEEKS 9-10: QUANTUM PARALLELISM & CORE ALGORITHMS
# Deutsch's Algorithm and Grover's Search
# ============================================================


def show_state(title, circuit):
    """Display the statevector after a circuit operation."""
    state = Statevector.from_instruction(circuit)

    print(f"\n{title}")
    for i, amplitude in enumerate(state.data):
        if abs(amplitude) > 1e-8:
            print(f"|{i:03b}> : {amplitude.real:+.4f}"
                  f" {amplitude.imag:+.4f}j")

    return state


# ============================================================
# 1. DEUTSCH'S ALGORITHM
# ============================================================

def deutsch_algorithm(constant_function=True):
    qc = QuantumCircuit(2)

    # Prepare input qubit |0> and ancilla |1>
    qc.x(1)
    qc.h(0)
    qc.h(1)

    # Oracle:
    # Constant function: do nothing
    # Balanced function: apply CNOT
    if not constant_function:
        qc.cx(0, 1)

    # Interference step
    qc.h(0)

    # Inspect the final state
    state = Statevector.from_instruction(qc)

    # Measurement probabilities for input qubit q0
    probabilities = state.probabilities([0])

    result = int(np.argmax(probabilities))

    return qc, result


print("=" * 60)
print("1. DEUTSCH'S ALGORITHM")
print("=" * 60)

for is_constant in [True, False]:
    circuit, result = deutsch_algorithm(is_constant)

    function_type = "CONSTANT" if is_constant else "BALANCED"

    print(f"\nOracle type: {function_type}")
    print(circuit)
    print("Input qubit measurement:", result)

    if is_constant and result == 0:
        print("Correctly identified a constant function.")
    elif not is_constant and result == 1:
        print("Correctly identified a balanced function.")
    else:
        print("Unexpected result: check the circuit.")


# ============================================================
# 2. GROVER'S SEARCH — THREE QUBITS
# ============================================================

def make_oracle(marked_state):
    """
    Create an oracle that flips the phase of one marked state.
    marked_state is a 3-bit string, e.g. '101'.
    """

    if len(marked_state) != 3 or any(b not in "01"
                                      for b in marked_state):
        raise ValueError("marked_state must be a 3-bit string.")

    qc = QuantumCircuit(3)

    # Convert zero-controls into one-controls.
    for qubit, bit in enumerate(reversed(marked_state)):
        if bit == "0":
            qc.x(qubit)

    # Phase flip of |111>
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)

    # Restore zero-controls.
    for qubit, bit in enumerate(reversed(marked_state)):
        if bit == "0":
            qc.x(qubit)

    return qc


def make_diffusion():
    """Build Grover's diffusion operator for three qubits."""

    qc = QuantumCircuit(3)

    qc.h([0, 1, 2])
    qc.x([0, 1, 2])

    # Phase flip of |111> in the transformed basis
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)

    qc.x([0, 1, 2])
    qc.h([0, 1, 2])

    return qc


def grover_search(marked_state="101"):
    qc = QuantumCircuit(3)

    # Create an equal superposition of all 8 states.
    qc.h([0, 1, 2])

    show_state("Initial equal superposition", qc)

    # Oracle phase inversion.
    oracle = make_oracle(marked_state)
    qc.compose(oracle, inplace=True)

    show_state("After oracle phase flip", qc)

    # Diffusion / amplitude amplification.
    diffusion = make_diffusion()
    qc.compose(diffusion, inplace=True)

    final_state = show_state("After diffusion operator", qc)

    probabilities = final_state.probabilities()

    print("\nFinal probabilities:")
    for i, probability in enumerate(probabilities):
        print(f"|{i:03b}> : {probability:.4f}")

    # Qiskit statevector index uses qubit 0 as the least
    # significant bit, so reverse the displayed bit string.
    marked_index = int(marked_state, 2)
    marked_probability = probabilities[marked_index]

    print("\nMarked state:", marked_state)
    print("Probability of marked state:",
          round(marked_probability, 4))

    if marked_probability > 0.75:
        print("SUCCESS: Grover amplification found the marked state.")
    else:
        print("DEBUG: Check the oracle and diffusion operations.")
    return qc


print("\n" + "=" * 60)
print("2. GROVER'S SEARCH — THREE QUBITS")
print("=" * 60)

grover_circuit = grover_search("101")

print("\nComplete Grover circuit:")
print(grover_circuit)


# ============================================================
# 3. DEBUGGING CHECKLIST
# ============================================================

print("\n" + "=" * 60)
print("3. DEBUGGING SUMMARY")
print("=" * 60)

print("Oracle: flips the phase of the marked state.")
print("Diffusion: amplifies the marked state's amplitude.")
print("Check the statevector before and after each operation.")
print("The marked state's probability should increase.")
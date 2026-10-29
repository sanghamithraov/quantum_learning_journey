import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def make_oracle(marked_state="101"):
    """Flip the phase of the marked state."""
    qc = QuantumCircuit(3)

    for q, bit in enumerate(reversed(marked_state)):
        if bit == "0":
            qc.x(q)

    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)

    for q, bit in enumerate(reversed(marked_state)):
        if bit == "0":
            qc.x(q)

    return qc


def make_diffusion():
    """Correct Grover diffusion operator."""
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    qc.x([0, 1, 2])
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)
    qc.x([0, 1, 2])
    qc.h([0, 1, 2])
    return qc


def run_grover(introduce_error=False):
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])

    qc.compose(make_oracle("101"), inplace=True)

    diffusion = make_diffusion()

    if introduce_error:
        # INTENTIONAL ERROR:
        # Remove the final Hadamard on qubit 0.
        diffusion.data.pop()

    qc.compose(diffusion, inplace=True)

    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities()
    marked_index = int("101", 2)

    print("\nMode:", "FAULTY" if introduce_error else "CORRECT")
    print("Marked state: 101")
    print("Marked-state probability:",
          round(probabilities[marked_index], 4))
    print("All probabilities:",
          np.round(probabilities, 4))

    return probabilities[marked_index]


print("=" * 50)
print("GROVER'S ALGORITHM: DEBUGGING COMPARISON")
print("=" * 50)

correct_probability = run_grover(introduce_error=False)
faulty_probability = run_grover(introduce_error=True)

print("\nDEBUGGING SUMMARY")
print("Correct probability:", round(correct_probability, 4))
print("Faulty probability:", round(faulty_probability, 4))
print("Difference:",
      round(abs(correct_probability - faulty_probability), 4))
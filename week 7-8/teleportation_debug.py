import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.quantum_info import partial_trace, state_fidelity


# ============================================================
# QUANTUM TELEPORTATION — DEBUGGING
# Compare a correct circuit with a circuit containing
# an intentional gate error.
# ============================================================


# The state we want to teleport: |+>
original_state = Statevector([
    1 / np.sqrt(2),
    1 / np.sqrt(2)
])


# ============================================================
# CORRECT TELEPORTATION
# ============================================================

correct = QuantumCircuit(3)

# Prepare Alice's state |+>
correct.h(0)

# Create entanglement between Alice and Bob
correct.h(1)
correct.cx(1, 2)

# Bell-state operations
correct.cx(0, 1)
correct.h(0)

# Correct state-transfer operations
correct.cx(1, 2)
correct.cz(0, 2)


# Get final state
correct_state = Statevector.from_instruction(correct)

# Extract Bob's qubit
bob_correct = partial_trace(
    DensityMatrix(correct_state),
    [0, 1]
)

# Compare Bob's state with the original state
correct_fidelity = state_fidelity(
    bob_correct,
    DensityMatrix(original_state)
)


print("=" * 60)
print("CORRECT QUANTUM TELEPORTATION")
print("=" * 60)

print(correct)

print("\nFidelity:", round(correct_fidelity, 6))

if correct_fidelity > 0.99:
    print("SUCCESS: Bob reconstructed the original state.")


# ============================================================
# INTENTIONAL GATE ERROR
# ============================================================

faulty = QuantumCircuit(3)

# Prepare Alice's state |+>
faulty.h(0)

# Create entanglement
faulty.h(1)
faulty.cx(1, 2)

# Bell-state operations
faulty.cx(0, 1)
faulty.h(0)

# Correct operation
faulty.cx(1, 2)

# ------------------------------------------------------------
# INTENTIONAL ERROR:
# The correct circuit uses CZ here.
# We deliberately use CX instead.
# ------------------------------------------------------------

faulty.cx(0, 2)


# Get faulty final state
faulty_state = Statevector.from_instruction(faulty)

# Extract Bob's qubit
bob_faulty = partial_trace(
    DensityMatrix(faulty_state),
    [0, 1]
)

# Compare faulty result with original state
faulty_fidelity = state_fidelity(
    bob_faulty,
    DensityMatrix(original_state)
)


print("\n" + "=" * 60)
print("TELEPORTATION WITH INTENTIONAL GATE ERROR")
print("=" * 60)

print(faulty)

print("\nFidelity:", round(faulty_fidelity, 6))

if faulty_fidelity < 0.99:
    print("FAILURE: State reconstruction failed.")
    print("The intentional gate error changed Bob's reconstructed state.")


# ============================================================
# DEBUGGING SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DEBUGGING SUMMARY")
print("=" * 60)

print("Correct fidelity :", round(correct_fidelity, 6))
print("Faulty fidelity  :", round(faulty_fidelity, 6))

print("\nIntentional error:")
print("CZ gate was replaced with CX.")

if faulty_fidelity < correct_fidelity:
    print("Result: The gate error reduced the fidelity.")
    print("Therefore, the original state was not correctly reconstructed.")
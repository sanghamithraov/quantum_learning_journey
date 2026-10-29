import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# ============================================================
# WEEK 5–6: MULTI-QUBIT SYSTEMS, TENSOR PRODUCTS & ENTANGLEMENT
# ============================================================


# ------------------------------------------------------------
# 1. TENSOR PRODUCTS
# ------------------------------------------------------------

print("=" * 60)
print("1. TENSOR PRODUCTS")
print("=" * 60)

zero = np.array([1, 0], dtype=complex)
one = np.array([0, 1], dtype=complex)

states = {
    "|00>": np.kron(zero, zero),
    "|01>": np.kron(zero, one),
    "|10>": np.kron(one, zero),
    "|11>": np.kron(one, one)
}

for name, state in states.items():
    print(f"{name} = {state}")

print()


# ------------------------------------------------------------
# 2. CNOT GATE
# ------------------------------------------------------------

print("=" * 60)
print("2. CNOT GATE")
print("=" * 60)

qc = QuantumCircuit(2)

qc.x(0)
qc.cx(0, 1)

print(qc)

state = Statevector.from_instruction(qc)

print("Statevector:")
print(state)

print()


# ------------------------------------------------------------
# 3. SWAP GATE
# ------------------------------------------------------------

print("=" * 60)
print("3. SWAP GATE")
print("=" * 60)

qc_swap = QuantumCircuit(2)

qc_swap.x(0)
qc_swap.swap(0, 1)

print(qc_swap)

state_swap = Statevector.from_instruction(qc_swap)

print("Statevector:")
print(state_swap)

print()


# ------------------------------------------------------------
# 4. CONTROLLED-U GATE
# ------------------------------------------------------------

print("=" * 60)
print("4. CONTROLLED-U GATE")
print("=" * 60)

qc_controlled = QuantumCircuit(2)

qc_controlled.h(0)
qc_controlled.cp(np.pi / 2, 0, 1)

print(qc_controlled)

state_controlled = Statevector.from_instruction(qc_controlled)

print("Statevector:")
print(state_controlled)

print()


# ------------------------------------------------------------
# 5. CONSTRUCTIVE / DESTRUCTIVE INTERFERENCE
# ------------------------------------------------------------

print("=" * 60)
print("5. QUANTUM INTERFERENCE")
print("=" * 60)

# H followed by H returns the qubit to |0>
qc_interference = QuantumCircuit(1)

qc_interference.h(0)
qc_interference.h(0)

print(qc_interference)

state_interference = Statevector.from_instruction(qc_interference)

print("Statevector after H-H:")
print(state_interference)

print("This demonstrates interference: the |1> amplitudes cancel.")


print()


# ------------------------------------------------------------
# 6. PARTIAL MEASUREMENT
# ------------------------------------------------------------

print("=" * 60)
print("6. PARTIAL MEASUREMENT")
print("=" * 60)

qc_partial = QuantumCircuit(2)

qc_partial.h(0)
qc_partial.cx(0, 1)

print(qc_partial)

state_partial = Statevector.from_instruction(qc_partial)

print("Entangled state before measurement:")
print(state_partial)

# Measurement of only qubit 0
# Conceptually, measuring one qubit of the Bell state
# collapses the other qubit to the corresponding state.

print("If qubit 0 is measured:")
print("  Result 0 -> qubit 1 collapses to |0>")
print("  Result 1 -> qubit 1 collapses to |1>")

print()


# ------------------------------------------------------------
# 7. BELL STATE |PHI+>
# ------------------------------------------------------------

print("=" * 60)
print("7. BELL STATE |PHI+>")
print("=" * 60)

phi_plus = QuantumCircuit(2)

phi_plus.h(0)
phi_plus.cx(0, 1)

print(phi_plus)

phi_plus_state = Statevector.from_instruction(phi_plus)

print("Statevector:")
print(phi_plus_state)

print("Expected:")
print("|PHI+> = (|00> + |11>) / sqrt(2)")

print()


# ------------------------------------------------------------
# 8. BELL STATE |PHI->
# ------------------------------------------------------------

print("=" * 60)
print("8. BELL STATE |PHI->")
print("=" * 60)

phi_minus = QuantumCircuit(2)

phi_minus.h(0)
phi_minus.z(0)
phi_minus.cx(0, 1)

print(phi_minus)

phi_minus_state = Statevector.from_instruction(phi_minus)

print("Statevector:")
print(phi_minus_state)

print("Expected:")
print("|PHI-> = (|00> - |11>) / sqrt(2)")

print()


# ------------------------------------------------------------
# 9. BELL STATE |PSI+>
# ------------------------------------------------------------

print("=" * 60)
print("9. BELL STATE |PSI+>")
print("=" * 60)

psi_plus = QuantumCircuit(2)

psi_plus.x(1)
psi_plus.h(0)
psi_plus.cx(0, 1)

print(psi_plus)

psi_plus_state = Statevector.from_instruction(psi_plus)

print("Statevector:")
print(psi_plus_state)

print("Expected:")
print("|PSI+> = (|01> + |10>) / sqrt(2)")

print()


# ------------------------------------------------------------
# 10. BELL STATE |PSI->
# ------------------------------------------------------------

print("=" * 60)
print("10. BELL STATE |PSI->")
print("=" * 60)

psi_minus = QuantumCircuit(2)

psi_minus.x(1)
psi_minus.h(0)
psi_minus.cx(0, 1)
psi_minus.z(0)

print(psi_minus)

psi_minus_state = Statevector.from_instruction(psi_minus)

print("Statevector:")
print(psi_minus_state)

print("Expected:")
print("|PSI-> = (|01> - |10>) / sqrt(2)")

print()


# ------------------------------------------------------------
# 11. ENTANGLEMENT: MATRIX REPRESENTATION
# ------------------------------------------------------------

print("=" * 60)
print("11. MATHEMATICAL PROOF OF ENTANGLEMENT")
print("=" * 60)

# Matrix representation of Phi+
phi_plus_matrix = np.array([
    [1 / np.sqrt(2), 0],
    [0, 1 / np.sqrt(2)]
])

print("|PHI+> coefficient matrix:")
print(phi_plus_matrix)

determinant = np.linalg.det(phi_plus_matrix)

print("\nDeterminant:")
print(determinant)

if not np.isclose(determinant, 0):
    print(
        "\nThe determinant is non-zero."
        "\nTherefore the matrix has rank 2."
        "\nIt cannot be written as an outer product of two"
        "\nindependent single-qubit states."
        "\nTherefore |PHI+> is an entangled state."
    )

print()


# ------------------------------------------------------------
# 12. CHECK ALL FOUR BELL STATES
# ------------------------------------------------------------

print("=" * 60)
print("12. BELL STATE SUMMARY")
print("=" * 60)

bell_states = {
    "Phi+": phi_plus_state,
    "Phi-": phi_minus_state,
    "Psi+": psi_plus_state,
    "Psi-": psi_minus_state
}

for name, state in bell_states.items():
    print(f"{name}: {state}")

print()


# ------------------------------------------------------------
# 13. NO-CLONING THEOREM
# ------------------------------------------------------------

print("=" * 60)
print("13. NO-CLONING THEOREM")
print("=" * 60)

print("""
The No-Cloning Theorem states that an arbitrary unknown
quantum state cannot be perfectly copied.

For an unknown state |psi>, a universal cloning operation
would require:

U(|psi>|0>) = |psi>|psi>

However, quantum mechanics does not allow such a universal
operation for arbitrary unknown states.

Therefore, an unknown quantum state cannot be perfectly cloned.
""")

print("=" * 60)
print("WEEK 5–6 TASK COMPLETED")
print("=" * 60)
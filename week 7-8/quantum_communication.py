import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
from qiskit.quantum_info import state_fidelity


# ============================================================
# WEEK 7–8: QUANTUM COMMUNICATION PROTOCOLS
# Superdense Coding | Quantum Teleportation | BB84 QKD
# ============================================================


# ============================================================
# 1. SUPERDENSE CODING
# ============================================================

def superdense_coding(message):
    """
    Encode two classical bits into one qubit using
    superdense coding.

    message: "00", "01", "10", or "11"
    """

    qc = QuantumCircuit(2)

    # Create Bell pair
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes her two classical bits
    if message == "01":
        qc.x(0)

    elif message == "10":
        qc.z(0)

    elif message == "11":
        qc.z(0)
        qc.x(0)

    # Bob decodes
    qc.cx(0, 1)
    qc.h(0)

    # Get final state
    state = Statevector.from_instruction(qc)

    probabilities = state.probabilities_dict()

    decoded = max(probabilities, key=probabilities.get)

    return decoded, qc


print("\n" + "=" * 60)
print("1. SUPERDENSE CODING")
print("=" * 60)

message = "11"

decoded_message, superdense_circuit = superdense_coding(message)

print("Original message :", message)
print("Decoded message  :", decoded_message)

print("\nCircuit:")
print(superdense_circuit)


# ============================================================
# 2. QUANTUM TELEPORTATION
# ============================================================

def quantum_teleportation():
    """
    Teleport the state |+> from Alice's qubit to Bob's qubit.
    """

    qc = QuantumCircuit(3)

    # --------------------------------------------------------
    # Prepare Alice's unknown state |+>
    # --------------------------------------------------------

    qc.h(0)

    # --------------------------------------------------------
    # Create entanglement between Alice's entanglement qubit
    # and Bob's qubit
    # --------------------------------------------------------

    qc.h(1)
    qc.cx(1, 2)

    # --------------------------------------------------------
    # Bell measurement between Alice's state and her
    # entangled qubit
    # --------------------------------------------------------

    qc.cx(0, 1)
    qc.h(0)

    # --------------------------------------------------------
    # Classical corrections
    #
    # In a real teleportation protocol these depend on
    # Alice's measurement results.
    #
    # Here we use the coherent equivalent so that we can
    # demonstrate the state transformation with Statevector.
    # --------------------------------------------------------

    qc.cx(1, 2)
    qc.cz(0, 2)

    return qc


print("\n" + "=" * 60)
print("2. QUANTUM TELEPORTATION")
print("=" * 60)

teleportation_circuit = quantum_teleportation()

print("Teleportation circuit:")
print(teleportation_circuit)

final_state = Statevector.from_instruction(teleportation_circuit)

# Trace out Alice's two qubits.
# Qubit 2 is Bob's qubit.
bob_state = partial_trace(
    DensityMatrix(final_state),
    [0, 1]
)

# Original |+> state
original_state = Statevector([1 / np.sqrt(2), 1 / np.sqrt(2)])

fidelity = state_fidelity(
    bob_state,
    DensityMatrix(original_state)
)

print("\nOriginal state: |+>")
print("Bob's reconstructed state:")
print(bob_state)

print("\nFidelity:", round(fidelity, 6))

if fidelity > 0.99:
    print("SUCCESS: State reconstructed correctly.")
else:
    print("FAILURE: State reconstruction is incorrect.")


# ============================================================
# 3. BB84 QUANTUM KEY DISTRIBUTION
# ============================================================

def prepare_qubit(bit, basis):
    """
    Prepare one BB84 qubit.

    basis = 0 -> computational/Z basis
    basis = 1 -> Hadamard/X basis
    """

    qc = QuantumCircuit(1)

    # Prepare |1> if bit = 1
    if bit == 1:
        qc.x(0)

    # Prepare diagonal basis if basis = 1
    if basis == 1:
        qc.h(0)

    return qc


def measure_qubit(qc, basis):
    """
    Measure a qubit in the requested basis.

    Returns 0 or 1.
    """

    circuit = qc.copy()

    # Rotate X basis back to Z basis
    if basis == 1:
        circuit.h(0)

    state = Statevector.from_instruction(circuit)

    probabilities = state.probabilities()

    return np.random.choice(
        [0, 1],
        p=probabilities
    )


def bb84_protocol(num_bits=20, eavesdrop=False):
    """
    Simulate the BB84 protocol.

    If eavesdrop=True, Eve intercepts each qubit using
    a randomly chosen basis.
    """

    alice_bits = np.random.randint(0, 2, num_bits)

    alice_bases = np.random.randint(0, 2, num_bits)

    bob_bases = np.random.randint(0, 2, num_bits)

    bob_results = []

    for i in range(num_bits):

        # Alice prepares the qubit
        qubit = prepare_qubit(
            alice_bits[i],
            alice_bases[i]
        )

        # ----------------------------------------------------
        # Eve intercepts the qubit
        # ----------------------------------------------------

        if eavesdrop:

            eve_basis = np.random.randint(0, 2)

            # Eve measures
            eve_result = measure_qubit(
                qubit,
                eve_basis
            )

            # Eve prepares a new qubit based on her result
            qubit = prepare_qubit(
                eve_result,
                eve_basis
            )

        # Bob measures
        bob_result = measure_qubit(
            qubit,
            bob_bases[i]
        )

        bob_results.append(bob_result)

    # --------------------------------------------------------
    # Alice and Bob keep only positions where their bases
    # are the same.
    # --------------------------------------------------------

    sifted_alice = []
    sifted_bob = []

    for i in range(num_bits):

        if alice_bases[i] == bob_bases[i]:

            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_results[i])

    # Calculate QBER
    if len(sifted_alice) == 0:
        qber = 0
    else:
        errors = sum(
            a != b
            for a, b in zip(sifted_alice, sifted_bob)
        )

        qber = errors / len(sifted_alice)

    return (
        alice_bits,
        alice_bases,
        bob_bases,
        sifted_alice,
        sifted_bob,
        qber
    )


# ============================================================
# BB84 WITHOUT EAVESDROPPING
# ============================================================

print("\n" + "=" * 60)
print("3. BB84 QUANTUM KEY DISTRIBUTION")
print("=" * 60)

(
    alice_bits,
    alice_bases,
    bob_bases,
    alice_key,
    bob_key,
    qber_without_eve
) = bb84_protocol(
    num_bits=100,
    eavesdrop=False
)

print("\nWithout Eve")
print("Alice's sifted key :", alice_key)
print("Bob's sifted key   :", bob_key)
print("QBER               :", round(qber_without_eve, 4))


# ============================================================
# BB84 WITH EAVESDROPPING
# ============================================================

(
    alice_bits,
    alice_bases,
    bob_bases,
    alice_key_eve,
    bob_key_eve,
    qber_with_eve
) = bb84_protocol(
    num_bits=100,
    eavesdrop=True
)

print("\nWith Eve")
print("Alice's sifted key :", alice_key_eve)
print("Bob's sifted key   :", bob_key_eve)
print("QBER               :", round(qber_with_eve, 4))

print("\n" + "=" * 60)
print("BB84 RESULT")
print("=" * 60)

print(
    "QBER without Eve :",
    round(qber_without_eve, 4)
)

print(
    "QBER with Eve    :",
    round(qber_with_eve, 4)
)

if qber_with_eve > qber_without_eve:
    print("\nEavesdropping detected!")
    print("The QBER increased because Eve disturbed the quantum states.")
else:
    print("\nRun again — randomness may have produced a similar QBER.")
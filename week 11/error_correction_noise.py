from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error, depolarizing_error
from qiskit import ClassicalRegister

# --------------------------------------------------
# 1. THREE-BIT BIT-FLIP ERROR CORRECTION
# --------------------------------------------------

def bit_flip_code():

    syndrome = ClassicalRegister(2, "syndrome")
    output = ClassicalRegister(3, "output")

    qreg = QuantumRegister(5, "q")
    qc = QuantumCircuit(qreg, syndrome, output)

    # Prepare logical state |1>
    qc.x(0)

    # Encode using three qubits
    qc.cx(0, 1)
    qc.cx(0, 2)

    # Intentionally introduce a bit-flip error
    qc.x(1)

    # Syndrome extraction
    qc.cx(0, 3)
    qc.cx(1, 3)

    qc.cx(1, 4)
    qc.cx(2, 4)

    qc.measure(3, syndrome[0])
    qc.measure(4, syndrome[1])

    # Correct according to syndrome
    with qc.if_test((syndrome, 1)):
        qc.x(0)

    with qc.if_test((syndrome, 3)):
        qc.x(1)

    with qc.if_test((syndrome, 2)):
        qc.x(2)

    # Measure corrected data qubits
    qc.measure(0, output[0])
    qc.measure(1, output[1])
    qc.measure(2, output[2])

    return qc


# --------------------------------------------------
# 2. THREE-BIT PHASE-FLIP ERROR CORRECTION
# --------------------------------------------------

def phase_flip_code():

    syndrome = ClassicalRegister(2, "syndrome")
    output = ClassicalRegister(3, "output")

    qreg = QuantumRegister(5, "q")
    qc = QuantumCircuit(qreg, syndrome, output)
    # Prepare logical state |1>
    qc.x(0)

    # Encode the logical state
    qc.cx(0, 1)
    qc.cx(0, 2)

    # Convert to phase-flip code basis
    for q in range(3):
        qc.h(q)

    # Introduce a phase-flip error
    qc.z(1)

    # Convert phase error into bit-flip error
    for q in range(3):
        qc.h(q)

    # Syndrome extraction
    qc.cx(0, 3)
    qc.cx(1, 3)

    qc.cx(1, 4)
    qc.cx(2, 4)

    qc.measure(3, syndrome[0])
    qc.measure(4, syndrome[1])

    # Correct the identified error
    with qc.if_test((syndrome, 1)):
        qc.x(0)

    with qc.if_test((syndrome, 3)):
        qc.x(1)

    with qc.if_test((syndrome, 2)):
        qc.x(2)

    # Return to phase-flip code basis
    for q in range(3):
        qc.h(q)

    # Measure the corrected state
    qc.measure(0, output[0])
    qc.measure(1, output[1])
    qc.measure(2, output[2])

    return qc


# --------------------------------------------------
# 3. SIMULATE ENVIRONMENTAL QUANTUM NOISE
# --------------------------------------------------

def noise_simulation():

    noise_model = NoiseModel()

    # Bit-flip channel: 10% probability of X error
    bit_error = pauli_error([
        ("X", 0.10),
        ("I", 0.90)
    ])

    # Depolarizing channel
    depolarizing = depolarizing_error(0.05, 1)

    noise_model.add_all_qubit_quantum_error(
        bit_error, ["id"]
    )

    noise_model.add_all_qubit_quantum_error(
        depolarizing, ["h"]
    )

    simulator = AerSimulator(noise_model=noise_model)

    qc = QuantumCircuit(1, 1)

    qc.h(0)

    # Repeated identity operations experience noise
    for _ in range(10):
        qc.id(0)

    qc.measure(0, 0)

    compiled = transpile(qc, simulator)

    result = simulator.run(
        compiled, shots=1024
    ).result()

    counts = result.get_counts()

    return counts


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    simulator = AerSimulator()

    print("=" * 55)
    print("QUANTUM ERROR CORRECTION AND NOISE SIMULATION")
    print("=" * 55)

    # Bit-flip demonstration
    print("\n1. THREE-BIT BIT-FLIP CODE")

    bit_circuit = bit_flip_code()
    compiled = transpile(bit_circuit, simulator)

    result = simulator.run(
        compiled, shots=1024
    ).result()

    print("Measurement results:")
    print(result.get_counts())

    # Phase-flip demonstration
    print("\n2. THREE-BIT PHASE-FLIP CODE")

    phase_circuit = phase_flip_code()
    compiled = transpile(phase_circuit, simulator)

    result = simulator.run(
        compiled, shots=1024
    ).result()

    print("Measurement results:")
    print(result.get_counts())

    # Noise demonstration
    print("\n3. ENVIRONMENTAL NOISE SIMULATION")

    noise_results = noise_simulation()

    print("Measurement results:")
    print(noise_results)

    print("\nSimulation completed!")
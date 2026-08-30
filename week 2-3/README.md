 # Week 2–3: Linear Algebra & Single-Qubit State Mechanics

## Objective

This work focuses on the mathematical foundations of single-qubit quantum mechanics and the implementation of basic quantum gate operations using raw matrix operations.

## Quantum Gates Implemented

The following single-qubit gates were represented as matrices:

- Pauli-X
- Pauli-Y
- Pauli-Z
- Hadamard (H)
- Phase (S)
- T

## Matrix Operations

The simulator applies a gate matrix to a qubit state vector using matrix multiplication:

Gate Matrix × State Vector → New State Vector

No quantum computing frameworks such as Qiskit were used.

## Measurement Simulation

The simulator calculates measurement probabilities from the amplitudes of the qubit state.

For a state:

|ψ⟩ = α|0⟩ + β|1⟩

the probabilities are:

P(0) = |α|²
P(1) = |β|²

The simulator then performs a measurement and collapses the state to either |0⟩ or |1⟩ according to these probabilities.

## Testing and Debugging

The implementation was tested by comparing the Python matrix operations with expected single-qubit gate results.

The Hadamard gate applied to |0⟩ produces an equal superposition:

H|0⟩ = 1/√2(|0⟩ + |1⟩)

The corresponding measurement probabilities are approximately:

P(0) = 0.5
P(1) = 0.5

The simulator successfully produced a measurement result and collapsed the state accordingly.

## Technologies

- Python
- NumPy

No quantum computing frameworks were used.
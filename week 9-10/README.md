Weeks 9–10: Quantum Parallelism & Core Algorithms

Objective

Study quantum parallelism, oracle functions, phase inversion, Deutsch's algorithm, and Grover's search algorithm.

Implementations

- Deutsch's algorithm
- Grover's search for three qubits
- Oracle construction and phase inversion
- Diffusion operator and amplitude amplification

Debugging

Compared the correct Grover implementation with a faulty implementation.

- Correct marked-state probability: 0.7812
- Faulty marked-state probability: 0.25
- Difference: 0.5312

The faulty circuit produced a different probability distribution, demonstrating how an implementation error can affect amplitude amplification.

Tools

- Python
- Qiskit (if used in the implementation)

Files

- "quantum_algorithms.py"
- "grover_debug.py"
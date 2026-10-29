import numpy as np

# -----------------------------
# Single-qubit gate matrices
# -----------------------------

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Y = np.array([
    [0, -1j],
    [1j, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([
    [1, 1],
    [1, -1]
], dtype=complex)

S = np.array([
    [1, 0],
    [0, 1j]
], dtype=complex)

T = np.array([
    [1, 0],
    [0, np.exp(1j * np.pi / 4)]
], dtype=complex)


# -----------------------------
# Basic qubit states
# -----------------------------

ket0 = np.array([
    [1],
    [0]
], dtype=complex)

ket1 = np.array([
    [0],
    [1]
], dtype=complex)


# -----------------------------
# Apply a quantum gate
# -----------------------------

def apply_gate(gate, state):
    return np.dot(gate, state)


# -----------------------------
# Display a state vector
# -----------------------------

def display_state(state):
    print(np.round(state, 4))


# -----------------------------
# Measurement probabilities
# -----------------------------

def measurement_probabilities(state):
    p0 = abs(state[0, 0]) ** 2
    p1 = abs(state[1, 0]) ** 2

    return p0, p1


# -----------------------------
# Simulate measurement collapse
# -----------------------------

def measure(state):
    p0, p1 = measurement_probabilities(state)

    result = np.random.choice(
        [0, 1],
        p=[p0, p1]
    )

    if result == 0:
        collapsed_state = ket0
    else:
        collapsed_state = ket1

    return result, collapsed_state


# -----------------------------
# Main demonstration
# -----------------------------

print("=== Single Qubit Gate Simulation ===")

print("\nInitial state |0>:")
display_state(ket0)

print("\nPauli-X applied to |0>:")
x_state = apply_gate(X, ket0)
display_state(x_state)

print("\nPauli-Y applied to |0>:")
y_state = apply_gate(Y, ket0)
display_state(y_state)

print("\nPauli-Z applied to |0>:")
z_state = apply_gate(Z, ket0)
display_state(z_state)

print("\nHadamard applied to |0>:")
h_state = apply_gate(H, ket0)
display_state(h_state)

print("\nPhase S applied to |0>:")
s_state = apply_gate(S, ket0)
display_state(s_state)

print("\nPhase T applied to |0>:")
t_state = apply_gate(T, ket0)
display_state(t_state)


# -----------------------------
# Measurement demonstration
# -----------------------------

print("\n=== Measurement of H|0> ===")

p0, p1 = measurement_probabilities(h_state)

print("Probability of measuring |0>:", round(p0, 4))
print("Probability of measuring |1>:", round(p1, 4))

result, collapsed_state = measure(h_state)

print("\nMeasurement result:", result)

print("Collapsed state:")
display_state(collapsed_state)
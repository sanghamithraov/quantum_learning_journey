Quantum Learning Journey

My technical learning journey during my 3-month internship at Usizo Solutions, focusing on quantum computing concepts, reversible logic, and practical implementation from first principles.

About This Repository

This repository documents my learning process throughout the internship.

The goal is not only to write working code, but to understand the underlying logic, implement concepts from scratch, test them, identify mistakes, and document what I learn.

Current Focus

- Classical logic and Boolean operations
- Reversible computation
- Reversible logic gates
- Truth-table simulation
- Debugging reversible mappings
- Python implementations without external quantum-computing libraries

---

From Classical to Reversible Computing

Classical logic gates such as AND and OR can be irreversible because the original inputs cannot always be uniquely determined from the output.

For example, an AND gate produces:

A| B| A AND B
0| 0| 0
0| 1| 0
1| 0| 0
1| 1| 1

If the output is "0", we cannot determine whether the original input was "00", "01", or "10".

Reversible computing takes a different approach. A reversible operation has a unique output for every input, allowing the original input state to be recovered.

This makes reversible logic an important foundation for understanding quantum computing, where quantum operations must be reversible.

---

Toffoli Gate

The Toffoli gate, also called the controlled-controlled-NOT (CCNOT) gate, operates on three bits:

- "A" — first control bit
- "B" — second control bit
- "C" — target bit

The target bit "C" is flipped only when both control bits are "1".

The mapping can be written as:

(A, B, C) → (A, B, C XOR (A AND B))

Truth Table

A| B| C| Output
0| 0| 0| 000
0| 0| 1| 001
0| 1| 0| 010
0| 1| 1| 011
1| 0| 0| 100
1| 0| 1| 101
1| 1| 0| 111
1| 1| 1| 110

Only the last two cases change because only those inputs have "A = 1" and "B = 1".

---

Implementation

The Toffoli gate was implemented in Python without using an external quantum-computing library.

def toffoli(a, b, c):
    if a == 1 and b == 1:
        c = 1 - c

    return a, b, c

The expression:

c = 1 - c

flips a binary bit:

0 → 1
1 → 0

The control bits remain unchanged.

---

Debugging: My First Logic Error

The first version of the simulator contained a logic error.

I initially used:

if a == 1 or b == 1:

This was incorrect because the Toffoli gate requires both control bits to be "1".

Using "or" would flip the target whenever either control was "1".

For example:

A = 1
B = 0
C = 0

The incorrect condition would flip "C", producing:

100 → 101

But a Toffoli gate should leave this input unchanged because "B = 0".

Correction

The condition was changed to:

if a == 1 and b == 1:

Now the target changes only when both controls are active.

This debugging process helped me understand that implementing a reversible gate is not just about writing the syntax correctly — the input-output mapping itself must be preserved exactly.

---

Files

[""toffoli_sim_v1.py""]

Initial implementation containing the control-condition logic error.

"["toffoli_sim_v2.py""]

Corrected implementation using the proper Toffoli condition.

---

Learning Progress

This repository will be updated as I progress through the internship.

Future work will include:

- More reversible gates
- Automated truth-table verification
- Reversible mapping experiments
- Additional debugging exercises
- Deeper exploration of the relationship between reversible logic and quantum computing

---

Internship

Organization: Usizo Solutions Pvt. Ltd.
Internship Duration: 3 months
Focus: Quantum Sensing / Quantum Computing Learning

This repository serves as a public record of my technical learning, experiments, implementations, and debugging process throughout the internship.

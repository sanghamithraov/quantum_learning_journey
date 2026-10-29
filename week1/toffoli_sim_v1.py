 # Toffoli Gate Simulator

# Toffoli gate
# A and B are control bits
# C is the target bit

def toffoli(a, b, c):

    # Flip C when the control condition is satisfied
    if a == 1 or b == 1:
        c = 1 - c

    return a, b, c


# All possible 3-bit inputs

inputs = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1)
]


# Expected Toffoli truth table
# We prepared this from the Toffoli rule.

expected_outputs = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 1),
    (1, 1, 0)
]


# Generate truth table

print("TOFFOLI TRUTH TABLE")
print("-------------------")

outputs = []

for i in range(len(inputs)):

    input_bits = inputs[i]

    output = toffoli(
        input_bits[0],
        input_bits[1],
        input_bits[2]
    )

    outputs.append(output)

    print(input_bits, "->", output)


# Check reversibility

print("\nREVERSIBILITY CHECK")
print("-------------------")

if len(outputs) == len(set(outputs)):
    print("Mapping is reversible.")
else:
    print("Mapping is NOT reversible.")


# Compare our output with the expected truth table

print("\nTRUTH TABLE CHECK")
print("-----------------")

mismatches = []

for i in range(len(inputs)):

    if outputs[i] != expected_outputs[i]:

        mismatches.append(
            (inputs[i], expected_outputs[i], outputs[i])
        )


if len(mismatches) == 0:

    print("All truth table values are correct.")

else:

    print("Mismatches found:")
    print()

    for mismatch in mismatches:

        print(
            "Input:", mismatch[0],
            "| Expected:", mismatch[1],
            "| Got:", mismatch[2]
        )


# Test applying the gate twice

print("\nDOUBLE APPLICATION TEST")
print("-----------------------")

test_input = (1, 1, 0)

first_output = toffoli(
    test_input[0],
    test_input[1],
    test_input[2]
)

second_output = toffoli(
    first_output[0],
    first_output[1],
    first_output[2]
)

print("Original input :", test_input)
print("After 1st gate :", first_output)
print("After 2nd gate :", second_output)

if second_output == test_input:
    print("PASS: Original input was restored.")
else:
    print("FAIL: Original input was not restored.")
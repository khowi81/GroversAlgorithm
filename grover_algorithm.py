# this is a project that demonstrates Grover's Algorithm in quantum computing 
# GA helps search an unsorted database for a specific item with quadratic speedup
# Code by Kasema Howard for use with IBM Qiskit simulator. 

from qiskit import Aer, QuantumCircuit, execute
from qiskit.visualization import plot_histogram
import numpy as np

# defining the database, which is colors mapped to binary
database = {
    "red": "000",
    "blue": "001",
    "yellow": "010",
    "green": "011",
    "purple": "100",
}

# set the target item in the database
target_color = "blue"
target_binary = database[target_color]

# Initialize the Quantum Circuit
n_qubits = len(target_binary) # how many qubits needed
qc = QuantumCircuit(n_qubits)

# Apply Hadamard Gates to initialize superposition
qc.h(range(n_qubits))

# Using Oracle, which flips the amplitude of the target state (to make it stand out more)
def oracle(circuit, target_state):
    for idx, bit in enumerate(target_state):
        if bit == "0":
            circuit.x(idx) # This applies an X-gate for |0> states
    circuit.h(n_qubits -1)
    circuit.mcx(list(range(n_qubits -1)), n_qubits -1) #this is a multi controlled Z
    circuit.h(n_qubits -1)
    for idx, bit in enumerate(target_state):
        if bit == "0":
            circuit.x(idx) # this reverts the X-gates

oracle(qc, target_binary)

# Using the Diffusion operator, which is a reflection about the average amplitude
def diffusion_operator(circuit, n_qubits):
    circuit.h(range(n_qubits))
    circuit.x(range(n_qubits))
    circuit.h(n_qubits -1)
    circuit.mcx(list(range(n_qubits -1)), n_qubits -1)
    circuit.h(n_qubits -1)
    circuit.x(range(n_qubits))
    circuit.h(range(n_qubits))

diffusion_operator(qc, n_qubits)

# Measurement
qc.measure_all()

# The fun part, run the circuit
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=1024).result()
counts = result.get_counts()

# Show your work and plot the results
print("Database: {database}")
print(f"Target: {target_color} ({target_binary})")
plot_histogram(counts)

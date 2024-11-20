import random
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler # Import Sampler for execution
from qiskit_aer import Aer # Import Aer from qiskit_aer


# Configuración
num_qubits = 10  # Número de qubits en el protocolo

# Paso 1: Alice prepara los qubits
alice_states = [random.choice(['0', '1']) for _ in range(num_qubits)]  # Estados de Alice
alice_bases = [random.choice(['X', 'Z']) for _ in range(num_qubits)]  # Bases de Alice

# Crear circuito cuántico
qc = QuantumCircuit(num_qubits, num_qubits)

# Preparar qubits
for i in range(num_qubits):
    if alice_states[i] == '1':
        qc.x(i)  # Estado |1>
    if alice_bases[i] == 'X':
        qc.h(i)  # Base Hadamard (X)

# Medición de Bob en bases aleatorias
bob_bases = [random.choice(['X', 'Z']) for _ in range(num_qubits)]
for i in range(num_qubits):
    if bob_bases[i] == 'X':
        qc.h(i)  # Base Hadamard para medir en X
qc.measure(range(num_qubits), range(num_qubits))

# Simular el circuito usando Aer and Sampler
simulator = Aer.get_backend('qasm_simulator')
sampler = Sampler() # Create a Sampler instance
job = sampler.run(qc, backend=simulator, shots=1) # Execute using Sampler
result = job.result() 
# Extract counts from the result 
# (get_counts is no longer directly available on result object)
counts = result.quasi_dists[0].binary_probabilities()
bob_results = list(counts.keys())[0]

# Paso 2: Comparar bases
shared_key = []
for i in range(num_qubits):
    if alice_bases[i] == bob_bases[i]:  # Bases coinciden
        shared_key.append(alice_states[i])

print("Estados de Alice:", alice_states)
print("Bases de Alice:", alice_bases)
print("Bases de Bob:", bob_bases)
print("Resultados de Bob:", bob_results)
print("Clave compartida:", shared_key)
# quantum_executor.py

from qiskit import QuantumCircuit, execute, Aer

def run_quantum_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1024)
    result = job.result()
    return result.get_counts(qc)
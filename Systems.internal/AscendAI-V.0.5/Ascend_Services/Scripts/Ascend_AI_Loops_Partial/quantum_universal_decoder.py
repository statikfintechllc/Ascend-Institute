import logging
from qiskit import QuantumCircuit, Aer, execute


class QuantumUniversalDecoder:
    def decode(self, quantum_data):
        qc = QuantumCircuit(len(quantum_data))
        for i, qubit in enumerate(quantum_data):
            if qubit:
                qc.x(i)
        qc.measure_all()
        result = execute(qc, Aer.get_backend("qasm_simulator")).result()
        counts = result.get_counts()
        decoded_result = max(counts, key=counts.get)
        return decoded_result

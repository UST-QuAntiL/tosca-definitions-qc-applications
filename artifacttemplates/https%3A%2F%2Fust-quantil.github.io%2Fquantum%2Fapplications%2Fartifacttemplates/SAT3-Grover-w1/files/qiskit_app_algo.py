from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.utils import QuantumInstance
from qiskit import BasicAer, execute
import math
import operator
from typing import List
from ast import literal_eval


######### Function signature & filename must not be changed #########
def run_algo(quantum_instance, args):
    print("run_algo grover wit args %s" % args)
    # args["clauses"] should be in the format [[-1, -1, -1], [1, -1, 1], [1, 1, -1], [1, -1, -1], [-1, 1, 1]]

    clauses_str = args["clauses"]
    clauses = literal_eval(clauses_str)
    print("find SAT solution for following clauses: %s" % clauses)

    N = len(clauses[0])
    oracle_circuit = oracle(clauses)
    grover_circuit = grover(N, oracle_circuit)
    counts = run(grover_circuit, quantum_instance)
    print("Execution results (counts): %s" % counts)
    max_found = max(counts.items(), key=operator.itemgetter(1))[0]
    print("Found solution: %s. Should be one of [000, 101, 110]" % max_found)

    return {'counts': counts, 'max': max_found}


def run(circ, quantum_instance):
    result = quantum_instance.execute(circ)
    return result.get_counts(circ)


def ccz(circ: QuantumCircuit, c1: int, c2: int, target: int, ancilla: int):
    circ.ccx(c1, c2, ancilla)
    circ.cz(ancilla, target)
    circ.ccx(c1, c2, ancilla)


def mcx(circuit: QuantumCircuit, controls: List[int], ancillas: List[int], target: int):
    num_ancillas = len(controls)-2
    if len(ancillas) < num_ancillas:
        print("Error: Too few ancilla bits for mcx")
    else:
        circuit.ccx(controls[0], ancillas[0], target)
        for i in range(1, len(controls)-2):
            circuit.ccx(controls[i], ancillas[i], ancillas[i-1])
        circuit.ccx(controls[-2], controls[-1], ancillas[num_ancillas-1])
        for i in range(len(controls)-3, 0, -1):
            circuit.ccx(controls[i], ancillas[i], ancillas[i-1])
        circuit.ccx(controls[0], ancillas[0], target)
        for i in range(1, len(controls)-2):
            circuit.ccx(controls[i], ancillas[i], ancillas[i-1])
        circuit.ccx(controls[-2], controls[-1], ancillas[num_ancillas-1])
        for i in range(len(controls)-3, 0, -1):
            circuit.ccx(controls[i], ancillas[i], ancillas[i-1])



def oracle(array: List[List[int]]):
    number_of_variables = len(array[0])
    number_of_ancillas = len(array) + len(array)-2
    ancilla_index = number_of_variables
    qreg = QuantumRegister(number_of_variables + number_of_ancillas + 1)
    circ = QuantumCircuit(qreg)

    for c in range(len(array)):
        clause = array[c]
        controls = []
        for i in range(number_of_variables):
            if clause[i] != 0:
                controls.append(i)
                if clause[i] == 1:
                    circ.x(i)
        mcx(circ, controls, target=ancilla_index+c, ancillas=[number_of_variables+number_of_ancillas])
        for i in range(number_of_variables):
            if clause[i] == 1:
                circ.x(i)

        circ.barrier()

    check = []
    for i in range(len(array)):
        circ.x(ancilla_index + i)
        check.append(ancilla_index + i)

    backwards = circ.reverse_ops()
    mcx(circ, check, target=number_of_variables+number_of_ancillas, ancillas=[8,9,10])
    result = circ.compose(backwards)

    return result


def grover(N, oracle_circ: QuantumCircuit):
    qreg = QuantumRegister(oracle_circ.num_qubits)
    creg = ClassicalRegister(N)
    circ = QuantumCircuit(qreg, creg)

    # initialization
    for i in range(N):
        circ.h(i)

    circ.barrier()

    iterations = math.floor(math.sqrt(N))
    print("Apply grover iteration %s times" % iterations)
    for x in range(iterations):
        # oracle
        circ = circ.compose(oracle_circ)

        # amplification
        qubits = []
        for i in range(N):
            circ.h(i)
            circ.x(i)
            qubits.append(i)
        qubits.pop(N-1)
        circ.barrier()
        circ.barrier()
        ccz(circ, c1=0, c2=1, target=2, ancilla=3)
        # circ.h(N-1)
        # circ.mcx(qubits, N-1, mode='noancilla')
        # circ.h(N-1)

        for i in range(N):
            circ.x(i)
            circ.h(i)

    circ.barrier()

    for i in range(N):
        # umgekehrte Bitreihenfolge
        circ.measure(i, N-1-i)

    return circ


if __name__ == "__main__":
    quantum_instance = QuantumInstance()
    clauses = "[[-1, -1, -1], [1, -1, 1], [1, 1, -1], [1, -1, -1], [-1, 1, 1]]"
    args = {"clauses": clauses}
    run_algo(quantum_instance, args)

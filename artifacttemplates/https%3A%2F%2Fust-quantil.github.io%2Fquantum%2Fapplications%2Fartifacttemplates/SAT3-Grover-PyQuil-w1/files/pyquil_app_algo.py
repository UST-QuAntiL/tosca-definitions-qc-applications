print("first line of pyquil_app_adapter.py")


from pyquil import Program, get_qc
from pyquil.gates import CCNOT, CZ, X, H, MEASURE
import math
import operator
from typing import List
from ast import literal_eval


######### Function signature & filename must not be changed #########
def run_algo(quantum_device, args):
    print("--- Start run_algo ---")
    clauses = literal_eval(args["clauses"])
    print("Try to find SAT solution for following clauses: %s" % clauses)
    n = len(clauses[0])
    oracle_circuit = oracle(clauses)
    grover_circuit = grover(n, oracle_circuit)
    counts = run(grover_circuit, quantum_device)
    print("Execution results (counts): %s" % counts)
    max_found = max(counts.items(), key=operator.itemgetter(1))[0]
    print("Found solution: %s. Should be one of [000, 101, 110]" % max_found)

    return {'counts': counts, 'max': max_found}


# Each quantum implementation must use this snippet to run the circuit.
def run(circ, quantum_device, shots=100):
    print('execute circuit on %s' % quantum_device)
    result = quantum_device.run(circ.wrap_in_numshots_loop(shots))
    measures = result.readout_data['ro']
    counts = {}
    for measurement in measures:
        x = ''.join(str(x) for x in measurement)
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def ccz(circ: Program, c1: int, c2: int, target: int, ancilla: int):
    circ.inst(CCNOT(c1, c2, ancilla))
    circ.inst(CZ(ancilla, target))
    circ.inst(CCNOT(c1, c2, ancilla))


def mcx(circuit: Program, controls: List[int], ancillas: List[int], target: int):
    num_ancillas = len(controls)-2
    if len(ancillas) < num_ancillas:
        print("Error: Too few ancilla bits for mcx")
    else:
        circuit.inst(CCNOT(controls[0], ancillas[0], target))
        for i in range(1, len(controls)-2):
            circuit.inst(CCNOT(controls[i], ancillas[i], ancillas[i-1]))
        circuit.inst(CCNOT(controls[-2], controls[-1], ancillas[num_ancillas-1]))
        for i in range(len(controls)-3, 0, -1):
            circuit.inst(CCNOT(controls[i], ancillas[i], ancillas[i-1]))
        circuit.inst(CCNOT(controls[0], ancillas[0], target))
        for i in range(1, len(controls)-2):
            circuit.inst(CCNOT(controls[i], ancillas[i], ancillas[i-1]))
        circuit.inst(CCNOT(controls[-2], controls[-1], ancillas[num_ancillas-1]))
        for i in range(len(controls)-3, 0, -1):
            circuit.inst(CCNOT(controls[i], ancillas[i], ancillas[i-1]))


def oracle(array: List[List[int]]):
    number_of_variables = len(array[0])
    number_of_ancillas = len(array) + len(array)-2
    ancilla_index = number_of_variables
    circ = Program()

    for c in range(len(array)):
        clause = array[c]
        controls = []
        for i in range(number_of_variables):
            if clause[i] != 0:
                controls.append(i)
                if clause[i] == 1:
                    circ.inst(X(i))
        mcx(circ, controls, target=ancilla_index+c, ancillas=[number_of_variables+number_of_ancillas])
        for i in range(number_of_variables):
            if clause[i] == 1:
                circ.inst(X(i))

    check = []
    for i in range(len(array)):
        circ.inst(X(ancilla_index + i))
        check.append(ancilla_index + i)

    backwards = circ[::-1]
    mcx(circ, check, target=number_of_variables+number_of_ancillas, ancillas=[8,9,10])
    result = circ + backwards

    return result


def grover(n: int, oracle_circ: Program):
    circ = Program()
    ro = circ.declare('ro', 'BIT', n)

    # initialization
    for i in range(n):
        circ.inst(H(i))

    iterations = math.floor(math.sqrt(n))
    print("Apply grover iteration %s times" % iterations)
    for x in range(iterations):
        # oracle
        circ = circ + oracle_circ

        # amplification
        qubits = []
        for i in range(n):
            circ.inst(H(i))
            circ.inst(X(i))
            qubits.append(i)
        qubits.pop(n - 1)
        ccz(circ, c1=0, c2=1, target=2, ancilla=3)
        # circ.h(N-1)
        # circ.mcx(qubits, N-1, mode='noancilla')
        # circ.h(N-1)

        for i in range(n):
            circ.inst(X(i))
            circ.inst(H(i))

    for i in range(n):
        # reverse bit order
        circ.inst(MEASURE(i, ro[n - 1 - i]))
    return circ


if __name__ == "__main__":
    qc = get_qc('10q-qvm')
    args = {
        'clauses': '[[-1, -1, -1], [1, -1, 1], [1, 1, -1], [1, -1, -1], [-1, 1, 1]]',
        'shots': '100'
    }
    run_algo(qc, args)

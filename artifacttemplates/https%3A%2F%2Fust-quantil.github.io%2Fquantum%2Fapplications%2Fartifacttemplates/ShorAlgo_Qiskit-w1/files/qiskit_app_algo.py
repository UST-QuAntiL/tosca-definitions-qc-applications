from qiskit.algorithms import Shor


######### Function signature & filename must not be changed #########
def run_algo(quantum_instance, args):

    print('Number:', args["Number"])

    algo = Shor(quantum_instance)
    
    result = algo.factor(int(args["Number"]))

    return {'factors': result.factors[0]}

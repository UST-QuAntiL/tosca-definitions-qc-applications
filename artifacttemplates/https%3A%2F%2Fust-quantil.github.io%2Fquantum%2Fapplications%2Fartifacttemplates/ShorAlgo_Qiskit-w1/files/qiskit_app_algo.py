from qiskit.aqua.algorithms import Shor


######### Function signature & filename must not be changed #########
def run_algo(quantum_instance, args):

    print('Number:', args["Number"])

    algo = Shor(int(args["Number"]))
    
    result = algo.run(quantum_instance)
	
    return {'factors': result["factors"]}

	

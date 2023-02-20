import boto3
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit


######### Function signature & filename must not be changed #########
def run_algo(args):
    # create the circuit
    circuit = Circuit()
    for i in range(int(args["bitlength"])):
        circuit = circuit.h(i)

    device = LocalSimulator()
    if args["device"]:
        device = AwsDevice(args["device"])

    result = device.run(circuit, shots=1).result()
    print(list(dict(result.measurement_counts).keys())[0])

    return {'number': list(dict(result.measurement_counts).keys())[0]}

if __name__ == '__main__':
    run_algo({"device":"", "bitlength":2})
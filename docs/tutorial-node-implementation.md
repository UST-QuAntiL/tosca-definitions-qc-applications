# Tutorial: Create Custom Nodes

This tutorial takes you through the steps to create a new node with implementation to use in a TOSCA topology.
The tutorial will lead you throgh recreating a node from the [Tutorial: Model and Deploy an Application with OpenTOSCA](./tutorial-model-and-deploy.md).

:information_source: Terms in *italics* can be found in the [glossary](tosca-glossary.md).

**Requirements:**

 *  [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (with GIT-LFS)
 *  [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
 *  Optional: At least 6GB RAM free for the OpenTOSCA complete docker-compose

Before starting with this tutorial clone the <https://github.com/OpenTOSCA/opentosca-docker> repository and read through the relevant sections of the README once (e.g. the first two sections, tips and tricks and troubleshooting).

If the modeled node should be comitted to a repository it is best to use a local repository (see <https://github.com/OpenTOSCA/opentosca-docker/blob/main/docs/advanced-how-to.md#how-to-use-an-existing-local-winery-repository>).
For this tutorial only the winery container needs to be started.


## Create a new Node

### 1. Start the Winery

Before a node can be created, first start a winery instance with the main repository set to where the node should be created.

We will use the `https://github.com/UST-QuAntiL/tosca-definitions-quantil` repository for this tutorial.

:information_source: Reusable *node types*, e.g., nodes that will be used by multiple applications should be placed in a common repository. Application specific node types should be placed in the application specific repositories.


### 2. Create a new Node

Open the `Node Types` tab in the winery and click on the `Add new` button on the right.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | CustomQiskit | |
| Versioning | Enabled | (optional) |
| Version | latest | (optional) |
| Namespace | `https://ust-quantil.github.io/nodetypes` ||

Optionally create a README, choose a license and customize the node appeareance.

:information_source: In the case that an existing node should be extended go to the inheritance tab and select the node type to inherit from.


### 3. Define Node Properties

The original Qiskit node does not have a *property*, but for this tutorial we will define one. Open the `Property Definitions` tab.

Select `Custom key/value pairs` to create new properties. Then click on the `Add` button to create a new Property.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `qiskitVersion` | |
| Type | `xsd:string` | |

Leave the rest empty and hit `Save`.

### 4. Create the Lifecycle Interface

A *node type* in TOSCA needs to define *interfaces* that contain the *methods* that can be called/executed on that node type.

First open the `interfaces` tab.

Click on the `Generate Lifecycle Interface` to create a new lifecycle interface for this *node type*.

:information_source: The lifecycle interface defines methods for, e.g., installing, configuring, and starting a node type.

For our quiskit node we only need to install the dependency so we can delete all other methods of the lifecycle interface.

Click on the `install` method to define input parameters. Click on the `Add` button of the input parameters.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `qiskitVersion` | |
| Type | `xsd:string` | |
| Required | False | |

Hit `Add` to add the input parameter.
This makes the (optional) `qiskitVersion` property available to all implementations of this interface method.

:information_source: The properties can come from the same node or any node this node depends on in a topology (e.g., with a hostedOn edge). Therefore, it is good to choose unique names for properties that should not be used generically (i.e. `qiskitVersion` instead of `version`).


### 5. Create the Connection Interface

Nodes that can connect to other nodes, e.g., our quiskit node should be able to connect to the IBMQ cloud, an interface implementing that connection needs to be added as well.
Click on the `Add` button of interfaces to create a new one.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `http://opentosca.org/interfaces/connectTo/ibmq` | |

:information_source: The interface name can be freely chosen for this. Opentosca will execute **any** interface with a *connectsTo* method for a *connectsTo* node relation. This can be used to implement multiple different connections. However, it is a good practise to include the connection type in the interface name.

Select the created interface and add a new method.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `connectTo` | |

* TODO add input parameters (see real qiskit node)

| Name | Type | Required |
|:-------|:------|:---------------|
| IBMQ_TOKEN |xsd:string | NO |
| PROVIDER |xsd:string | NO |
| IBMQ_BACKEND_NAME |xsd:string | NO |
| IBMQ_GROUP |xsd:string | NO |
| IBMQ_PROJECT |xsd:string | NO |
| IBMQ_HUB |xsd:string | NO |

:information_source: SOURCE_ and TARGET_ prefixes...

:information_source: Interface methods will only be called if their properties can be satisfied/filled in => use this to differentiate between different connectsTo implementations

### 6. Add an Implementation

Open the `implementations` tab and click on `Add` to create a new implementation.

<!-- Rest wie vorausgefüllt -->
| Namespace | `https://ust-quantil.github.io/nodetypeimplementations` | |


## Implement the Node Type

### 1. Open the created node type implementation

create readme license etc.

### 2. Create Lifecycle implementation

Go to the *`implementation artifacts`* tab.

TODO: write text, add script artefact

### 3. Create ConnectsTo implementation

:information_source: Multiple connects tos with config updates: Restart things if needed; Write config to disc; PID files


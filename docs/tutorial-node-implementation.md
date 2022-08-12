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

**Table of contents**

[Create a new Node](#create-a-new-node)
1. [Start Winery](#1-start-winery)
2. [Create a new Node](#2-create-a-new-node)
3. [Define Node Properties](#3-define-node-properties)
4. [Create the Lifecycle Interface](#4-create-the-lifecycle-interface)
5. [Create the Connection Interface](#5-create-the-connection-interface)
6. [Add an Implementation](#6-add-an-implementation)

[Implement the Node Type](#implement-the-node-type)
1. [Add infos (optional)](#1-add-infos-optional)
2. [Create Lifecycle implementation](#2-create-lifecycle-implementation)
3. [Explanation of the install script](#3-explanation-of-the-install-script)
4. [Create ConnectsTo implementation](#4-create-connectsto-implementation)
5. [Explanation of the ConnectTo script](#5-explanation-of-the-connectto-script)

[Deployment Artefacts](#deployment-artefacts)

[Tips and tricks](#tips-and-tricks)


## Create a new Node

This chapter is an example on how to create a new `Node Type`.
We will recreate the Qiskit node type from the repository `https://github.com/UST-QuAntiL/tosca-definitions-quantil` .

### 1. Start Winery

Before a node can be created, first start a winery instance with the main repository set to where the node should be created.

We will use the `https://github.com/UST-QuAntiL/tosca-definitions-quantil` repository for this tutorial.

To do this you can open the docker-compose.yml file and replace the WINERY_REPOSITORY_URL of the winery container. To start only the winery container you can use the command `docker-compose up winery` .

:information_source: Reusable *node types*, e.g., nodes that will be used by multiple applications should be placed in a common repository. Application specific node types should be placed in the application specific repositories.


### 2. Create a new Node

Open Winery in your browser (default URL: http://localhost:8080) and click on the `Node Types` tab.
Click on the `Add new` button on the right.

![Create new node type in winery](./images/new_node_type/new.png)

Enter the following values into the dialog and click on `Add`:

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | CustomQiskit | |
| Versioning | Enabled | (optional) |
| Version | latest | (optional) |
| Namespace | `https://ust-quantil.github.io/nodetypes` ||

![New node type dialog](./images/new_node_type/new_dialog.png)

Optionally create a README, choose a license and customize the node appeareance.

![Node type readme](./images/new_node_type/readme.png)

:information_source: In the case that an existing node should be extended go to the inheritance tab and select the node type to inherit from.


### 3. Define Node Properties

The original Qiskit node does not have a *property*, but for this tutorial we will define one. Open the `Property Definitions` tab.

Select `Custom key/value pairs` to create new properties. Then click on the `Add` button to create a new Property.

![Node type new property](./images/new_node_type/new_property.png)

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `qiskitVersion` | |
| Type | `xsd:string` | data type |

Leave the rest empty and hit `Save`.

![Node type new property dialog](./images/new_node_type/new_property_dialog.png)

### 4. Create the Lifecycle Interface

A *node type* in TOSCA needs to define *interfaces* that contain the *methods* that can be called/executed on that node type.

First open the `interfaces` tab.

Click on the `Generate Lifecycle Interface` to create a new lifecycle interface for this *node type*.

:information_source: The lifecycle interface defines methods for, e.g., installing, configuring, and starting a node type.

![Generate Lifecycle Interface](./images/new_node_type/interfaces/generate_interfaces.png)

For our quiskit node we only need to install the dependency so we can delete all other methods of the lifecycle interface.

![Delete unused operations](./images/new_node_type/interfaces/delete_operations.png)

Click on the `install` method to define input parameters. Click on the `Add` button of the input parameters.

![Add input parameters](./images/new_node_type/interfaces/add_input_parameters.png)

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `qiskitVersion` | |
| Type | `xsd:string` | data type |
| Required | False | if the user needs to supply a value |

![Add inputer parameters dialog](./images/new_node_type/interfaces/add_input_parameters_dialog.png)

Hit `Add` to add the input parameter and `Save` to save the changes you made.
This makes the (optional) `qiskitVersion` property available to all implementations of this interface method.

![Save](./images/new_node_type/interfaces/save.png)

:information_source: The properties can come from the same node or any node this node depends on in a topology (e.g., with a hostedOn edge). Therefore, it is good to choose unique names for properties that should not be used generically (i.e. `qiskitVersion` instead of `version`).


### 5. Create the Connection Interface

Nodes that can connect to other nodes, e.g., our qiskit node should be able to connect to the IBMQ cloud, an interface implementing that connection needs to be added as well.
Click on the `Add` button of interfaces to create a new one.

![Add interface](./images/new_node_type/interfaces/connectto/add_interface.png)

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `http://opentosca.org/interfaces/connectTo/ibmq` | |

:information_source: The interface name can be freely chosen for this. Opentosca will execute **any** interface with a *connectsTo* method for a *connectsTo* node relation. This can be used to implement multiple different connections. However, it is a good practise to include the connection type in the interface name.

Select the created interface and add a new operation.

| Field | Value | Explanation |
|:-------|:------|:---------------|
| Name | `connectTo` | |

![Add operation](./images/new_node_type/interfaces/connectto/add_operation.png)

Add the following input parameters:

| Name | Type | Required |
|:-------|:------|:---------------|
| IBMQ_TOKEN |xsd:string | NO |
| PROVIDER |xsd:string | NO |
| IBMQ_BACKEND_NAME |xsd:string | NO |
| IBMQ_GROUP |xsd:string | NO |
| IBMQ_PROJECT |xsd:string | NO |
| IBMQ_HUB |xsd:string | NO |

![Add input parameters](./images/new_node_type/interfaces/connectto/add_input_parameters.png)

:information_source: Interface methods will only be called if their properties can be satisfied/filled in => use this to differentiate between different connectsTo implementations

Save the changes you made.

![Save](./images/new_node_type/interfaces/connectto/save.png)

### 6. Add an Implementation

Open the `implementations` tab and click on `Add` to create a new implementation.

![Implementations](./images/new_node_type/implementations/implementations.png)

| Field | Value | Required |
|:------|:------|:---------|
| Enable Versioning | True | No |
| Namespace | `https://ust-quantil.github.io/nodetypeimplementations` | YES |

Use the default values for the rest of the fields.

![new implementation](./images/new_node_type/implementations/new_implementation_dialog.png)

The new implementation opens automatically.


## Implement the Node Type

### 1. Add infos (optional)

Go to the new implementation if it's not open already.
Here you can add a readme and license if you want.

![Implementation readme](./images/new_node_type/implementations/implementation_readme.png)

### 2. Create Lifecycle implementation

Go to the *`implementation artifacts`* tab.
Add the `install` artefact.

![Add implementation artefact](./images/new_node_type/implementations/implementation_artefacts/add_new.png)

Enter the following values:

| Field | Value | Required |
|:------|:------|:--------|
| Name | Qiskit_Install | Yes |
| Interface Name | http://opentosca.org/interfaces/lifecycle | Yes |
| Operation Name | install | Yes |
| Artifact Template Creation | Create Artifact Template | Yes |
| Enable Versioning | True | No |
| Type | ScriptArtefact | Yes |
| Namespace | https://ust-quantil.github.io/artifacttemplates | Yes |

![Install artefact](./images/new_node_type/implementations/implementation_artefacts/install_1.png)

![Install artefact](./images/new_node_type/implementations/implementation_artefacts/install_2.png)

Upload the script [install.sh](./images/new_node_type/implementations/implementation_artefacts/install.sh):

![Upload artefact](./images/new_node_type/implementations/implementation_artefacts/install_upload.png)

### 3. Explanation of the install script

```bash
#!/bin/bash

sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip -qq
	
pip3 install --upgrade pip
pip install qiskit==${qiskitVersion}

```

This script installs Pip, updates it and then installs Qiskit with the specified version.
The version can be specified with the input parameter `qiskitVersion` of install interface and is available in the script as an environment variable.

### 4. Create ConnectsTo implementation

Add the `connectTo` artefact.
Enter the following values:

| Field | Value | Required |
|:------|:------|:--------|
| Name | Qiskit_ConnectTo | Yes |
| Interface Name | http://opentosca.org/interfaces/connectTo/ibmq | Yes |
| Operation Name | connectTo | Yes |
| Artifact Template Creation | Create Artifact Template | Yes |
| Enable Versioning | True | No |
| Type | ScriptArtefact | Yes |
| Namespace | https://ust-quantil.github.io/artifacttemplates | Yes |

![Connect-to artefact](./images/new_node_type/implementations/implementation_artefacts/connect_to_1.png)
![Connect-to artefact](./images/new_node_type/implementations/implementation_artefacts/connect_to_2.png)

Upload the script [connectTo.sh](./images/new_node_type/implementations/implementation_artefacts/connectTo.sh):

![Connect-to upload](./images/new_node_type/implementations/implementation_artefacts/connect_to_upload.png)

:information_source: Multiple connects tos with config updates: Restart things if needed; Write config to disc; PID files

### 5. Explanation of the ConnectTo script

```bash
#!/bin/bash

sudo mkdir -p qiskit_app

echo "PROVIDER=${PROVIDER}" >> qiskit_app/.env

echo "AER_BACKEND_NAME=${AER_BACKEND_NAME}" >> qiskit_app/.env

echo "IBMQ_TOKEN=${IBMQ_TOKEN}" >> qiskit_app/.env
echo "IBMQ_BACKEND_NAME=${IBMQ_BACKEND_NAME}" >> qiskit_app/.env
echo "IBMQ_HUB=${IBMQ_HUB}" >> qiskit_app/.env
echo "IBMQ_GROUP=${IBMQ_GROUP}" >> qiskit_app/.env
echo "IBMQ_PROJECT=${IBMQ_PROJECT}" >> qiskit_app/.env
```

This script helps to make the user input available to the Qiskit application.
Again, the values of the input parameters are available in environment variables.
This script writes the values of the input parameters of the `connectTo` interface to the file `qiskit_app/.env`.
The Qiskit application can then read these values from the file.

<!-- TODO: Python Artefact -->

## Deployment artefacts

Deployment artefacts implement the business logic of an application e.g. the jar file for a Tomcat web server.
If you want to create a node type that has e.g. a jar file as deployment artefact, you need to also create an interface with an implementation artefact that can execute this file.

**Example with a jar file as deployment artefact**
- create a `node type`
- create an `interface` with a `start operation` for this `node type`
- create a `node type implementation` for this `node type`
- add a `deployment artefact` to the `node type implementation`
![deployment artefact](./images/new_node_type/deployment%20artefacts/jar_artefact.png)
- upload the `jar file` to the `deployment artefact`
- add a `ScriptArtefact` as `implementation artefact` for the `start operation` to the `node type implementation`
![implementation artefact](./images/new_node_type/deployment%20artefacts/start_artefact.png)
- upload a `script` to the `ScriptArtefact` that executes the `jar file`

Example script to execute a `jar file`:
```bash
#!/bin/bash

echo "Starting QHana-Backend"

cd qhana_backend
java -jar qhana_backend.jar
echo "Done"

sleep 5
```

## Tips and tricks

**Access input parameters of source and target nodes:**
In an implementation artefact of a `connectTo` interface you can prefix environment variables with `SOURCE_` or `TARGET_` to specify whether you want the input parameter of the source or target node respectively.
This helps in cases where the source and target node have an input parameter with the same name.

**Ways to debug implementations:**
- Enter the container and execute the implementation manually
- Write debug information (logs) to a file, then copy that file from the container to your disk

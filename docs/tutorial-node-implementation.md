# Tutorial: Create Custom Node Types

This tutorial takes you through the steps to create a new `Node Type` with implementation to use it in a `Topology Template`.
The tutorial will lead you through recreating a `Node Type` from the [Tutorial: Model and Deploy an Application with OpenTOSCA](./tutorial-model-and-deploy.md).

:information_source: Explanations of important terms can be found in the [glossary](tosca-glossary.md).

**Requirements:**

 *  [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (with GIT-LFS)
 *  [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
 *  Optional: At least 6GB RAM free for the OpenTOSCA complete docker-compose

Before you start with this tutorial, clone the <https://github.com/OpenTOSCA/opentosca-docker> repository and read through the relevant sections of the README once (e.g. the first two sections, tips and tricks, and troubleshooting).

To avoid loosing your progress after terminating the Docker Compose setup, use a local repository (see <https://github.com/OpenTOSCA/opentosca-docker/blob/main/docs/advanced-how-to.md#how-to-use-an-existing-local-winery-repository>).
In this tutorial, you only need the `winery` container, but you can start the whole ecosystem as well.

**Table of contents**

[Create a new Node Type](#create-a-new-node-type)
1. [Configure the Docker setup and start Winery](#1-configure-the-docker-setup-and-start-winery)
2. [Create a new Node Type](#2-create-a-new-node-type)
3. [Define Properties](#3-define-properties)
4. [Create the Lifecycle Interface](#4-create-the-lifecycle-interface)
5. [Create the Connection Interface](#5-create-the-connection-interface)
6. [Add a Node Type Implementation](#6-add-a-node-type-implementation)

[Implement the Node Type](#implement-the-node-type)
1. [Add infos (optional)](#1-add-infos-optional)
2. [Create Lifecycle implementation](#2-create-lifecycle-implementation)
3. [Explanation of the install script](#3-explanation-of-the-install-script)
4. [Create ConnectsTo implementation](#4-create-connectsto-implementation)
5. [Explanation of the ConnectTo script](#5-explanation-of-the-connectto-script)

[Example of a PythonScriptArtifact](#example-of-a-pythonscriptartifact)

[Deployment Artifacts](#deployment-artifacts)

[Tips and tricks](#tips-and-tricks)


## Create a new Node Type

This chapter is an example of how to create a new `Node Type`.
We will recreate the Qiskit `Node Type` from the repository `https://github.com/UST-QuAntiL/tosca-definitions-quantil` .

### 1. Configure the Docker setup and start Winery

Before a `Node Type` can be created, first start a winery instance with the main repository set to where the `Node Type` should be created.
We will use the `https://github.com/UST-QuAntiL/tosca-definitions-quantil` repository for this tutorial.
To do this, go to the opentosca-docker folder that you have cloned earlier and add a `docker-compose.override.yml` file with the following content and replace `path-to-folder` with the absolute path to the `opentosca-docker` folder:

```yml
version: '3'
services:
  winery:
    environment:
      WINERY_REPOSITORY_PATH: /var/opentosca/repository
      WINERY_REPOSITORY_URL: https://github.com/UST-QuAntiL/tosca-definitions-quantil
    volumes:
      - /path-to-folder/opentosca-docker/repository:/var/opentosca/repository
```

To start only the winery container, you can use the command `docker-compose up winery`.

:information_source: Reusable `Node Types` that, e.g., can be used by multiple applications, should be placed in a common repository. On the other hand, application-specific `Node Types` should be placed in the application-specific repositories.
The application-specific repository can then import the common repositories.
Therefore, the user has to create a `repositories.json` file in the root directory of the repository.
In this file all repositories to be imported are listed with their name, repository url and branch:
```json
[ {
  "name" : "Normative Types",
  "url" : "https://github.com/OpenTOSCA/tosca-normative-types",
  "branch" : "main"
},
{
  "name" : "Common Types",
  "url" : "https://github.com/OpenTOSCA/tosca-definitions-common",
  "branch" : "main"
},
{
  "name" : "QuAntiL Types",
  "url" : "https://github.com/UST-QuAntiL/tosca-definitions-quantil",
  "branch" : "main"
} ] 
```
The content of the current repository is in the workspace folder.


### 2. Create a new Node Type

Open Winery in your browser (default URL: http://localhost:8080) and click on the `Node Types` tab.
Click on the `Add new` button on the right.

![Create new node type in winery](./images/new_node_type/new.png)

Enter the following values into the dialog and click on `Add`:

| Field      | Value                                     | Explanation |
|:-----------|:------------------------------------------|:------------|
| Name       | CustomQiskit                              |             |
| Versioning | Enabled                                   | (optional)  |
| Version    | latest                                    | (optional)  |
| Namespace  | `https://ust-quantil.github.io/nodetypes` |             |

![New node type dialog](./images/new_node_type/new_dialog.png)

Optionally create a README, choose a license and customize the appearance.

![Node type readme](./images/new_node_type/readme.png)

:information_source: In the case that an existing `Node Type` should be extended, go to the inheritance tab and select the `Node Type` to inherit from.


### 3. Define Properties

The original Qiskit `Node Type` does not have a `property`, but for this tutorial, we will define one. Open the `Property Definitions` tab.

Select `Custom key/value pairs` to create new properties. Then click on the `Add` button to create a new Property.

![Node type new property](./images/new_node_type/new_property.png)

| Field | Value           | Explanation |
|:------|:----------------|:------------|
| Name  | `qiskitVersion` |             |
| Type  | `xsd:string`    | data type   |

Leave the rest empty and hit `Save`.

![Node type new property dialog](./images/new_node_type/new_property_dialog.png)

### 4. Create the Lifecycle Interface

A `Node Type` in TOSCA needs to define `interfaces` that contain the `operations` that can be called/executed on that `Node Type`.

First, open the `interfaces` tab.

Click on the `Generate Lifecycle Interface` to create a new lifecycle interface for this `Node Type`.

:information_source: The lifecycle interface defines operations for, e.g., installing, configuring, and starting a `Node Type`.

![Generate Lifecycle Interface](./images/new_node_type/interfaces/generate_interfaces.png)

For our Qiskit `Node Type`, we only need to install the dependency so we can delete all other operations of the lifecycle interface.

![Delete unused operations](./images/new_node_type/interfaces/delete_operations.png)

Click on the `install` operation to define input parameters. Then, click on the `Add` button of the input parameters.

![Add input parameters](./images/new_node_type/interfaces/add_input_parameters.png)

| Field    | Value           | Explanation                         |
|:---------|:----------------|:------------------------------------|
| Name     | `qiskitVersion` |                                     |
| Type     | `xsd:string`    | data type                           |
| Required | `False`         | if the user needs to supply a value |

![Add input parameters dialog](./images/new_node_type/interfaces/add_input_parameters_dialog.png)

Hit `Add` to add the input parameter and `Save` to save the changes you made.
This makes the (optional) `qiskitVersion` property available to all implementations of this interface operation.

![Save](./images/new_node_type/interfaces/save.png)

:information_source: The properties can come from the same `Node Type`, or any `Node Type` this `Node Type` depends on in a `Topology Template` (e.g., with a hostedOn edge). Therefore, it is good to choose unique names for properties that should not be used generically (i.e. `qiskitVersion` instead of `version`).


### 5. Create the Connection Interface

`Node Types` that can connect to other `Node Types`, e.g. our Qiskit `Node Type` should be able to connect to the IBMQ cloud, need an interface implementing that connection.
Click on the `Add` button of interfaces to create a new one.

![Add interface](./images/new_node_type/interfaces/connectto/add_interface.png)

| Field | Value                                            | Explanation |
|:------|:-------------------------------------------------|:------------|
| Name  | `http://opentosca.org/interfaces/connectTo/ibmq` |             |

:information_source: The interface name can be freely chosen for this. OpenTOSCA will execute **any** interface with a `connectsTo` operation for a `connectsTo` node relation. This can be used to implement multiple different connections. However, it is a good practice to include the connection type in the interface name.

Select the created interface and add a new operation.

| Field | Value       | Explanation |
|:------|:------------|:------------|
| Name  | `connectTo` |             |

![Add operation](./images/new_node_type/interfaces/connectto/add_operation.png)

Add the following input parameters:

| Name              | Type       | Required |
|:------------------|:-----------|:---------|
| IBMQ_TOKEN        | xsd:string | NO       |
| PROVIDER          | xsd:string | NO       |
| IBMQ_BACKEND_NAME | xsd:string | NO       |
| IBMQ_GROUP        | xsd:string | NO       |
| IBMQ_PROJECT      | xsd:string | NO       |
| IBMQ_HUB          | xsd:string | NO       |

![Add input parameters](./images/new_node_type/interfaces/connectto/add_input_parameters.png)

:information_source: Interface operations will only be called if their properties can be satisfied/filled in => use this to differentiate between different connectsTo implementations

Save the changes you made.

![Save](./images/new_node_type/interfaces/connectto/save.png)

### 6. Add a Node Type Implementation

Open the `implementations` tab and click on `Add` to create a new implementation.

![Implementations](./images/new_node_type/implementations/implementations.png)

| Field             | Value                                                   | Required |
|:------------------|:--------------------------------------------------------|:---------|
| Enable Versioning | True                                                    | NO       |
| Namespace         | `https://ust-quantil.github.io/nodetypeimplementations` | YES      |

Use the default values for the rest of the fields.

![new implementation](./images/new_node_type/implementations/new_implementation_dialog.png)

The new implementation opens automatically.


## Implement the Node Type

### 1. Add infos (optional)

Go to the new implementation if it is not open already.
Here you can add a readme and license if you want.

![Implementation readme](./images/new_node_type/implementations/implementation_readme.png)

### 2. Create Lifecycle implementation

Go to the `Implementation Artifacts` tab.
Add the `install` artifact.

![Add implementation artifact](./images/new_node_type/implementations/implementation_artifacts/add_new.png)

Enter the following values:

| Field                      | Value                                           | Required |
|:---------------------------|:------------------------------------------------|:---------|
| Name                       | Qiskit_Install                                  | Yes      |
| Interface Name             | http://opentosca.org/interfaces/lifecycle       | Yes      |
| Operation Name             | install                                         | Yes      |
| Artifact Template Creation | Create Artifact Template                        | Yes      |
| Enable Versioning          | True                                            | No       |
| Type                       | ScriptArtifact                                  | Yes      |
| Namespace                  | https://ust-quantil.github.io/artifacttemplates | Yes      |

![Install artifact](./images/new_node_type/implementations/implementation_artifacts/install_1.png)

![Install artifact](./images/new_node_type/implementations/implementation_artifacts/install_2.png)

Upload the script [install.sh](./images/new_node_type/implementations/implementation_artifacts/install.sh):

![Upload artifact](./images/new_node_type/implementations/implementation_artifacts/install_upload.png)

### 3. Explanation of the install script

```bash
#!/bin/bash

sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip -qq
    
pip3 install --upgrade pip
pip install qiskit==${qiskitVersion}

```

This script installs Pip, updates it, and then installs Qiskit with the specified version.
The version can be specified with the input parameter `qiskitVersion` of the install interface and is available in the script as an environment variable.

### 4. Create ConnectsTo implementation

Add the `connectTo` artifact.
Enter the following values:

| Field                      | Value                                           | Required |
|:---------------------------|:------------------------------------------------|:---------|
| Name                       | Qiskit_ConnectTo                                | Yes      |
| Interface Name             | http://opentosca.org/interfaces/connectTo/ibmq  | Yes      |
| Operation Name             | connectTo                                       | Yes      |
| Artifact Template Creation | Create Artifact Template                        | Yes      |
| Enable Versioning          | True                                            | No       |
| Type                       | ScriptArtifact                                  | Yes      |
| Namespace                  | https://ust-quantil.github.io/artifacttemplates | Yes      |

![Connect-to artifact](./images/new_node_type/implementations/implementation_artifacts/connect_to_1.png)
![Connect-to artifact](./images/new_node_type/implementations/implementation_artifacts/connect_to_2.png)

Upload the script [connectTo.sh](./images/new_node_type/implementations/implementation_artifacts/connectTo.sh):

![Connect-to upload](./images/new_node_type/implementations/implementation_artifacts/connect_to_upload.png)

:information_source: Multiple connectTos with config updates: Restart things if needed; Write config to disc; PID files

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

## Example of a PythonScriptArtifact
So far we have implemented all methods as bash scripts. But Python scripts are supported as well.
The following example script installs `Deployment Artifacts` and requirements of the `Node Type` QHAna-PluginRunner version latest-w2.

```python
# !/usr/bin/env python
import sys
import subprocess
from collections import ChainMap
from os import environ
from pathlib import Path
from zipfile import ZipFile
from shutil import copyfile
from shlex import join as cmd_join
from subprocess import PIPE


def argv_to_dict(argv):
    return dict(arg.split('=', maxsplit=1) for arg in argv if '=' in arg)


def printOutput(dict):
    for key in dict:
        print(str(key) + '=' + str(dict[key]))


def install_requirements(environ):
    cmd = ['apt-get', 'update', '-qq']
    print(cmd_join(cmd))
    subprocess.run(cmd)
    cmd = ['apt-get', 'install', 'git', '-qq']
    print(cmd_join(cmd))
    subprocess.run(cmd)


def install_deployment_artifacts(environ):
    das = (da.strip() for da in environ.get('DAs', '').split(';') if da.strip())
    plugin_runner_found = False
    for da in das:
        print('DA:', da)
        result = da.split(',', maxsplit=1)
        da_path = Path('/') / environ.get('CSAR', '').strip('/') / result[1].lstrip('/')
        if da_path.suffix == '.zip':
            if result[0] == 'QHAna-PluginRunner_DA':
                plugin_runner_found = True
                print('install plugin runner DA', *result)
                install_plugin_runner(da_path)
            else:
                print('install plugin DA', *result)
                install_plugin(da_path)
    if not plugin_runner_found:
        print('ERROR: No plugin runner DA!!!')


def extract_zip(source, target):
    target.mkdir(parents=True, exist_ok=True)
    with source.open(mode='rb') as zip_file:
        ZipFile(zip_file).extractall(target)


def install_plugin_runner(zip_da):
    if not zip_da.exists():
        print('ERROR: DA not found at ', zip_da)
        return
    target = Path('src')
    extract_zip(zip_da, target)
    # TODO unpin versions if possible
    cmd = ['python3', '-m', 'pip', 'install', 'PyMySQL', 'poetry', 'mysql-connector-python==8.0.26']
    print(cmd_join(cmd))
    subprocess.run(cmd)
    for f in ['tasks.py', 'pyproject.toml', 'poetry.lock']:
        copyfile(target / f, Path('.') / f)
    cmd = ['python3', '-m', 'poetry', 'export', '--without-hashes']
    requirments = subprocess.run(cmd, stdout=PIPE)
    req_file = Path('requirements.txt')
    with req_file.open(mode='w') as f:
        f.write(f'{target.resolve()}\n')
        f.write(requirments.stdout.decode())
    cmd = ['python3', '-m', 'pip', 'install', '-r', str(req_file.resolve())]
    print(cmd_join(cmd))
    subprocess.run(cmd)


def install_plugin(zip_da):
    if not zip_da.exists():
        print('ERROR: DA not found at ', zip_da)
        return
    extract_zip(zip_da, Path('plugins'))


def post_install(environ):
    extra_env = {
        'FLASK_APP': 'qhana_plugin_runner',
        'FLASK_ENV': 'production',
        'PLUGIN_FOLDERS': 'plugins:git-plugins'
    }

    cmd = ['python3', '-m', 'invoke', 'load-git-plugins']
    print(cmd_join(cmd), 'env:', extra_env)
    subprocess.run(cmd, env=ChainMap(extra_env, environ))
    cmd = ['python3', '-m', 'flask', 'install']
    print(cmd_join(cmd), 'env:', extra_env)
    subprocess.run(cmd, env=ChainMap(extra_env, environ))


def main(argv):
    print('pwd', Path('.').resolve())
    print(argv)
    env = ChainMap(argv_to_dict(argv), environ)
    install_requirements(env)
    install_deployment_artifacts(env)
    post_install(env)


if __name__ == "__main__":
    main(sys.argv[1:])
```

### Explanation

`PythonScriptArtifacts` get the user input not as environment variables but as command-line arguments.
The function `argv_to_dict` converts the command-line arguments to a dictionary for easy access.
The `ChainMap` class is used to merge multiple dictionaries, i.e., to merge the command-line arguments with the environment variables.
`install_requirements` installs git.
The file names of the `Deployment Artifacts` are passed as environment variables to the script under the key `DAs`, and the path to the unzipped `CSAR` folder can be found under the key `CSAR`.
The function `install_deployment_artifacts` calculates the paths to the `Deployment Artifacts`,
checks the type, and calls the right install functions.
`install_plugin_runner` unpacks the passed `Deployment Artifact` and installs required Python packages, `install_plugin` unpacks the passed `Deployment Artifact` into the plugins folder.
In the end, `post_install` executes commands to configure the application and install more dependencies.


## Deployment Artifacts

`Deployment Artifacts` implement the business logic of an application, e.g., the jar file for a Tomcat web server.
If you want to create a `Node Type` that has, e.g., a jar file as a deployment artifact, you need to create an interface with an implementation artifact that can execute this file.

**Example with a jar file as deployment artifact**
- create a `Node Type`
- create an `Interface` with a `start operation` for this `Node Type`
- create a `Node Type Implementation` for this `Node Type`
- add a `Deployment Artifact` to the `Node Type Implementation`
![deployment artifact](./images/new_node_type/deployment%20artifacts/jar_artifact.png)
- upload the `jar file` to the `Deployment Artifact`
- add a `ScriptArtifact` as `Implementation Artifact` for the `start operation` to the `Node Type Implementation`
![implementation artifact](./images/new_node_type/deployment%20artifacts/start_artifact.png)
- upload a `script` to the `ScriptArtifact` that executes the `jar file`

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

**Access input parameters of source and target Node Types:**
In an `Implementation Artifact` of a `connectTo` interface, you can prefix environment variables with `SOURCE_` or `TARGET_` to specify whether you want the input parameter of the source or target `Node Type`, respectively.
This helps in cases where the source and target `Node Type` have a property with the same name.

**Ways to debug implementations:**
- Enter the container and execute the implementation manually
- Write debug information (logs) to a file, then copy that file from the container to your disk

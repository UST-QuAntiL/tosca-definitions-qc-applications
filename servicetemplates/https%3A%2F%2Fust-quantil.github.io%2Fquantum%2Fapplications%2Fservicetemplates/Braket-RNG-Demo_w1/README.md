# Braket RNG on AWS (+ Demo UI)

> Deploys Python, Boto3 SDK, & Braket SDK on a Ubuntu Docker Container and installs and runs an RNG Braket app on a quantum backend available at AWS.
> A second Docker Container with a Demo UI is deployed and connected to the app.

## Properties

- `FrontendPort` Port used for the frontend service
- `BackendPort` Port used for the backend service
- `DockerEngineURL` Docker engine URL
- `AWS_ACCESS_KEY_ID`: AWS Access Key ID of a User with permission to run circuits via Braket
- `AWS_SECRET_ACCESS_KEY` Corresponding secret access key
- `AWS_REGION` AWS region

## Haftungsausschluss

Dies ist ein Forschungsprototyp und enthält insbesondere Beiträge von Studenten. Diese Software enthält möglicherweise Fehler und funktioniert möglicherweise, insbesondere bei variierten oder neuen Anwendungsfällen, nicht richtig. Insbesondere beim Produktiveinsatz muss 1. die Funktionsfähigkeit geprüft und 2. die Einhaltung sämtlicher Lizenzen geprüft werden. Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden ausgeschlossen.

## Disclaimer of Warranty

Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor
provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT,
MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the
appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of
permissions under this License.

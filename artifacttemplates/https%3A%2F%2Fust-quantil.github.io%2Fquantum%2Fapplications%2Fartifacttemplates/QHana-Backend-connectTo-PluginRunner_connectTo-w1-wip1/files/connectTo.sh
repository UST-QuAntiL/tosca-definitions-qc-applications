#!/bin/sh

cd qhana_backend

cat << EOF >> Config.toml

qhana.qhana_backend.pluginRunners = ["http://${TARGET_ContainerIP}:${TARGET_Port}"]

EOF

kill $(pgrep -f 'java')

nohup java -jar qhana_backend.jar &

sleep 10
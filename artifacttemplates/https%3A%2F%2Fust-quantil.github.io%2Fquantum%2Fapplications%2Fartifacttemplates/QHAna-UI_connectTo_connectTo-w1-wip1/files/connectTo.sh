#!/bin/sh

cat << EOF >> Config.test

"${TARGET_ContainerIP}:${TARGET_BackendPort}"

EOF


sleep 10
#!/bin/bash

# install gettext for envsubst
sudo apt-get update -qq
sudo apt-get -qqy install gettext-base

export QHANA_BACKEND_PROTOCOL="http:"
export QHANA_BACKEND_HOSTNAME="${TARGET_ContainerIP}"
export QHANA_BACKEND_PORT="${TARGET_BackendPort}"


envsubst < /var/www/html/${SOURCE_AppName}/assets/env.js.template > /var/www/html/${SOURCE_AppName}/assets/env.js


sleep 10
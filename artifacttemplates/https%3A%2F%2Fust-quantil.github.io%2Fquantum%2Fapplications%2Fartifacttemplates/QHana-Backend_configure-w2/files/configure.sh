#!/bin/sh

cat << EOF > Config.toml

# the port the server will listen on
qhana.qhana_backend.port = $BackendPort

# the domains allowed cors requests
qhana.qhana_backend.corsDomains = ["*"]

qhana.qhana_backend.internalUrlMap."(?<=^|https?://)localhost(:[0-9]+)?" = "host.docker.internal\$1"

EOF

echo "$(<Config.toml)"

mv Config.toml ./qhana_backend
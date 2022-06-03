#!/bin/sh

cat << EOF > Config.toml
[qhana.qhana_backend]

# the port the server will listen on
port = $BackendPort

# the domains allowed cors requests
corsDomains = ["http://localhost:4200", "*"]

[qhana.qhana_backend.internalUrlMap]
"(?<=^|https?://)localhost(:[0-9]+)?" = "host.docker.internal\$1"

EOF

echo "$(<Config.toml)"

mv Config.toml ./qhana_backend
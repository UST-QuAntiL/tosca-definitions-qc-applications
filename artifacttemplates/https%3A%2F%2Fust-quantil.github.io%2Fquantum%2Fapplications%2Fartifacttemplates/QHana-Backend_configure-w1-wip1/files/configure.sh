#!/bin/sh

cat << EOF > Config.toml
[qhana.qhana_backend]

# the port the server will listen on
port = $Port

# the domains allowed cors requests
corsDomains = ["http://localhost:4200", "*"]


[qhana.qhana_backend.database]


# Either "sqlite" or "mariadb"
dbType = "mariadb"


# File Path to the sqlite db
dbPath = "qhana-backend.db"


# Hostname + port for mariadb db
dbHost = "$DBHost"
# DB name for mariadb db
dbName = "$DBName"
# DB user for mariadb db
dbUser = "$DBUser"
# DB password for mariadb db
dbPassword = "$DBPassword"
EOF

echo "$(<Config.toml)"

mv Config.toml ./qhana_backend
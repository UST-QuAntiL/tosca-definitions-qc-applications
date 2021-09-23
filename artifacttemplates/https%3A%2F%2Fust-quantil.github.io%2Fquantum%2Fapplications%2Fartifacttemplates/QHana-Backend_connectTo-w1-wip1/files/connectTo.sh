#!/bin/sh

cd qhana_backend

cat << EOF >> Config.toml
[qhana.qhana_backend.database]


# Either "sqlite" or "mariadb"
dbType = "mariadb"


# File Path to the sqlite db
dbPath = "qhana-backend.db"


# Hostname + port for mariadb db
dbHost = "${TARGET_ContainerIP}:${DMBSPort}"
# DB name for mariadb db
dbName = "$DBName"
# DB user for mariadb db
dbUser = "$DBUser"
# DB password for mariadb db
dbPassword = "$DBPassword"
EOF

java -jar qhana_backend.jar
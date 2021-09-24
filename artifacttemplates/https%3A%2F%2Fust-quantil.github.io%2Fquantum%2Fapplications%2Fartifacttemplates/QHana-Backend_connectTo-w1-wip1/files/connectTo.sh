#!/bin/sh

cd qhana_backend

cat << EOF >> Config.toml
[qhana.qhana_backend.database]


# Either "sqlite" or "mariadb"
dbType = "mariadb"


# File Path to the sqlite db
dbPath = "qhana-backend.db"


# Hostname + port for mariadb db
dbHost = "${TARGET_ContainerIP}:${TARGET_DMBSPort}"
# DB name for mariadb db
dbName = "$TARGET_DBName"
# DB user for mariadb db
dbUser = "$TARGET_DBUser"
# DB password for mariadb db
dbPassword = "$TARGET_DBPassword"
EOF

java -jar qhana_backend.jar
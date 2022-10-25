#!/bin/sh

cd qhana_backend

cat << EOF >> Config.toml


# Either "sqlite" or "mariadb"
qhana.qhana_backend.database.dbType = "mariadb"


# File Path to the sqlite db
qhana.qhana_backend.database.dbPath = "qhana-backend.db"


# Hostname + port for mariadb db
qhana.qhana_backend.database.dbHost = "${TARGET_ContainerIP}:${TARGET_DBMSPort}"
# DB name for mariadb db
qhana.qhana_backend.database.dbName = "$TARGET_DBName"
# DB user for mariadb db
qhana.qhana_backend.database.dbUser = "$TARGET_DBUser"
# DB password for mariadb db
qhana.qhana_backend.database.dbPassword = "$TARGET_DBPassword"
EOF

kill $(pgrep -f 'java')

nohup java -jar qhana_backend.jar &

sleep 10
#!/bin/bash

cat << EOF > connect_db.sh
#!/bin/bash
export SQLALCHEMY_DATABASE_URI = mariadb+pymysql://${DBUser}:${DBPassword}@${TARGET_ContainerIP}:${DBMSPort}/${DBName}?charset=utf8mb4
EOF

if [ -f connect_redis.sh ]; then
    source connect_redis.sh
    source connect_db.sh
    source start_script.sh
fi
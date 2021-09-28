#!/bin/bash

cat << EOF > connect_db.sh
#!/bin/bash
export SQLALCHEMY_DATABASE_URI="mariadb+pymysql://${TARGET_DBUser}:${TARGET_DBPassword}@${TARGET_ContainerIP}:${TARGET_DBMSPort}/${TARGET_DBName}?charset=utf8mb4"
EOF

if [ -f connect_ibmq.sh ]; then
    if [ -f connect_redis.sh ]; then
        source connect_redis.sh
        source connect_db.sh
        source connect_ibmq.sh
        source start_script.sh
    fi
fi

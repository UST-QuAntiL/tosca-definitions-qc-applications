#!/bin/bash

cat << EOF > connect_redis.sh
#!/bin/bash
export BROKER_URL="redis://${TARGET_ContainerIP}:${TARGET_RedisPort}"
export RESULT_BACKEND="redis://${TARGET_ContainerIP}:${TARGET_RedisPort}"
EOF

if [ -f connect_db.sh ]; then
    source connect_redis.sh
    source connect_db.sh
    source start_script.sh
fi
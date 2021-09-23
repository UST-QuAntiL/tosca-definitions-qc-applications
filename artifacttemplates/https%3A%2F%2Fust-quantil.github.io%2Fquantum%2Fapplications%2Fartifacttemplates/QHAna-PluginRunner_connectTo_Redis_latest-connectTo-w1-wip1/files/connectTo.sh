#!/bin/bash

cat << EOF > connect_redis.sh
#!/bin/bash
export BROKER_URL = redis://${TARGET_ContainerIP}:${RedisPort}
export RESULT_BACKEND = $BROKER_URL
EOF

if [ -f connect_db.sh ]; then
    source connect_redis.sh
    source connect_db.sh
    source start_script.sh
fi
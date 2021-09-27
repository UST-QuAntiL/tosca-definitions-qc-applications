#!/bin/bash

cat << EOF > connect_ibmq.sh
#!/bin/bash
export IBMQ_BACKEND_NAME="${TARGET_IBMQ_BACKEND_NAME}"
export IBMQ_TOKEN="${TARGET_IBMQ_TOKEN}"
EOF

if [ -f connect_redis.sh ]; then
    if [ -f connect_db.sh ]; then
        source connect_redis.sh
        source connect_db.sh
        source connect_ibmq.sh
        source start_script.sh
fi
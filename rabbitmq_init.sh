#!/bin/bash

set -e

# Load libraries
. /opt/bitnami/scripts/libbitnami.sh
. /opt/bitnami/scripts/librabbitmq.sh

print_welcome_page

if [[ "$*" = "/opt/bitnami/scripts/rabbitmq/run.sh" ]]; then
    info "** Starting RabbitMQ setup **"
    /opt/bitnami/scripts/rabbitmq/setup.sh
    info "** RabbitMQ setup finished! **"
fi

# Start the change_password script in the background
# /opt/bitnami/scripts/rabbitmq/rabbitmq_change_password.sh &

echo ""
exec "$@"


#!/bin/sh

# Exit immediately if any command fails.
set -e

# Replaces environment variables (e.g., ${LISTEN_PORT}, ${APP_HOST}) in the template file.
# Writes the resulting Nginx configuration to /etc/nginx/conf.d/default.conf.

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Starts Nginx.
# daemon off; keeps Nginx running in the foreground instead of becoming a background process.
# This is commonly used in Docker containers so the container stays alive.
nginx -g 'daemon off;'
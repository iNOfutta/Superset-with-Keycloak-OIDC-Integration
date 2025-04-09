FROM apache/superset:latest

# Any future errors use tag "4.1.2", the working tag by the time it was built

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/config /app/pythonpath

# Copy configuration files
COPY config/superset_config.py /app/pythonpath/
COPY config/keycloak_security_manager.py /app/pythonpath/
COPY config/client_secret.json /app/pythonpath/client_secret.json

# Create a script to handle environment variable substitution and server startup
RUN echo '#!/bin/bash\n\
# Substitute environment variables in client_secret.json\n\
envsubst < /app/pythonpath/client_secret.json > /app/pythonpath/client_secret.json.tmp\n\
mv /app/pythonpath/client_secret.json.tmp /app/pythonpath/client_secret.json\n\
chmod 644 /app/pythonpath/client_secret.json\n\
\n\
if [ ! -f /app/.initialized ]; then\n\
    # Initialize Superset\n\
    superset db upgrade\n\
    \n\
    # Create admin user with custom username if specified\n\
    if [ -n "$ADMIN_USERNAME" ]; then\n\
        superset fab create-admin \\\n\
            --username "$ADMIN_USERNAME" \\\n\
            --firstname Superset-Admin \\\n\
            --lastname User \\\n\
            --email admin@example.com \\\n\
            --password "$ADMIN_PASSWORD"\n\
    else\n\
        superset fab create-admin \\\n\
            --username admin \\\n\
            --firstname Admin \\\n\
            --lastname User \\\n\
            --email admin@example.com \\\n\
            --password admin\n\
    fi\n\
    \n\
    superset init\n\
    touch /app/.initialized\n\
fi\n\
\n\
# Start Gunicorn with optimal settings\n\
gunicorn \
    --bind 0.0.0.0:8088 \
    --workers=4 \
    --threads=4 \
    --worker-class=gthread \
    --timeout 120 \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    "superset.app:create_app()"' > /app/docker-entrypoint.sh \
&& chmod +x /app/docker-entrypoint.sh


RUN chown -R superset:superset /app && \
    chmod 644 /app/pythonpath/client_secret.json

USER superset

ENTRYPOINT ["/app/docker-entrypoint.sh"]
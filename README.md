# Superset with Keycloak Integration

A production-ready Apache Superset setup with Keycloak authentication integration.

## Features

- 🔐 **Keycloak Integration**: OpenID Connect (OIDC) authentication
- 🚀 **Performance Optimized**: Configured with Gunicorn workers and Redis caching
- 🔄 **Role Mapping**: Automatic role synchronization between Keycloak and Superset
- 🎯 **Production Ready**: Includes health checks and proper error handling
- 📊 **Dashboard Optimization**: Native filters and cross-filtering enabled

## Prerequisites

- Docker and Docker Compose
- Keycloak server (running and configured)
- MySQL/PostgreSQL database (for Superset metadata)

## Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd superset-keycloak
```

2. Configure environment variables in `.env`:

```bash
# Database Configuration
DATABASE_URL=mysql://superset:superset@host.docker.internal:3306/superset

# Note: `host.docker.internal` is specific to Docker Desktop on Windows and macOS.
# For Linux, replace `host.docker.internal` with the IP address of your host machine (e.g., `172.17.0.1`).

# Keycloak Configuration
KEYCLOAK_BASE_URL=http://localhost:8080
KEYCLOAK_REALM=your-realm
OAUTH_CLIENT_ID=superset
OAUTH_CLIENT_SECRET=your-client-secret

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

3. Start the services:

```bash
docker-compose up -d
```

## Configuration Details

### Keycloak Setup

1. Create a new client in Keycloak:

   - Client ID: `superset`
   - Client Protocol: `openid-connect`
   - Access Type: `confidential`
   - Valid Redirect URIs:
     - `http://localhost:8088/oauth-authorized/keycloak`
     - `http://localhost:8088/login/`
     - `http://localhost:8088/authorize`

2. Configure client roles and role mappings:
   - Default roles: `Admin`, `Alpha`, `Gamma`, `Public`
   - Map Keycloak roles to Superset roles in `superset_config.py`

### Performance Configuration

The setup includes optimized settings for production:

- **Gunicorn Workers**: 4 workers with 4 threads each
- **Database Connection Pool**: Size of 10 with 1800s recycle time
- **Redis Caching**: Enabled for dashboards and results
- **Feature Flags**: Native filters and cross-filtering enabled

### Role Mapping

Role mapping is configured in `superset_config.py`:

```python
AUTH_ROLES_MAPPING = {
    'Admin': ['Admin', 'admin', 'ADMIN', 'realm-admin'],
    'Alpha': ['Alpha', 'alpha'],
    'Gamma': ['Gamma', 'gamma'],
    'Public': ['Public', 'public']
}
```

## Production Deployment

For production deployment, ensure:

1. Set secure passwords and secrets in `.env`
2. Configure HTTPS/SSL
3. Adjust Gunicorn workers based on CPU cores: (2 \* CPU cores) + 1
4. Set appropriate database connection pool size
5. Configure proper logging levels

## Troubleshooting

Common issues and solutions:

1. **Authentication Failed**:

   - Check Keycloak client configuration
   - Verify redirect URIs
   - Ensure client secret is correct

2. **Performance Issues**:

   - Adjust Gunicorn workers/threads
   - Check database connection pool settings
   - Monitor Redis cache usage

3. **Role Mapping Issues**:
   - Verify role names in Keycloak
   - Check AUTH_ROLES_MAPPING configuration
   - Ensure user has appropriate roles assigned

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the Apache License 2.0.

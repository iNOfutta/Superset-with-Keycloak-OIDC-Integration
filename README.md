# Superset with Keycloak Integration

A production-ready deployment of Apache Superset with Keycloak OpenID Connect (OIDC) integration using Flask-OIDC, Redis caching, and PostgreSQL database.

## Features

- 🔐 Secure authentication via Keycloak OIDC using Flask-OIDC
- 🚀 High-performance setup with Redis caching
- 📊 PostgreSQL database for metadata storage
- 🔄 Automatic user role synchronization
- 🛡️ Production-ready security configurations
- 📝 Comprehensive logging and monitoring
- 🔧 Flexible configuration via environment variables

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database (local or remote)
- Keycloak server with OIDC client configured
- SSL certificates (for production)
- Python 3.7+ (for Flask-OIDC compatibility)

## Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd superset-keycloak
```

2. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:

```bash
docker-compose up -d
```

4. Access Superset:

- Development: http://localhost:8088
- Production: https://your-domain

## Configuration

### Environment Variables

The application is configured through environment variables in `.env`. Key configurations include:

#### Database Configuration

```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Superset Configuration

```bash
SECRET_KEY=your-secret-key
FLASK_ENV=development
SUPERSET_WEBSERVER_PORT=8088
```

#### Redis Configuration

```bash
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

#### Keycloak OIDC Configuration (Flask-OIDC)

```bash
KEYCLOAK_BASE_URL=https://your-keycloak-server
KEYCLOAK_REALM=your-realm
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
OIDC_REDIRECT_URI=http://localhost:8088/authorize
```

#### Admin User Configuration

```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

### Keycloak Setup

1. Create a new client in Keycloak:

   - Client ID: superset
   - Protocol: openid-connect
   - Access Type: confidential
   - Valid Redirect URIs: http://localhost:8088/\*
   - Web Origins: \*

2. Configure client roles:

   - Create roles: Admin, Alpha, Gamma
   - Map roles to users

3. **Critical Role Configuration**:

   - Navigate to Realm Settings → Client Scopes
   - For both realm roles and client roles:
     - Select the appropriate scope (e.g., `roles` or client-specific scope)
     - Under the Mappers tab, ensure the role mapper has "Add to userinfo" enabled
     - This configuration is essential for proper role propagation to Superset
     - Without this setting, the `keycloak_security_manager.py` will default to assigning the Gamma role regardless of the user's actual Keycloak roles

4. **Role Mapping Verification**:
   - Test the configuration by checking the userinfo endpoint
   - Verify that roles appear in the JWT token and userinfo response
   - Use the following curl command to test:
     ```bash
     curl -X GET "${KEYCLOAK_BASE_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/userinfo" \
          -H "Authorization: Bearer ${ACCESS_TOKEN}"
     ```
   - The response should include the user's roles in the `roles` claim

### Flask-OIDC Configuration

The integration uses Flask-OIDC for handling OIDC authentication. Key configurations include:

1. **Client Configuration**:

   - Client ID and Secret from Keycloak
   - Redirect URI for authentication flow
   - Token endpoint configuration

2. **Security Manager**:

   - Custom OIDC security manager implementation
   - Role mapping configuration
   - User information handling

3. **Session Management**:
   - Token storage and refresh
   - Session timeout settings
   - Secure cookie configuration

### Security Settings

- Session security
- CORS configuration
- Rate limiting
- Proxy headers

## Architecture

The deployment consists of three main services:

1. **Superset Application**

   - Apache Superset with Flask-OIDC security manager
   - Gunicorn server with optimized settings
   - Environment-aware configuration

2. **Redis Service**

   - Caching layer
   - Rate limiting
   - Session storage
   - Health monitoring

3. **Nginx (Production)**
   - SSL termination
   - Reverse proxy
   - Static file serving
   - Security headers

## Development vs Production

### Development Mode

- HTTP access
- Debug logging
- Local database
- No SSL
- Flask-OIDC debug mode enabled

### Production Mode

- HTTPS only
- Optimized logging
- Remote database
- SSL certificates
- Nginx reverse proxy
- Flask-OIDC production settings

## Monitoring and Logging

- Application logs
- Access logs
- Error tracking
- Health checks
- Flask-OIDC debug logs (in development)

## Troubleshooting

### Common Issues

1. **Database Connection**

   - Check database URL
   - Verify network access
   - Test credentials

2. **Keycloak OIDC Integration**

   - Validate OIDC configuration
   - Check redirect URIs
   - Verify client secret
   - Enable Flask-OIDC debug logging
   - Check token validation
   - Verify role mapping
   - **Important**: Check Keycloak URL realm construction
     - Different Keycloak versions may construct realm URLs differently
     - Some versions use: `${KEYCLOAK_BASE_URL}/realms/${KEYCLOAK_REALM}`
     - Others use: `${KEYCLOAK_BASE_URL}/auth/realms/${KEYCLOAK_REALM}`
     - Ensure your `client_secret.json` matches your Keycloak version's URL structure
     - This mismatch can cause authentication failures

3. **Redis Connection**
   - Test Redis connectivity
   - Check password
   - Verify port mapping

### Log Files

- Application logs: `docker-compose logs superset`
- Redis logs: `docker-compose logs redis`
- Nginx logs: `docker-compose logs nginx`
- Flask-OIDC debug logs (development only)

## Important Notes

### Admin User Configuration

The admin user specified in the `.env` file (`ADMIN_USERNAME` and `ADMIN_PASSWORD`) **must be different** from the admin user configured in Keycloak. If the admin credentials in the `.env` file match the Keycloak admin credentials, the admin user will **not be created** in the Superset database, and you will not be able to log in to Superset.

Ensure that:

- `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env` are unique and do not overlap with Keycloak credentials.
- Example:
  ```properties
  ADMIN_USERNAME=superset-admin
  ADMIN_PASSWORD=securepassword123
  ```

---

### Reverse Proxy Configuration

When deploying Superset behind a reverse proxy (e.g., Nginx), you must configure the proxy to handle requests properly. Below is an example configuration for Nginx:

#### Nginx Configuration (`analytics.conf`)

```nginx
server {
    listen 80;
    server_name analytics.yourdomain.com;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Buffer settings to avoid upstream errors
        proxy_buffer_size   128k;
        proxy_buffers     4 256k;
        proxy_busy_buffers_size 256k;

        proxy_pass http://localhost:8088/;
    }
}
```

#### Why the Buffer Section is Important

The buffer settings are critical to avoid errors like:

```
[error] upstream sent too big header while reading response header from upstream
```

This error typically occurs when the response headers from Superset exceed the default buffer size. The above configuration increases the buffer size to handle larger headers.

---

### Debugging Reverse Proxy Issues

If you encounter issues with the reverse proxy, such as failed requests or login errors, check the Nginx error logs for more details. Use the following command to filter logs related to your domain:

```bash
sudo cat /var/log/nginx/error.log | grep "analytics*"
```

---

### Debugging Login Flow Issues

If you experience issues specific to the login flow (e.g., OIDC errors or Keycloak integration problems), consider the following steps:

1. **Enable Development Mode**:

   - Temporarily set `FLASK_ENV=development` in your `.env` file to enable debug mode in Flask.
   - Restart the Superset container to apply the changes.

2. **Add Debug Logs in `keycloak_security_manager.py`**:

   - Locate the `keycloak_security_manager.py` file in your project.
   - Add logging statements to capture more details about the login flow. For example:

     ```python
     import logging
     logger = logging.getLogger(__name__)

     def some_function():
         logger.debug("Debugging Keycloak login flow...")
     ```

3. **Check Superset Logs**:

   - Use the following command to view Superset logs:
     ```bash
     docker-compose logs superset
     ```

4. **Check Keycloak Logs**:
   - If the issue persists, check the Keycloak server logs for errors related to the OIDC flow.

## Maintenance

### Backup

- Database backup
- Redis persistence
- Configuration backup

### Updates

- Image updates
- Configuration changes
- Security patches
- Flask-OIDC updates

## Security Considerations

1. **Environment Variables**

   - Use strong secrets
   - Rotate credentials
   - Secure storage

2. **Network Security**

   - Firewall rules
   - SSL/TLS
   - Access control

3. **Application Security**
   - Session management
   - Rate limiting
   - Input validation
   - Flask-OIDC security settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

## Support

For support, please:

- Check the documentation
- Open an issue
- Contact the maintainers

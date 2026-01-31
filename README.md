# KSHRD Certificate Verify Service

A FastAPI-based REST API service for verifying and managing KSHRD (Korea Software HRD) certificates. This service provides secure certificate verification capabilities with Keycloak authentication integration.

## Features

- 🔐 **Keycloak Authentication**: JWT-based authentication using Keycloak for secure access
- 📜 **Certificate Management**: Manage and verify KSHRD certificates
- 👥 **User Management**: User roles and permissions (ADMIN, STAFF, GRADUATE)
- 🗄️ **PostgreSQL Database**: Async database operations using SQLAlchemy and asyncpg
- ⚡ **Async/Await**: Fully asynchronous API for high performance
- 🏥 **Health Checks**: Built-in health check endpoints for monitoring
- 🔧 **Environment-based Configuration**: Secure configuration management via environment variables

## Tech Stack

- **Framework**: FastAPI 0.128.x
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0+ (async)
- **Authentication**: Keycloak (JWT verification)
- **Configuration**: Pydantic Settings
- **Server**: Uvicorn
- **Python**: 3.13+

## Project Structure

```
app/
├── core/
│   └── config.py          # Application configuration and settings
├── db/
│   └── database.py        # Database connection and session management
├── models/
│   ├── user.py            # User model
│   └── certificate.py     # Certificate model
└── main.py                # FastAPI application entry point
```

## Installation

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)
- PostgreSQL database
- Keycloak instance (for authentication)

### Setup Steps

1. **Clone the repository** (if applicable)
   ```bash
   git clone <repository-url>
   cd "Certificate Service API"
   ```

2. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

3. **Create a `.env` file** in the project root with the following variables:
   ```env
   # Database Configuration
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database_name

   # Keycloak Configuration
   KEYCLOAK_URL=https://keycloak.kshrd.app
   KEYCLOAK_REALM=your_realm
   KEYCLOAK_CLIENT_ID=your_client_id
   KEYCLOAK_CLIENT_SECRET=your_client_secret  # Optional, for confidential clients

   # Optional: Debug Mode
   DEBUG=True
   ```

4. **Set up the database**
   - Ensure PostgreSQL is running
   - Create the database specified in `DB_NAME`
   - Run migrations (if applicable) to create tables

## Running the Application

### Development Mode

Start the development server with auto-reload:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Production Mode

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Checks

- `GET /` - Welcome message
- `GET /health` - Application health status
- `GET /db_health_checl` - Database connection health check

### Interactive API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Configuration

The application uses Pydantic Settings to manage configuration. All settings are loaded from:

1. Environment variables
2. `.env` file in the project root

### Key Configuration Options

- **Database**: Configured via `DATABASE_URL` (auto-generated from individual DB variables)
- **Keycloak**: JWKS URL is auto-generated from `KEYCLOAK_URL` and `KEYCLOAK_REALM`
- **Debug Mode**: Enable SQL query logging by setting `DEBUG=True`

## Database Models

### User Model
- UUID-based primary key (matches Keycloak `sub` field)
- Username (unique)
- Role (ADMIN, STAFF, GRADUATE)
- Active status
- Timestamps (created_at, updated_at)
- Relationship with certificates

### Certificate Model
- (To be defined)

## Authentication

The service integrates with Keycloak for authentication:

- JWT tokens are verified using public keys from Keycloak's JWKS endpoint
- User IDs match Keycloak's `sub` field
- Supports both public and confidential client configurations

## Development

### Adding Dependencies

```bash
poetry add <package-name>
```

### Running Tests

(Add test commands when tests are implemented)

## License

(Add license information)

## Author

DoeunKongden - doeunkongden1@gmail.com

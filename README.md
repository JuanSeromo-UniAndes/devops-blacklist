# Blacklist API

A Flask REST API for managing email blacklists with JWT authentication.

## Features

- Add emails to blacklist with reasons
- Check if an email is blacklisted
- JWT-based authentication
- PostgreSQL database support

## Setup

### Prerequisites

- Python 3.14+
- PostgreSQL database

### Installation

```bash
# Install dependencies
poetry install

# Set environment variables (optional)
export DATABASE_URL="postgresql://user:password@localhost:5432/blacklist_db"
export JWT_SECRET_KEY="your-jwt-secret"
export SECRET_KEY="your-secret-key"

# Run the application
poetry run python main.py
```

## API Endpoints

### Health Check
```
GET /blacklist/ping
```
Returns: `pong`

### Add to Blacklist
```
POST /blacklist
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "email": "user@example.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Spam activity"
}
```

### Check Email
```
GET /blacklist/<email>
Authorization: Bearer <JWT_TOKEN>
```

Returns:
- `{"existing": true, "blocked_reason": "..."}` if blacklisted
- `{"existing": false}` if not blacklisted

## Database

The application uses PostgreSQL and automatically creates the required tables on startup.

Default connection: `postgresql://postgres:mysecretpassword@localhost:5432/blacklist_db`

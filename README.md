# Blacklist API

A Flask REST API for managing email blacklists with JWT authentication.

## Features

- Add emails to blacklist with reasons
- Check if an email is blacklisted
- JWT-based authentication
- SQLite/PostgreSQL database support
- IP address tracking
- Timestamp logging
- Email format validation
- UUID validation
- Duplicate email protection

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API (uses SQLite by default)
python app.py
```

The API will be available at `http://localhost:5000`

### Generate JWT Token

```bash
python gen_token.py
```

### Run Tests

```bash
python test_simple.py
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

**Response:**
- `201`: Email added successfully
- `400`: Invalid data or email already exists
- `401`: Missing/invalid token

### Check Email
```
GET /blacklist/<email>
Authorization: Bearer <JWT_TOKEN>
```

**Returns:**
- `{"existing": true, "blocked_reason": "..."}` if blacklisted
- `{"existing": false}` if not blacklisted

## Database Schema

- `id`: Primary key
- `email`: Email address (required, unique)
- `app_uuid`: Application UUID (required)
- `blocked_reason`: Reason for blocking (optional)
- `ip_address`: Client IP address (auto-captured)
- `created_at`: Timestamp (auto-generated)

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)
- `JWT_SECRET_KEY`: JWT signing key (default: 'super-secret')
- `SECRET_KEY`: Flask secret key (default: 'your-secret-key')

### For PostgreSQL

```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/blacklist_db"
export JWT_SECRET_KEY="your-jwt-secret"
export SECRET_KEY="your-flask-secret"
python app.py
```

## Testing

### Automated Tests

```bash
# Run all tests
python test_simple.py
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:5000/blacklist/ping

# Generate token
TOKEN=$(python gen_token.py | grep "Token:" | cut -d' ' -f2)

# Add email to blacklist
curl -X POST http://localhost:5000/blacklist \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","app_uuid":"550e8400-e29b-41d4-a716-446655440000","blocked_reason":"Test"}'

# Check email
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/blacklist/test@example.com
```

## Postman Collection

Import `Blacklist_API.postman_collection.json` for ready-to-use API tests.

## AWS Deployment

### Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create blacklist-env`
4. Deploy: `eb deploy`

### Environment Variables for Production

Set in EB Console:
- `DATABASE_URL`: Your RDS PostgreSQL connection string
- `JWT_SECRET_KEY`: Strong secret key
- `SECRET_KEY`: Strong Flask secret

## Validation Rules

- **Email**: Must be valid email format
- **app_uuid**: Must be valid UUID format
- **blocked_reason**: Optional string
- **Authentication**: JWT token required for all endpoints except health check

## Error Responses

- `400`: Bad request (invalid data, duplicate email)
- `401`: Unauthorized (missing/invalid token)
- `422`: Unprocessable entity (invalid JWT)
- `500`: Internal server error

## Files Structure

- `app.py`: Main application file
- `gen_token.py`: JWT token generator
- `test_simple.py`: Automated tests
- `requirements.txt`: Python dependencies
- `config.py`: Configuration (legacy)
- `.ebextensions/`: AWS Beanstalk configuration

## Test Results

✅ All functionality tested and working:
- Health check endpoint
- JWT authentication
- Add emails to blacklist
- Check emails in blacklist
- Duplicate email validation
- Endpoint protection
- Error handling
- Database operations
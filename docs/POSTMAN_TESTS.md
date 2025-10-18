# Postman Collection for Blacklist API

## Environment Variables
- `base_url`: Your AWS Beanstalk URL (e.g., http://blacklist-env.eba-xyz.us-east-1.elasticbeanstalk.com)
- `jwt_token`: Generated JWT token

## Test Cases

### 1. Health Check
```
GET {{base_url}}/blacklist/ping
```

### 2. Generate JWT Token
Run the generate_token.py script locally to get a token.

### 3. Add Email to Blacklist
```
POST {{base_url}}/blacklist
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "email": "test@example.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Spam activity"
}
```

### 4. Check Blacklisted Email
```
GET {{base_url}}/blacklist/test@example.com
Authorization: Bearer {{jwt_token}}
```

### 5. Check Non-Blacklisted Email
```
GET {{base_url}}/blacklist/clean@example.com
Authorization: Bearer {{jwt_token}}
```

## Expected Responses

### Health Check: 200 OK
```
pong
```

### Add Email: 201 Created
```json
{
  "message": "Email successfully added to blacklist"
}
```

### Check Blacklisted: 200 OK
```json
{
  "existing": true,
  "blocked_reason": "Spam activity"
}
```

### Check Clean: 200 OK
```json
{
  "existing": false
}
```
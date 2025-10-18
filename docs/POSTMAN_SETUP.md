# Postman Setup Guide

## Import Collection

1. Open Postman
2. Click "Import" button
3. Select `Blacklist_API.postman_collection.json`
4. Collection will be imported with all test cases

## Setup Variables

### Method 1: Environment Variables
1. Create new environment called "Blacklist Local"
2. Add variables:
   - `base_url`: `http://localhost:5000`
   - `jwt_token`: `YOUR_TOKEN_HERE`

### Method 2: Collection Variables
1. Right-click on "Blacklist API" collection
2. Select "Edit"
3. Go to "Variables" tab
4. Update:
   - `base_url`: `http://localhost:5000`
   - `jwt_token`: Generate using `python gen_token.py`

## Generate JWT Token

```bash
python gen_token.py
```

Copy the token and paste it in the `jwt_token` variable.

## Test Sequence

Run requests in this order for best results:

1. **Health Check** - Verify API is running
2. **Add Email to Blacklist** - Add first email
3. **Check Email in Blacklist** - Verify it was added
4. **Add Another Email** - Add second email
5. **Add Duplicate Email** - Should fail with 400
6. **Add Email with Invalid Format** - Should fail with 400
7. **Add Email with Invalid UUID** - Should fail with 400
8. **Check Non-Existing Email** - Should return false
9. **Unauthorized Access** - Should fail with 401
10. **Invalid Token** - Should fail with 422

## Expected Results

- ✅ Health Check: 200 "pong"
- ✅ Add Email: 201 "Email successfully added"
- ✅ Check Email: 200 {"existing": true, "blocked_reason": "..."}
- ✅ Duplicate Email: 400 "Email already exists"
- ✅ Invalid Format: 400 "Invalid email format"
- ✅ Invalid UUID: 400 "Invalid UUID format"
- ✅ Non-existing: 200 {"existing": false}
- ✅ No Token: 401 "Missing Authorization Header"
- ✅ Invalid Token: 422 JWT decode error

## Tips

- Generate a new token if you get 422 errors (token expired)
- Make sure the API is running on localhost:5000
- Check console logs for detailed error messages
# User Service

This is the User Service for the E-commerce Order Processing System. It provides the following features:

- User Registration
- Get User Details by ID

## Endpoints

### `POST /register`
Register a new user.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

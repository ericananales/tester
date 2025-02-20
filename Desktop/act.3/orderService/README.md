# Order Service

This is the Order Service for the E-commerce Order Processing System. It provides the following features:

- Create Orders for Users
- Retrieve Orders for a User by ID

## Endpoints

### `POST /user/<user_id>/order`
Create a new order for a specific user.

**Request Body:**
```json
{
  "product_name": "Laptop",
  "quantity": 1,
  "price": 999.99
}

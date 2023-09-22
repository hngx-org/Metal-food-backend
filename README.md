## Endpoints

- Get withdrawal list `api/withdrawal/get`
- Get specific withdrwal `api/withdrawal/get/<int:pk>`

## Sample Requests and Responses

### 1. Get withdrawal list

**Request:**

```http
GET /api/withdrawal/get
Content-Type: application/json

```

**Response (Success):**

```json  
   {
    "id": 1,
    "user_id": 2345,
    "status": Success,
    "amount": 200.99,
    "created_at": 2023-09-10T15:45:30.123456
    },
   {
    "id": 2,
    "user_id": 2345,
    "status": Success,
    "amount": 400.99,
    "created_at": 2023-09-15T15:45:30.123456
    },
   {
    "id": 3,
    "user_id": 2345,
    "status": Success,
    "amount": 600.99,
    "created_at": 2023-09-19T15:45:30.123456
    },

```
### 1. Get specific withdrawal list

**Request:**

```http
GET api/withdrawal/get/1/
Content-Type: application/json

```

**Response (Success):**

```json  
   {
    "id": 1,
    "user_id": 2345,
    "status": Success,
    "amount": 200.99,
    "created_at": 2023-09-10T15:45:30.123456
    },

```

# Ecommerce API

A FastAPI-based ecommerce application with MongoDB integration.

## Overview

This application provides RESTful APIs for managing products and orders in an ecommerce system. It includes product creation, listing with filtering, order management, and user order retrieval.

## Features

- Product management (create, list with filters)
- Order management (create, retrieve by user)
- MongoDB integration with optimized queries
- Input validation using Pydantic
- Comprehensive error handling
- Pagination support

## Tech Stack

- Python 3.10+
- FastAPI
- MongoDB (Pymongo)
- Pydantic
- Uvicorn

## Setup

### Prerequisites
- Python 3.10 or higher
- MongoDB instance (local or Atlas)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Intern-Backend
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment
```bash
cp env.example .env
```

Edit `.env` with your MongoDB connection string:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db?retryWrites=true&w=majority
```

4. Run the application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Products

#### Create Product
- **POST** `/products`
- **Status**: 201 Created
- **Request**:
```json
{
    "name": "Product Name",
    "description": "Product description",
    "price": 99.99,
    "category": "Electronics",
    "size": "large",
    "color": "Black",
    "brand": "Brand Name",
    "stock": 50
}
```

#### List Products
- **GET** `/products`
- **Status**: 200 OK
- **Query Parameters**:
  - `name` (optional): Filter by name (supports regex)
  - `size` (optional): Filter by size
  - `limit` (optional): Number of results (default: 10)
  - `offset` (optional): Skip results (default: 0)

### Orders

#### Create Order
- **POST** `/orders`
- **Status**: 201 Created
- **Request**:
```json
{
    "user_id": "user123",
    "items": [
        {
            "product_id": "product_id_here",
            "quantity": 2,
            "price": 99.99
        }
    ],
    "shipping_address": "123 Main St, City, State 12345",
    "payment_method": "credit_card"
}
```

#### Get User Orders
- **GET** `/orders/{user_id}`
- **Status**: 200 OK
- **Query Parameters**:
  - `limit` (optional): Number of results (default: 10)
  - `offset` (optional): Skip results (default: 0)

## Database Schema

### Products Collection
```json
{
    "_id": "ObjectId",
    "name": "string",
    "description": "string",
    "price": "float",
    "category": "string",
    "size": "string",
    "color": "string",
    "brand": "string",
    "stock": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Orders Collection
```json
{
    "_id": "ObjectId",
    "user_id": "string",
    "items": [
        {
            "product_id": "string",
            "quantity": "integer",
            "price": "float"
        }
    ],
    "total_amount": "float",
    "shipping_address": "string",
    "payment_method": "string",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

## Development

For development with auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Deployment

### Render
1. Connect your GitHub repository
2. Set environment variables (MONGODB_URI)
3. Deploy using the provided `render.yaml`

### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy using the provided `Procfile`

## Project Structure

```
├── main.py              # FastAPI application
├── requirements.txt      # Dependencies
├── test_api.py          # Test script
├── start.py             # Development helper
├── env.example          # Environment template
├── render.yaml          # Render deployment config
├── Procfile             # Railway deployment config
└── README.md           # Documentation
``` 
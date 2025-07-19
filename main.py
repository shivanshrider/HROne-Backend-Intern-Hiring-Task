from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from typing import Optional, List
from pydantic import BaseModel, Field
import re

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Ecommerce API",
    description="A FastAPI ecommerce application with MongoDB",
    version="1.0.0"
)

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client.ecommerce_db

# Pydantic models
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    category: str = Field(..., description="Product category")
    size: str = Field(..., description="Product size")
    color: str = Field(..., description="Product color")
    brand: str = Field(..., description="Product brand")
    stock: int = Field(..., description="Available stock")

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    size: str
    color: str
    brand: str
    stock: int
    created_at: datetime
    updated_at: datetime

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Product ID")
    quantity: int = Field(..., description="Quantity ordered")
    price: float = Field(..., description="Price per unit")

class OrderCreate(BaseModel):
    user_id: str = Field(..., description="User ID")
    items: List[OrderItem] = Field(..., description="Order items")
    shipping_address: str = Field(..., description="Shipping address")
    payment_method: str = Field(..., description="Payment method")

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    shipping_address: str
    payment_method: str
    status: str
    created_at: datetime
    updated_at: datetime

# Helper functions
def calculate_total_amount(items: List[OrderItem]) -> float:
    return sum(item.price * item.quantity for item in items)

def validate_product_exists(product_id: str) -> bool:
    return db.products.find_one({"_id": ObjectId(product_id)}) is not None

# API Endpoints

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        product_data = product.model_dump()
        product_data["created_at"] = datetime.now(timezone.utc)
        product_data["updated_at"] = datetime.now(timezone.utc)
        
        result = db.products.insert_one(product_data)
        
        # Get the created product
        created_product = db.products.find_one({"_id": result.inserted_id})
        created_product["id"] = str(created_product["_id"])
        del created_product["_id"]
        
        return ProductResponse(**created_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@app.get("/products", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None, description="Product name filter (supports regex)"),
    size: Optional[str] = Query(None, description="Product size filter"),
    limit: Optional[int] = Query(10, description="Number of documents to return"),
    offset: Optional[int] = Query(0, description="Number of documents to skip")
):
    """List products with optional filtering and pagination"""
    try:
        # Build filter query
        filter_query = {}
        
        if name:
            # Support regex/partial search
            filter_query["name"] = {"$regex": name, "$options": "i"}
        
        if size:
            filter_query["size"] = size
        
        # Get total count for pagination
        total_count = db.products.count_documents(filter_query)
        
        # Get products with pagination
        products = list(db.products.find(filter_query).skip(offset).limit(limit).sort("_id", -1))
        
        # Format response
        formatted_products = []
        for product in products:
            product["id"] = str(product["_id"])
            del product["_id"]
            formatted_products.append(ProductResponse(**product))
        
        return formatted_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        # Validate all products exist
        for item in order.items:
            if not validate_product_exists(item.product_id):
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        
        # Calculate total amount
        total_amount = calculate_total_amount(order.items)
        
        order_data = order.model_dump()
        order_data["total_amount"] = total_amount
        order_data["status"] = "pending"
        order_data["created_at"] = datetime.now(timezone.utc)
        order_data["updated_at"] = datetime.now(timezone.utc)
        
        result = db.orders.insert_one(order_data)
        
        # Get the created order
        created_order = db.orders.find_one({"_id": result.inserted_id})
        created_order["id"] = str(created_order["_id"])
        del created_order["_id"]
        
        return OrderResponse(**created_order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@app.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str,
    limit: Optional[int] = Query(10, description="Number of documents to return"),
    offset: Optional[int] = Query(0, description="Number of documents to skip")
):
    """Get orders for a specific user with pagination"""
    try:
        # Get total count for pagination
        total_count = db.orders.count_documents({"user_id": user_id})
        
        # Get orders with pagination
        orders = list(db.orders.find({"user_id": user_id}).skip(offset).limit(limit).sort("_id", -1))
        
        # Format response
        formatted_orders = []
        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]
            formatted_orders.append(OrderResponse(**order))
        
        return formatted_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ecommerce API",
        "version": "1.0.0",
        "endpoints": {
            "create_product": "POST /products",
            "list_products": "GET /products",
            "create_order": "POST /orders",
            "get_user_orders": "GET /orders/{user_id}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
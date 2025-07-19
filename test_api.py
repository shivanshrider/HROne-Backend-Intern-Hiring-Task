#!/usr/bin/env python3
"""
Test script for the Ecommerce API
Run this script to test all endpoints and verify they work correctly
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployed URL

def test_create_product():
    """Test creating a product"""
    print("Testing Create Product API...")
    
    product_data = {
        "name": "Test Product",
        "description": "A test product for API testing",
        "price": 99.99,
        "category": "Electronics",
        "size": "large",
        "color": "Black",
        "brand": "TestBrand",
        "stock": 10
    }
    
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    
    if response.status_code == 201:
        print("SUCCESS: Create Product API")
        product = response.json()
        print(f"  Product ID: {product['id']}")
        return product['id']
    else:
        print(f"FAILED: Create Product API")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def test_list_products():
    """Test listing products with filters"""
    print("\nTesting List Products API...")
    
    # Test without filters
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        print("SUCCESS: List Products API (no filters)")
        products = response.json()
        print(f"  Found {len(products)} products")
    else:
        print(f"FAILED: List Products API")
        print(f"  Status Code: {response.status_code}")
        return
    
    # Test with size filter
    response = requests.get(f"{BASE_URL}/products?size=large")
    if response.status_code == 200:
        print("SUCCESS: List Products API (size filter)")
        products = response.json()
        print(f"  Found {len(products)} large products")
    else:
        print(f"FAILED: List Products API (size filter)")
    
    # Test with name filter
    response = requests.get(f"{BASE_URL}/products?name=Test")
    if response.status_code == 200:
        print("SUCCESS: List Products API (name filter)")
        products = response.json()
        print(f"  Found {len(products)} products with 'Test' in name")
    else:
        print(f"FAILED: List Products API (name filter)")

def test_create_order(product_id):
    """Test creating an order"""
    print(f"\nTesting Create Order API...")
    
    order_data = {
        "user_id": "user123",
        "items": [
            {
                "product_id": product_id,
                "quantity": 2,
                "price": 999.99
            }
        ],
        "shipping_address": "123 Main St, City, State 12345",
        "payment_method": "credit_card"
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    
    if response.status_code == 201:
        print("SUCCESS: Create Order API")
        order = response.json()
        print(f"  Order ID: {order['id']}")
        print(f"  Total Amount: ${order['total_amount']}")
        return order['id']
    else:
        print(f"FAILED: Create Order API")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def test_get_user_orders():
    """Test getting user orders"""
    print(f"\nTesting Get User Orders API...")
    
    user_id = "user123"
    response = requests.get(f"{BASE_URL}/orders/{user_id}")
    
    if response.status_code == 200:
        print("SUCCESS: Get User Orders API")
        orders = response.json()
        print(f"  Found {len(orders)} orders for user {user_id}")
        
        for order in orders:
            print(f"  Order ID: {order['id']}, Total: ${order['total_amount']}")
    else:
        print(f"FAILED: Get User Orders API")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")

def test_root_endpoint():
    """Test the root endpoint"""
    print(f"\nTesting Root Endpoint...")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("SUCCESS: Root Endpoint")
        data = response.json()
        print(f"  Message: {data['message']}")
        print(f"  Version: {data['version']}")
    else:
        print(f"FAILED: Root Endpoint")
        print(f"  Status Code: {response.status_code}")

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print(f"Base URL: {BASE_URL}")
    print("=" * 50)
    
    # Test root endpoint
    test_root_endpoint()
    
    # Test product creation
    product_id = test_create_product()
    
    if product_id:
        # Test product listing
        test_list_products()
        
        # Test order creation
        order_id = test_create_order(product_id)
        
        if order_id:
            # Test getting user orders
            test_get_user_orders()
    
    print("\n" + "=" * 50)
    print("API Tests Completed!")
    print("\nTo test manually, you can:")
    print(f"1. Visit {BASE_URL}/docs for interactive API documentation")
    print(f"2. Use curl commands as shown in the README")
    print(f"3. Use Postman or any API testing tool")

if __name__ == "__main__":
    main() 
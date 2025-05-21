import requests
import sys
import os
from pprint import pprint

def test_cors_preflight():
    """Test CORS preflight request to register endpoint"""
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Set headers for preflight request
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type,Authorization"
    }
    
    print(f"\n\n{'='*80}")
    print("Testing OPTIONS preflight request")
    print(f"{'='*80}")
    print(f"URL: {url}")
    print(f"Headers:")
    pprint(headers)
    
    try:
        # Send OPTIONS request
        response = requests.options(url, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        pprint(dict(response.headers))
        
        # Check for CORS headers
        cors_headers = {k: v for k, v in response.headers.items() if "access-control" in k.lower()}
        if cors_headers:
            print(f"\nCORS Headers Present:")
            pprint(cors_headers)
        else:
            print(f"\nWARNING: No CORS headers in response!")
            
    except Exception as e:
        print(f"Error: {e}")
        
def test_register_post():
    """Test POST request to register endpoint"""
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Sample user data
    data = {
        "email": "test@example.com",
        "password": "Password123!",
        "full_name": "Test User"
    }
    
    # Set headers for POST request
    headers = {
        "Origin": "http://localhost:3000",
        "Content-Type": "application/json"
    }
    
    print(f"\n\n{'='*80}")
    print("Testing POST request")
    print(f"{'='*80}")
    print(f"URL: {url}")
    print(f"Headers:")
    pprint(headers)
    print(f"Data:")
    pprint(data)
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, json=data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        pprint(dict(response.headers))
        
        # Try to print response body
        try:
            print(f"\nResponse Body:")
            pprint(response.json())
        except:
            print(f"\nResponse Text:")
            print(response.text[:500])  # Print at most 500 chars
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("CORS Testing Script")
    print("This script tests CORS behavior of the /api/v1/auth/register endpoint")
    
    test_cors_preflight()
    test_register_post()

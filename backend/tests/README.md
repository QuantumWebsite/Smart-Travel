# API Testing Guide

This folder contains tests for the Smart Travel API endpoints. These tests are designed to verify that all API endpoints are working correctly.

## Setup

Before running the tests, make sure you have all dependencies installed:

```bash
pip install pytest pytest-cov httpx
```

## Running the Tests

To run all tests:

```bash
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_auth.py
```

To run tests with coverage report:

```bash
pytest --cov=app tests/
```

## Test Organization

The tests are organized as follows:

- `test_auth.py`: Tests for authentication endpoints (login, register)
- `test_users.py`: Tests for user endpoints (profile, update, admin operations)
- `test_search.py`: Tests for search functionality
- `test_recommendations.py`: Tests for recommendation endpoints
- `test_deals.py`: Tests for deals endpoints
- `test_health.py`: Basic health checks for the API

## Manual Testing with Postman/Curl

If you prefer manual testing, you can use tools like Postman or curl. Here are some example commands:

### Authentication

**Register a new user:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "testpassword123", "full_name": "Test User"}'
```

**Login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/access-token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=testpassword123"
```

### User Operations

**Get current user profile:**

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Update user profile:**

```bash
curl -X PATCH "http://localhost:8000/api/v1/users/me" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"full_name": "Updated Name"}'
```

### Search Operations

**Create a new search:**

```bash
curl -X POST "http://localhost:8000/api/v1/search/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"origin": "NYC", "destination": "LON", "departure_date": "2025-06-01", "return_date": "2025-06-10", "adults": 1, "children": 0, "cabin_class": "economy"}'
```

**Get search history:**

```bash
curl -X GET "http://localhost:8000/api/v1/search/history" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Recommendations

**Get recommendations:**

```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Deals

**Get all deals:**

```bash
curl -X GET "http://localhost:8000/api/v1/deals/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Save a deal:**

```bash
curl -X POST "http://localhost:8000/api/v1/deals/1/save" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Notes

- These tests assume a working database connection. If you're testing with a live database, make sure to use a separate testing database.
- Some tests may fail if certain data doesn't exist in the database. Adjust the tests as needed to match your database state.
- For CI/CD integration, you might want to create a separate configuration that uses an in-memory database.

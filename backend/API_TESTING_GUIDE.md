# Smart Travel API Testing Guide

This guide provides comprehensive instructions for testing your Smart Travel API endpoints and CRUD operations. Use this document as a reference when verifying that your API is functioning correctly.

## Table of Contents

1. [Setting Up the Testing Environment](#setting-up-the-testing-environment)
2. [Running Automated Tests](#running-automated-tests)
3. [Testing with Swagger UI](#testing-with-swagger-ui)
4. [Manual API Testing](#manual-api-testing)
5. [CRUD Validation](#crud-validation)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)

## Setting Up the Testing Environment

Before running tests, make sure you have all the necessary dependencies installed:

```powershell
# Install required Python packages
pip install pytest pytest-cov httpx
```

### Using the Test Runner

We've created a PowerShell script that makes it easy to run tests:

```powershell
# Run the test menu
.\run_api_tests.ps1
```

## Running Automated Tests

### Run All Tests

```powershell
# Using pytest directly
pytest -v

# Using the run_tests.py script
python run_tests.py --all --verbose
```

### Run Specific Test Module

```powershell
# Test authentication endpoints
python run_tests.py --endpoint auth --verbose

# Test user endpoints
python run_tests.py --endpoint users --verbose

# Test search functionality
python run_tests.py --endpoint search --verbose
```

### Generate Coverage Report

```powershell
# Generate console coverage report
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
```

## Testing with Swagger UI

The FastAPI application comes with built-in Swagger UI documentation that allows you to test endpoints interactively:

1. Start the server:
   ```powershell
   uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

3. The Swagger UI allows you to:
   - View all available endpoints
   - See required parameters and request bodies
   - Execute requests directly from the browser
   - Authenticate using the "Authorize" button

## Manual API Testing

### Authentication

#### Register a new user

```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body $body
```

#### Login for access token

```powershell
$form = @{
    username = "test@example.com"
    password = "password123"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login/access-token" -Method Post -Form $form
$token = $response.access_token

# Save token for later use
$headers = @{
    Authorization = "Bearer $token"
}
```

### User Operations

#### Get current user

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/me" -Method Get -Headers $headers
```

#### Update user profile

```powershell
$updateBody = @{
    full_name = "Updated User Name"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/me" -Method Patch -ContentType "application/json" -Headers $headers -Body $updateBody
```

### Search Operations

#### Create a new search

```powershell
$searchBody = @{
    origin = "NYC"
    destination = "LON"
    departure_date = "2025-06-15"
    return_date = "2025-06-22"
    adults = 2
    children = 0
    cabin_class = "economy"
} | ConvertTo-Json

$searchResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/search/" -Method Post -ContentType "application/json" -Headers $headers -Body $searchBody
```

#### Get search history

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/search/history" -Method Get -Headers $headers
```

### Recommendations

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommendations/" -Method Get -Headers $headers
```

### Deals

```powershell
# Get all deals
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/deals/" -Method Get -Headers $headers

# Save a deal (assuming deal ID 1 exists)
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/deals/1/save" -Method Post -Headers $headers

# Get saved deals
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/deals/saved" -Method Get -Headers $headers
```

## CRUD Validation

We've created a script to validate all CRUD operations:

```powershell
# Run CRUD validation
python .\tests\validate_crud.py
```

This script tests:
- User creation, retrieval, update, and deletion
- Search creation and retrieval
- Other model operations

## Troubleshooting Common Issues

### Authentication Failures

- **Issue**: Getting 401 Unauthorized errors
- **Solution**: Ensure your token is valid and properly formatted in the Authorization header

### Database Connection Issues

- **Issue**: SQLAlchemy errors during tests
- **Solution**: Check database connection settings in conftest.py

### Test Data Not Found

- **Issue**: Tests fail because specific IDs don't exist
- **Solution**: Update test data or ensure proper test data is created before running tests

### Endpoint Not Found

- **Issue**: Getting 404 Not Found errors
- **Solution**: Verify API endpoint paths and check API router configuration

### Server Not Starting

- **Issue**: Error when starting uvicorn server
- **Solution**: Check port availability and ensure all dependencies are installed

## Conclusion

Use these testing tools to ensure your Smart Travel API is functioning correctly. Regular testing helps catch issues early and ensures a reliable application for your users.

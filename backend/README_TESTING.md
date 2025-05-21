# Smart Travel API Testing Tools

This directory contains various tools to help you test your Smart Travel API endpoints and CRUD operations. Below is a guide to the testing tools available.

## Available Testing Tools

1. **Automated Tests** (`tests/` directory)
   - Comprehensive pytest test suite for all API endpoints
   - Tests auth, users, search, recommendations, and deals endpoints

2. **Test Runner Script** (`run_tests.py`)
   - Python script that provides CLI for running different test scenarios
   - Run with `--help` flag to see all options

3. **PowerShell Test Menu** (`run_api_tests.ps1`)
   - Interactive menu for running various test scenarios
   - Just run the script and follow the prompts

4. **CRUD Validation Script** (`tests/validate_crud.py`)
   - Validates that all CRUD operations work correctly for all models
   - Tests create, read, update, and delete operations

5. **API Endpoint Tester** (`test_endpoints.ps1`)
   - Interactive tool to test specific API endpoints manually
   - Handles authentication and session management

6. **Server Starter** (`start_server.bat`)
   - Simple batch file to start the API server for testing

## Quick Start Guide

1. **Run automated tests**:
   ```
   python run_tests.py --all
   ```

2. **Start the test menu**:
   ```
   .\run_api_tests.ps1
   ```

3. **Validate CRUD operations**:
   ```
   python tests\validate_crud.py
   ```

4. **Test specific endpoints**:
   ```
   .\test_endpoints.ps1
   ```

5. **Start the API server for Swagger UI testing**:
   ```
   .\start_server.bat
   ```
   Then visit: http://localhost:8000/docs

## Detailed Testing Documentation

For more comprehensive testing instructions, please refer to the `API_TESTING_GUIDE.md` document.

Happy testing!

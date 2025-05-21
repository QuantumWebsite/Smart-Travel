"""
Validation script to test if all CRUD operations work correctly.
This script tests all the CRUD operations for each model in the application.
"""
import sys
import os
from typing import Dict, Any, List, Optional, Type

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate


# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_colored(message, color=RESET):
    """Print a message with color"""
    print(f"{color}{message}{RESET}")


def print_header(message):
    """Print a header message"""
    print("\n" + "=" * 80)
    print_colored(f"{BOLD}{message}{RESET}", YELLOW)
    print("=" * 80)


def print_success(message):
    """Print a success message"""
    print_colored(f"✓ {message}", GREEN)


def print_error(message):
    """Print an error message"""
    print_colored(f"✗ {message}", RED)


def test_user_crud(db: Session):
    """Test CRUD operations for User model"""
    print_header("Testing User CRUD operations")
    
    # Create a test user
    print("Creating test user...")
    email = "crud_test_user@example.com"
    password = "testpassword123"
    
    # Check if user already exists (from previous test runs)
    existing_user = crud.user.get_by_email(db, email=email)
    if existing_user:
        print(f"Deleting existing test user {email}...")
        db.delete(existing_user)
        db.commit()
    
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="CRUD Test User"
    )
    
    # Test create
    user = crud.user.create(db, obj_in=user_in)
    if user and user.email == email:
        print_success("User creation successful")
    else:
        print_error("User creation failed")
        return False
    
    # Test get by ID
    user_by_id = crud.user.get(db, id=user.id)
    if user_by_id and user_by_id.id == user.id:
        print_success("Get user by ID successful")
    else:
        print_error("Get user by ID failed")
        return False
    
    # Test get by email
    user_by_email = crud.user.get_by_email(db, email=email)
    if user_by_email and user_by_email.email == email:
        print_success("Get user by email successful")
    else:
        print_error("Get user by email failed")
        return False
    
    # Test update
    update_data = {"full_name": "Updated CRUD Test User"}
    updated_user = crud.user.update(db, db_obj=user, obj_in=update_data)
    if updated_user and updated_user.full_name == update_data["full_name"]:
        print_success("User update successful")
    else:
        print_error("User update failed")
        return False
    
    # Test authenticate
    auth_user = crud.user.authenticate(db, email=email, password=password)
    if auth_user and auth_user.id == user.id:
        print_success("User authentication successful")
    else:
        print_error("User authentication failed")
        return False
    
    # Test remove
    removed_user = crud.user.remove(db, id=user.id)
    if removed_user and removed_user.id == user.id:
        print_success("User removal successful")
    else:
        print_error("User removal failed")
        return False
    
    # Verify removal
    user_after_remove = crud.user.get(db, id=user.id)
    if user_after_remove is None:
        print_success("User removal verification successful")
    else:
        print_error("User removal verification failed")
        return False
    
    return True


def test_search_crud(db: Session):
    """Test CRUD operations for Search model"""
    print_header("Testing Search CRUD operations")
    
    # First create a test user for the search
    print("Creating test user for search...")
    user_in = UserCreate(
        email="search_test_user@example.com",
        password="testpassword123",
        full_name="Search Test User"
    )
    user = crud.user.create(db, obj_in=user_in)
    
    # Create search data
    from app.schemas.search import SearchCreate
    
    search_data = {
        "origin": "NYC",
        "destination": "LON",
        "departure_date": "2025-06-15",
        "return_date": "2025-06-22",
        "adults": 2,
        "children": 1,
        "cabin_class": "economy",
        "user_id": user.id
    }
    
    # Test create
    search_in = SearchCreate(**search_data)
    search = crud.search.create(db, obj_in=search_in)
    if search and search.destination == search_data["destination"]:
        print_success("Search creation successful")
    else:
        print_error("Search creation failed")
        return False
    
    # Test get by ID
    search_by_id = crud.search.get(db, id=search.id)
    if search_by_id and search_by_id.id == search.id:
        print_success("Get search by ID successful")
    else:
        print_error("Get search by ID failed")
        return False
    
    # Test get by user ID
    searches_by_user = crud.search.get_multi_by_user(db, user_id=user.id)
    if searches_by_user and len(searches_by_user) > 0:
        print_success("Get searches by user ID successful")
    else:
        print_error("Get searches by user ID failed")
        return False
    
    # Clean up
    crud.search.remove(db, id=search.id)
    crud.user.remove(db, id=user.id)
    
    return True


def main():
    """Main function to test all CRUD operations"""
    print_header("SMART TRAVEL API - CRUD VALIDATION")
    print(f"Testing CRUD operations for all models in {settings.APP_NAME}")
    
    db = SessionLocal()
    try:
        # Test all CRUD operations
        tests = {
            "User": test_user_crud,
            "Search": test_search_crud,
            # Add more tests for other models as needed
        }
        
        results = {}
        for name, test_func in tests.items():
            try:
                results[name] = test_func(db)
            except Exception as e:
                print_error(f"Error testing {name} CRUD: {str(e)}")
                results[name] = False
        
        # Print summary
        print_header("TEST SUMMARY")
        for name, result in results.items():
            if result:
                print_success(f"{name}: All CRUD operations working")
            else:
                print_error(f"{name}: Some CRUD operations failed")
        
        # Overall result
        if all(results.values()):
            print_success("All CRUD operations are working correctly!")
            return 0
        else:
            print_error("Some CRUD operations failed. Check the logs for details.")
            return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())

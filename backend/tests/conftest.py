"""
Test configuration for Smart Travel API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.db.base_class import Base


# Use in-memory SQLite for tests
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Setup test database
def setup_test_db():
    Base.metadata.create_all(bind=engine)


# Dependency override for database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Setup test client with overridden dependencies
def get_test_client():
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="module")
def test_app():
    # Set up the database
    setup_test_db()
    
    # Create a test client
    client = get_test_client()
    
    yield client  # this is where the testing happens
    
    # Clean up dependencies
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def test_db():
    # Set up the database
    setup_test_db()
    
    # Create a testing database session
    db = TestingSessionLocal()
    
    yield db  # this is where the testing happens
    
    # Clean up
    db.close()

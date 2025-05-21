# Smart Travel Backend

This is the backend API for the Smart Travel application, providing endpoints for travel deals, AI-powered recommendations, and more.

## Environment Setup

The backend uses a `.env` file to store configuration and secrets. Follow these steps to set up your environment:

1. Run the setup script to create your `.env` file with a secure secret key:

```bash
python -m scripts.setup_env
```

2. Open the `.env` file and fill in the required values:
   - Database credentials
   - Bright Data API keys (if using web scraping)
   - Any other API keys you need

3. For team development, create an example file without real secrets:

```bash
python -m scripts.setup_env --create-example
```

## Environment Variables

The following environment variables can be configured:

### Security
- `SECRET_KEY`: Secret key for JWT token encryption
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Database
- `POSTGRES_SERVER`: PostgreSQL server address
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

### Bright Data (Web Scraping)
- `BRIGHT_DATA_API_KEY`: API key for Bright Data
- `BRIGHT_DATA_ZONE_USERNAME`: Zone username
- `BRIGHT_DATA_ZONE_PASSWORD`: Zone password

### Application Settings
- `APP_NAME`: Name of the application
- `APP_ENVIRONMENT`: Environment (development, production)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### CORS Settings
- `BACKEND_CORS_ORIGINS`: List of origins that are allowed to make cross-origin requests
  - Format can be a comma-separated string: `http://localhost:3000,http://localhost:8000`
  - Or a JSON array: `["http://localhost:3000", "http://localhost:8000"]`
  - Add your production domains when deploying

## Important Security Notes

1. Never commit your `.env` file to version control
2. The `.gitignore` file is configured to exclude `.env` files
3. Use the `.env.example` file to share the structure without sharing secrets
4. Generate a strong `SECRET_KEY` for production environments

## Development Setup

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

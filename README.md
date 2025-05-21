# Smart Travel

![Smart Travel](https://img.shields.io/badge/Smart-Travel-blue)

Smart Travel is a modern travel application that helps users find the best travel deals, get AI-powered trip recommendations, and manage their travel plans with ease. The application includes features like flight and hotel searches, weather information, packing suggestions, and personalized travel recommendations.

## Project Overview

This application is built with:
- **Frontend**: Next.js-based web application with a modern UI
- **Backend**: FastAPI Python backend with PostgreSQL database
- **AI Features**: Integration with AI services for personalized recommendations and packing suggestions
- **Email Notifications**: System for travel alerts and user verification

## Features

- **Travel Deal Search**: Find the best flight and hotel deals
- **AI Recommendations**: Personalized travel recommendations based on user preferences
- **Weather Information**: Get weather forecasts for your destinations
- **Packing Suggestions**: AI-powered packing list suggestions based on destination and trip duration
- **User Accounts**: Save favorite deals and receive personalized recommendations
- **Email Notifications**: Receive alerts about travel deals and trip reminders

## Repository Structure

```
smart_travel/
├── backend/              # FastAPI backend service
│   ├── app/              # Main application code
│   ├── scripts/          # Utility scripts
│   └── tests/            # Backend tests
├── frontend/             # Next.js frontend application
│   ├── public/           # Static files
│   └── src/              # Frontend source code
├── docker/               # Docker configuration files
└── docs/                 # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- PostgreSQL database
- Docker and Docker Compose (optional, for containerized setup)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # OR
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   python -m scripts.setup_env
   ```
   Then edit the created `.env` file with your configuration values.

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   # OR use the batch file
   start_server.bat
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # OR
   yarn install
   ```

3. Create a `.env.local` file in the frontend directory with your environment variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   # OR
   yarn dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser to access the application.

### Docker Setup (Optional)

To run the entire application using Docker:

1. Make sure Docker and Docker Compose are installed on your system

2. Navigate to the project root directory

3. Build and start the containers:
   ```bash
   cd docker
   docker-compose up -d
   ```

4. Access the application at [http://localhost:3000](http://localhost:3000)

## Development

### API Documentation

When the backend server is running, you can access the API documentation at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Testing

#### Backend Tests

Run backend tests with:
```bash
cd backend
python run_tests.py
# OR use the PowerShell script
.\run_api_tests.ps1
```

#### Email Testing

For testing email functionality:
1. Start the MailDev server:
   ```bash
   .\start_maildev.ps1
   ```
2. Run the email tests:
   ```bash
   .\run_email_tests.ps1
   ```
3. Access the MailDev web interface at [http://localhost:1080](http://localhost:1080)

## Deployment

### Backend Deployment

The backend can be deployed as a Docker container or directly to a cloud service supporting Python applications.

### Frontend Deployment

The Next.js frontend can be deployed to services like Vercel, Netlify, or any platform supporting Node.js applications.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/)
- Database powered by [PostgreSQL](https://www.postgresql.org/)
@echo off
echo Starting Smart Travel API server...
echo Press Ctrl+C to stop the server
uvicorn app.main:app --reload

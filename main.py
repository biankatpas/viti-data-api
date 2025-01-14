"""
Entry point for the FastAPI application.

This module initializes the FastAPI application, includes API routes, and handles database initialization.

Components:
    - FastAPI application: The main app instance.
    - Router: Routes for API endpoints included from the `api.router` module.
    - Startup Event: Initializes the database tables on application startup.

Usage:
    Run this module to start the FastAPI server:
        python main.py

    Alternatively, use a command like uvicorn:
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI

from services.storage import db_handler
from api.router import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """
    Event handler triggered when the application starts.

    Initializes the database by creating all required tables.
    """
    
    db_handler.init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

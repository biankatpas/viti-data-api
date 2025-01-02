import logging
from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import Base
from api.routes import router
from services.storage.db_handler import engine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(router)


def init_db():
    """
    Initialize the database by creating all tables.
    """
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")

@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

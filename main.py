from fastapi import FastAPI

from services.storage import db_handler
from api.router import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    db_handler.init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

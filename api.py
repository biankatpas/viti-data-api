from fastapi import FastAPI

from data_ingestion.update_data import update_all_data

app = FastAPI()


@app.post("/update")
async def update_data_endpoint(year: int):
    """
    Endpoint to trigger data update for a specific year.
    """
    updated_data = update_all_data(year)
    return {"status": "success", "updated_data": list(updated_data.keys())}

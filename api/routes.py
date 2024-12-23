from fastapi import APIRouter

from .scrape import perform_scrape

router = APIRouter()


@router.get("/scrape")
async def scrape_endpoint(year: int):
    """
    Endpoint to trigger data scrape for a specific year.
    """

    data = perform_scrape(year)

    return {
        "status": "success",
        "data": data
    }

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .scrape import perform_scrape

router = APIRouter()


@router.get("/scrape")
async def scrape_route(year: int, page: str):
    """
    Endpoint to trigger page scrape for a specific year.
    """

    # TODO: store scraped data
    data = perform_scrape(year, page)
    print(data)

    response_content = {}
    return JSONResponse(
        content=response_content,
        status_code=200
    )

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from services.storage import db_handler, get_db, PageModelMapping
from .scrape import perform_scrape

router = APIRouter()


@router.get("/scrape")
async def scrape_route(year: int, page: str, db: Session = Depends(get_db)):
    """
    Endpoint to trigger page scrape for a specific year.
    """
    try:
        model = PageModelMapping[page.upper()].value
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page: {page}. Must be one of {[p.name for p in PageModelMapping]}."
        )

    try:
        scraped_data = perform_scrape(year, page.upper())

        if scraped_data.empty:
            return {"status": "error", "message": f"No data found for page {page}/{year}."}

        for _, row in scraped_data.iterrows():
            row_data = {
                **row.to_dict(),
                "year": year,
            }
            db_handler.store(
                db=db,
                model=model,
                **row_data
            )

        return {"status": "success", "message": f"Data for {page}/{year} stored successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

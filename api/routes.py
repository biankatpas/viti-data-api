import requests

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from services.storage import db_handler, get_db, PageModelMapping
from .scrape import perform_scrape
from .retrieve import (
    get_imports, get_exports, get_production, get_commercialization, get_processing, get_years_as_list
)

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

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch data for {page}/{year}. Reason: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/import")
async def import_route(
    years: str = Query(default=None, description="Comma-separated years"), db: Session = Depends(get_db)
):
    """
    Retrieve import data.
    """
    try:
        years_list = get_years_as_list(years)
        data = get_imports(db, years_list)
        return {"status": "success", "data": [row.__dict__ for row in data]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_route(
    years: str = Query(default=None, description="Comma-separated years"), db: Session = Depends(get_db)
):
    """
    Retrieve export data.
    """
    try:
        years_list = get_years_as_list(years)
        data = get_exports(db, years_list)
        return {"status": "success", "data": [row.__dict__ for row in data]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/production")
async def production_route(
    years: str = Query(default=None, description="Comma-separated years"), db: Session = Depends(get_db)
):
    """
    Retrieve production data.
    """
    try:
        years_list = get_years_as_list(years)
        data = get_production(db, years_list)
        return {"status": "success", "data": [row.__dict__ for row in data]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commercialization")
async def commercialization_route(
    years: str = Query(default=None, description="Comma-separated years"), db: Session = Depends(get_db)
):
    """
    Retrieve commercialization data.
    """
    try:
        years_list = get_years_as_list(years)
        data = get_commercialization(db, years_list)
        return {"status": "success", "data": [row.__dict__ for row in data]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/processing")
async def processing_route(
    years: str = Query(default=None, description="Comma-separated years"), db: Session = Depends(get_db)
):
    """
    Retrieve processing data.
    """
    try:
        years_list = get_years_as_list(years)
        data = get_processing(db, years_list)
        return {"status": "success", "data": [row.__dict__ for row in data]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import requests

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from services.storage import get_db, PageModelMapping
from .routes.scrape import perform_scrape, process_and_store_data
from .routes.retrieve import (
    get_imports, get_exports, get_production, get_commercialization, get_processing, get_years_as_list
)
from services.scraper.scraper_enums import ScraperPages

router = APIRouter()


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return JSONResponse(content={"message": "Welcome to the Viticulture Data API! Visit /docs for API documentation."})

@router.get(
    "/scrape",
    tags=["Scraping"],
    summary="Scrape data for a specific year and page",
    description=(
        "Trigger a web scraping process to fetch data for a given year and page. "
        "The scraped data is processed and stored in the database."
    ),
    responses={
        200: {
            "description": "Scraping completed successfully.",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message": "Data for PRODUCTION/2020 stored successfully."}
                }
            },
        },
        400: {
            "description": "Invalid page provided.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid page: TEST. Must be one of ['PRODUCTION', 'PROCESSING', ...]."}
                }
            },
        },
        503: {
            "description": "Failed to fetch data due to a request error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to fetch data for PRODUCTION/2020. Reason: Timeout error."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred during scraping.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred: Parser not found."}
                }
            },
        },
    },
)
async def scrape_route(year: int, page: str, db: Session = Depends(get_db)):
    """
    Scrape data for a specific year and page.

    This endpoint triggers a web scraping process for the specified year and page.
    The scraped data is processed, validated, and stored in the database.

    Args:
        year (int): The year for which data is to be scraped.
        page (str): The page to scrape, corresponding to a valid `ScraperPages` value.
        db (Session): Database session dependency.

    Returns:
        JSONResponse: Status and message indicating the result of the scraping operation.

    Raises:
        HTTPException: 400 - If the page is invalid.
        HTTPException: 503 - If there is a request error during scraping.
        HTTPException: 500 - For any unexpected errors during scraping or storage.
    """

    try:
        # Validate the page against PageModelMapping
        scraper_page = ScraperPages[page.upper()]
        model = PageModelMapping[page.upper()].value
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page: {page}. Must be one of {[p.name for p in PageModelMapping]}."
        )

    try:
        # Perform the scraping process
        scraped_data = perform_scrape(
            year=year,
            page=scraper_page,
        )

        if scraped_data is None:
            return {"status": "error", "message": f"No data found for page {page}/{year}."}

        # Process and store data
        results = {}
        for suboption, data in scraped_data.items():
            results[suboption] = process_and_store_data(
                scraped_data=data,
                db=db,
                model=model,
                year=year,
                suboption=suboption if suboption != "default" else None
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
            detail=f"TODO An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/import",
    tags=["Import Data"],
    summary="Retrieve import data",
    description=(
        "Fetch import data from the database, optionally filtered by a list of years. "
        "The years should be provided as a comma-separated string."
    ),
    responses={
        200: {
            "description": "Successfully retrieved import data.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "year": 2020,
                                "country": "USA",
                                "quantity": 1000,
                                "value": 50000
                            },
                            {
                                "id": 2,
                                "year": 2021,
                                "country": "Canada",
                                "quantity": 2000,
                                "value": 75000
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid years format.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid format for years. Expected comma-separated integers."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred while retrieving data."}
                }
            },
        },
    },
)
async def import_route(
    years: str = Query(
        default=None,
        description="Comma-separated list of years to filter the data. If not provided, all data will be returned."
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve import data.

    Args:
        years (str, optional): Comma-separated list of years to filter the data. Defaults to None.
        db (Session): Database session provided via dependency injection.

    Returns:
        dict: Status and retrieved data as a list of dictionaries.

    Raises:
        HTTPException:
            - 400: If the `years` string cannot be parsed into a list of integers.
            - 500: For any unexpected errors during data retrieval.
    """

    try:
        # Convert years string to a list of integers
        years_list = get_years_as_list(years)
        data = get_imports(db, years_list)

        # Convert SQLAlchemy objects to dictionaries for the response
        formatted_data = [
            {key: value for key, value in row.__dict__.items() if not key.startswith("_")}
            for row in data
        ]

        return {"status": "success", "data": formatted_data}

    except ValueError as e:
        # Handle invalid years format
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/export",
    tags=["Export Data"],
    summary="Retrieve export data",
    description=(
        "Fetch export data from the database, optionally filtered by a list of years. "
        "The years should be provided as a comma-separated string."
    ),
    responses={
        200: {
            "description": "Successfully retrieved export data.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "year": 2020,
                                "country": "Brazil",
                                "quantity": 1000,
                                "value": 50000
                            },
                            {
                                "id": 2,
                                "year": 2021,
                                "country": "Argentina",
                                "quantity": 2000,
                                "value": 75000
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid years format.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid format for years. Expected comma-separated integers."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred while retrieving data."}
                }
            },
        },
    },
)
async def export_route(
    years: str = Query(
        default=None,
        description="Comma-separated list of years to filter the data. If not provided, all data will be returned."
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve export data.

    Args:
        years (str, optional): Comma-separated list of years to filter the data. Defaults to None.
        db (Session): Database session provided via dependency injection.

    Returns:
        dict: Status and retrieved data as a list of dictionaries.

    Raises:
        HTTPException:
            - 400: If the `years` string cannot be parsed into a list of integers.
            - 500: For any unexpected errors during data retrieval.
    """

    try:
        # Convert years string to a list of integers
        years_list = get_years_as_list(years)
        data = get_exports(db, years_list)

         # Convert SQLAlchemy objects to dictionaries for the response
        formatted_data = [
            {key: value for key, value in row.__dict__.items() if not key.startswith("_")}
            for row in data
        ]

        return {"status": "success", "data": formatted_data}

    except ValueError as e:
        # Handle invalid years format
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/production",
    tags=["Production Data"],
    summary="Retrieve production data",
    description=(
        "Fetch production data from the database, optionally filtered by a list of years. "
        "The years should be provided as a comma-separated string."
    ),
    responses={
        200: {
            "description": "Successfully retrieved production data.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "year": 2020,
                                "product": "Wheat",
                                "quantity": 1000
                            },
                            {
                                "id": 2,
                                "year": 2021,
                                "product": "Corn",
                                "quantity": 2000
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid years format.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid format for years. Expected comma-separated integers."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred while retrieving data."}
                }
            },
        },
    },
)
async def production_route(
    years: str = Query(
        default=None,
        description="Comma-separated list of years to filter the data. If not provided, all data will be returned."
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve production data.

    Args:
        years (str, optional): Comma-separated list of years to filter the data. Defaults to None.
        db (Session): Database session provided via dependency injection.

    Returns:
        dict: Status and retrieved data as a list of dictionaries.

    Raises:
        HTTPException:
            - 400: If the `years` string cannot be parsed into a list of integers.
            - 500: For any unexpected errors during data retrieval.
    """

    try:
        # Convert years string to a list of integers
        years_list = get_years_as_list(years)
        data = get_production(db, years_list)

        # Convert SQLAlchemy objects to dictionaries for the response
        formatted_data = [
            {key: value for key, value in row.__dict__.items() if not key.startswith("_")}
            for row in data
        ]

        return {"status": "success", "data": formatted_data}

    except ValueError as e:
        # Handle invalid years format
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/commercialization",
    tags=["Commercialization Data"],
    summary="Retrieve commercialization data",
    description=(
        "Fetch commercialization data from the database, optionally filtered by a list of years. "
        "The years should be provided as a comma-separated string."
    ),
    responses={
        200: {
            "description": "Successfully retrieved commercialization data.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "year": 2020,
                                "product": "Wine",
                                "quantity": 1000
                            },
                            {
                                "id": 2,
                                "year": 2021,
                                "product": "Beer",
                                "quantity": 2000
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid years format.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid format for years. Expected comma-separated integers."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred while retrieving data."}
                }
            },
        },
    },
)
async def commercialization_route(
    years: str = Query(
        default=None,
        description="Comma-separated list of years to filter the data. If not provided, all data will be returned."
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve commercialization data.

    Args:
        years (str, optional): Comma-separated list of years to filter the data. Defaults to None.
        db (Session): Database session provided via dependency injection.

    Returns:
        dict: Status and retrieved data as a list of dictionaries.

    Raises:
        HTTPException:
            - 400: If the `years` string cannot be parsed into a list of integers.
            - 500: For any unexpected errors during data retrieval.
    """

    try:
        # Convert years string to a list of integers
        years_list = get_years_as_list(years)
        data = get_commercialization(db, years_list)

        # Convert SQLAlchemy objects to dictionaries for the response
        formatted_data = [
            {key: value for key, value in row.__dict__.items() if not key.startswith("_")}
            for row in data
        ]

        return {"status": "success", "data": formatted_data}

    except ValueError as e:
        # Handle invalid years format
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/processing",
    tags=["Processing Data"],
    summary="Retrieve processing data",
    description=(
        "Fetch processing data from the database, optionally filtered by a list of years. "
        "The years should be provided as a comma-separated string."
    ),
    responses={
        200: {
            "description": "Successfully retrieved processing data.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "year": 2020,
                                "variety": "Chardonnay",
                                "quantity": 1500
                            },
                            {
                                "id": 2,
                                "year": 2021,
                                "variety": "Pinot Noir",
                                "quantity": 1200
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid years format.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid format for years. Expected comma-separated integers."}
                }
            },
        },
        500: {
            "description": "An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred while retrieving data."}
                }
            },
        },
    },
)
async def processing_route(
    years: str = Query(
        default=None,
        description="Comma-separated list of years to filter the data. If not provided, all data will be returned."
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve processing data.

    Args:
        years (str, optional): Comma-separated list of years to filter the data. Defaults to None.
        db (Session): Database session provided via dependency injection.

    Returns:
        dict: Status and retrieved data as a list of dictionaries.

    Raises:
        HTTPException:
            - 400: If the `years` string cannot be parsed into a list of integers.
            - 500: For any unexpected errors during data retrieval.
    """

    try:
        # Convert years string to a list of integers
        years_list = get_years_as_list(years)
        data = get_processing(db, years_list)

        # Convert SQLAlchemy objects to dictionaries for the response
        formatted_data = [
            {key: value for key, value in row.__dict__.items() if not key.startswith("_")}
            for row in data
        ]

        return {"status": "success", "data": formatted_data}

    except ValueError as e:
        # Handle invalid years format
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

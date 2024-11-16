from .scraper_ingestion import scraper_ingestion


def update_data(year):
    scraped_data = scraper_ingestion(year)
    print("Scraping data updated.")

    updated_data = {
        "scraped": scraped_data,
    }

    return updated_data

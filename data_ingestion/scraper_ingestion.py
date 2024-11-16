from scraper.scraper import Scraper
from scraper.enums import ScraperOption


def scraper_ingestion(year):
    options = [
        ScraperOption.PRODUCTION,
        ScraperOption.PROCESSING,
        ScraperOption.COMMERCIALIZATION,
        ScraperOption.IMPORT,
        ScraperOption.EXPORT
    ]
    scraped_data = {}

    for option in options:
        print(f"Scraping data for {option.name} for year {year}...")

        scraper = Scraper(year=year, option=option)
        data = scraper.get_data()

        if data is not None:
            scraped_data[option] = data
            print(f"Data for {option.name} scraped successfully.")
        else:
            print(f"No data found for {option.name}.")

    return scraped_data

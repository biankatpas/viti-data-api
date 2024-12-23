from services.scraper.enums import ScraperOption
from services.scraper import Scraper


def perform_scrape(year):
    scraped_data = scrape_all_data(year)
    print("Scraping data updated.")

    return scraped_data,
    
def scrape_all_data(year):
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
        data = scraper.scrape()

        if data is not None:
            scraped_data[option] = data
            print(f"Data for {option.name} scraped successfully.")
        else:
            print(f"No data found for {option.name}.")

    return scraped_data

# Viticulture Data API

This REST API was developed using FastAPI to scrape, process, and store viticulture-related data such as production, processing, commercialization, import, and export information.

## Data Source

The data used in this API is scraped from [Embrapa's Viticulture and Enology Database](http://vitibrasil.cnpuv.embrapa.br/index.php).

## Core Features
* Data Scraping: Retrieve data from external sources using a scraping engine.
* Data Storage: Processed data is stored in a PostgreSQL database.
* API Endpoints: Access and query the stored data via dedicated endpoints.
* Swagger Documentation: Interactive API documentation is available at /docs.

## Running the Project

Follow these steps to run the Viticulture Data API using Docker:

**1. Prerequisites**

Before starting the project, ensure you have the following installed on your machine:

* Docker: download and install from Docker's official website.

**2. Clone the Repository**

Clone the repository to your local machine and navigate to the project directory:

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace <repository-url> with the URL of your repository and <repository-directory> with the name of the directory created by the clone command.

**3. Configure Environment Variables**

The project uses a .env file for configuration. Before running the project:

Create a `.env` file in the root directory of the project.
Use the provided `example.env` as a reference.

**4. Build and Start the Docker Containers**

Navigate to the root directory of the project and run the following command:

```bash
docker-compose up --build
```

This will build and start the FastAPI application and the PostgreSQL database container.

**5. Access the API Documentation**

Once the containers are running, open your browser and navigate to:

* Swagger UI: http://127.0.0.1:8000/docs

These pages provide interactive documentation of all available endpoints.

**6. Use the API**

You can use Postman or any other API client to test the available endpoints.

## API Endpoints Overview
Here are the core endpoints provided by the API:

**Scraping:**

`GET /scrape`: Trigger scraping for a specific page and year.

**Data Retrieval:**
  
`GET /import`: Retrieve import data.

`GET /export`: Retrieve export data.

`GET /production`: Retrieve production data.

`GET /commercialization`: Retrieve commercialization data.

`GET /processing`: Retrieve processing data.

Each retrieval endpoint supports filtering by a comma-separated list of years via the `years` query parameter.

### Example Request

Retrieve data for the year `2020` using the `/production` endpoint:

```bash
GET http://127.0.0.1:8000/production?years=2020
```

### Example Response

```bash
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "year": 2020,
      "product": "Wine",
      "quantity": 1500
    }
  ]
}
```

### Notes
Ensure the `.env` file is correctly configured before starting the containers.

If you encounter any issues, check the container logs:

```bash
docker-compose logs
```

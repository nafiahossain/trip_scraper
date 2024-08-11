# Trip Scraper

## Overview

A Scrapy project to scrape hotel data from Trip.com, download hotel images, and store the scraped data in a PostgreSQL database and JSON files.

## Features

- Scrapes hotel data from specified locations on Trip.com. 
- Downloads and stores hotel images in a local directory.
- Saves the scraped data in JSON files (Scraped_locations.json and Scraped_hotels.json).
- Stores the scraped data in a PostgreSQL database.

## Installation

### Prerequisites

- Python 3.7 or later
- Scrapy
- PostgreSQL
- SQLAlchemy
- dotenv (optional but recommended)
- Virtualenv (optional but recommended)

### Project Structure

    ```bash
    trip_scraper/
    ├── trip_scraper/
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders/
    │       ├── __init__.py
    │       └── trip_scraper.py
    ├── .env
    ├── scrapy.cfg
    ├── README.md
    └── requirements.txt
    ```
### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/nafiahossain/Flask_API.git
    cd Flask-API
    ```

2. **Create and activate a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
    
    or,
   
    ```bash
    pip install scrapy sqlalchemy psycopg2-binary python-dotenv pillow
    ```
   
5. **Set up environment variables**:

    Create a database:
    Step 1: Open the PostgreSQL Command Line
    First, access the PostgreSQL command line interface (CLI) or use a graphical user interface (GUI) tool like pgAdmin.

    Step 2: Connect to PostgreSQL
    If you're using the command line, connect to your PostgreSQL server. Replace username with your PostgreSQL username:
   
    ```sh
    psql -U username
    ```

    Step 3: Create the Database
    Once connected, use the following SQL command to create a database. Replace database_name with your desired database name:
   
    ```sql
    CREATE DATABASE yourdatabase;
    ```
    
    Then,
   
    Create a `.env` file in the project root directory and add the following:

    ```env
    DATABASE_URL=postgresql://username:password@localhost:5433/yourdatabase
    ```

7. **Initialize the database**:

    Ensure that your PostgreSQL server is running, and the database specified in the .env file is created.

7. **Configure Scrapy Settings**:

    ```python
    # settings.py

    ITEM_PIPELINES = {
        'trip_scraper.pipelines.CustomImagesPipeline': 1,
        'trip_scraper.pipelines.PostgreSQLPipeline': 2,
    }

    IMAGES_STORE = 'path/to/your/image_directory'  # Replace with your desired path

    ```
    Replace 'path/to/your/image_directory' with the actual path where you want to store the images.


8. **Run the application**:
    Run the Spider:

    Use the following command to start the scraper:

    ```bash
    scrapy crawl trip_scraper
    ```

    Output:

    Images: Downloaded and stored in the directory specified in IMAGES_STORE.
    Locations Data: Saved in Scraped_locations.json.
    Hotels Data: Saved in Scraped_hotels.json and stored in the PostgreSQL database.

## Testing


## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.


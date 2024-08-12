# Trip Scraper

## Overview

A Scrapy project to scrape hotel data from Trip.com, download hotel images, and store the scraped data in a PostgreSQL database and JSON files.  At first it scrapes all the locations on the start_url: https://uk.trip.com/hotels/?locale=en-GB&curr=GBP, then scrapes hotel data for few of those locations.

## Features

- Used Scrapy Spider to handle all the web scraping tasks efficiently.
- The scraped data is stored in a PostgreSQL database using SQLAlchemy. This ensures a structured and reliable storage solution.
- Automatic Table Creation and Image Storage:
    - The database tables are automatically created by SQLAlchemy, so there's no need for manual setup.
    - Scraped images are saved into a directory that is automatically created during runtime. The file paths for these images are stored in the database, making it easy to retrieve them later.
- Saves the scraped data in JSON files (Scraped_locations.json and Scraped_hotels.json).
- This README.md file includes detailed guidelines on how to set up and use the project. This includes everything from installing dependencies to running the Scrapy spider and accessing the stored data.


## Installation

### Prerequisites

- Python 3.7 or later
- Scrapy
- PostgreSQL
- SQLAlchemy
- dotenv (recommended for database confidentiality)
- Virtualenv (optional but recommended)

### Project Structure

    
    trip_scraper/
    ├── trip_scraper/
    │   ├── __init__.py
    │   ├── .env
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   ├── images/full/  # after running the program
    │   └── spiders/
    │       ├── __init__.py
    │       └── trip_scraper.py
    ├── scrapy.cfg
    ├── README.md
    ├── Scraped_locations.json
    ├── Scraped_hotels.json
    └── requirements.txt
    

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/nafiahossain/trip_scraper.git
    cd trip_scraper
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
    Once connected, use the following SQL command to create a database. Replace yourdatabase with your desired database name:
   
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

    - Custom Pipelines

        - CustomImagesPipeline: Downloads images and stores them in the specified directory. It also updates the images field in each HotelItem with the paths of the downloaded images.
        - PostgreSQLPipeline: Stores the scraped hotel data in a PostgreSQL database.
    
    - Notes
        - Ensure that the image_urls field in HotelItem is correctly populated with the URLs of the images you want to download.
        - Adjust the settings in settings.py to customize the image storage location and other Scrapy settings.

8. **Run the application**:

    - Run the Spider:

    Use the following command to start the scraper:

    ```bash
    cd trip_scraper
    scrapy crawl trip_scraper
    ```

    - Output:

        - Images: Downloaded and stored in the directory specified in IMAGES_STORE.
        - Locations Data: Saved in Scraped_locations.json (For visualizing how the data scraped from trip.com).
        - Hotels Data: Saved in Scraped_hotels.json (For visualizing how the data scraped from trip.com).
        - Database: Scraped hotel data stored in 'yourdatabase', in the PostgreSQL database.

## Testing

Check the json files where the scraped data for locations and hotels were stored. Also check your database and image directory  whether the data was scraped or not. 

## Starting New Project (optional)

If you want to create a new scrapy project, then run this following commands: 

    
    scrapy startproject trip_scraper
    

To initiate the spider,

    
    scrapy genspider trip_scraper
    

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.


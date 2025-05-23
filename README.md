# Starbucks DB

[![Scrape latest data](https://github.com/ngshiheng/starbucksdb/actions/workflows/scrape.yml/badge.svg)](https://github.com/ngshiheng/starbucksdb/actions/workflows/scrape.yml)

This is a data collection and storage project focused on Starbucks Singapore store and menu information. It uses web scraping techniques to gather data about Starbucks locations, menu items, and pricing, storing this information in a SQLite database for easy access and analysis.

## How It Works

```mermaid
graph TB
    subgraph Railway
        deployment[Datasette]
        class deployment vercel;
    end
    subgraph GitHub
        subgraph Actions
            scraper[scrape.py]
        end
        subgraph Artifacts
            db[(starbucks.db)]
            class db artifacts;
        end
    end
    subgraph Starbucks
        api[API]
    end
    subgraph DockerHub
        dockerhub[Docker Hub]
    end
    db --> |1: Download| scraper
    api --> |2: Fetch Data| scraper
    scraper --> |3: Upload| db
    scraper --> |4: Publish to Docker Hub| dockerhub
    dockerhub --> |5: Pull Image and Deploy| deployment
    deployment --> |6: View/Access Data| client[User]
```

## Installation

1. Clone the repository: `git clone https://github.com/ngshiheng/starbucksdb.git`
2. Install `uv`

## Usage

```sh
# To run the spider and collect data:
make run
```

## Database Schema

```mermaid
erDiagram
    STORES {
        INTEGER id PK "Primary Key"
        VARCHAR branch_code "Not Null"
        VARCHAR outlet_code "Not Null"
        VARCHAR store_code "Not Null"
        VARCHAR store_name "Not Null"
        VARCHAR address "Not Null"
        VARCHAR postal_code "Not Null"
        VARCHAR phone_no "Not Null"
        REAL longitude "Not Null"
        REAL latitude "Not Null"
        INTEGER monp_status "Not Null"
        INTEGER delivery_status "Not Null"
        INTEGER open_now "Not Null"
        JSON service_hours "Not Null"
        JSON amenities "Not Null"
    }

    MENU_ITEMS {
        INTEGER id PK "Primary Key"
        INTEGER store_id FK "Foreign Key"
        VARCHAR item_id "Not Null"
        VARCHAR item_code
        VARCHAR name "Not Null"
        VARCHAR description "Not Null"
        JSON photo_urls "Not Null"
        INTEGER is_mobile_order_pay "Not Null"
        INTEGER is_delivery "Not Null"
        INTEGER is_inventoried "Not Null"
        INTEGER is_featured "Not Null"
        INTEGER is_scheduled "Not Null"
        INTEGER is_dine_in "Not Null"
    }

    ITEM_PRICES {
        INTEGER id PK "Primary Key"
        INTEGER item_id FK "Foreign Key"
        INTEGER store_id FK "Foreign Key"
        INTEGER base_price "Not Null"
        INTEGER delivery_price "Not Null"
        DATE effective_date "Not Null"
    }

    STORES ||--o{ MENU_ITEMS : "has many"
    STORES ||--o{ ITEM_PRICES : "has many"
    MENU_ITEMS ||--o{ ITEM_PRICES : "has many"

```

The project uses three main models:

1. `Store`: Represents a Starbucks store location
2. `Item`: Represents a menu item
3. `Price`: Represents the pricing information for an item at a specific store

For detailed schema information, refer to the [`database.py`](./starbucksdb/models/database.py) file.

## License

This project is licensed under the [MIT License](./LICENSE).

## Disclaimer

This software is only used for research purposes, users must abide by the relevant laws and regulations of their location, please do not use it for illegal purposes. The user shall bear all the consequences caused by illegal use.

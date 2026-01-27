# Faculty Finder – Data Engineering Pipeline

## Overview

Faculty Finder is an end-to-end **Data Engineering project** that builds a clean, structured, and API-accessible dataset of university faculty information.

The system crawls multiple faculty web pages, normalizes the data, stores it in a relational database, and exposes it through a FastAPI service for downstream analytics and application use.

---

## Problem Statement

Faculty information is typically distributed across multiple web pages and stored in semi-structured HTML formats.

The objective of this project is to:

- Crawl faculty profile data from university's multiple faculty web pages
- Normalize and clean scraped HTML data
- Store structured faculty information in a relational database
- Serve the data via a  REST API

---

## System Architecture

```
Faculty Web Pages (HTML)
        ↓
Data Ingestion (Web Scraping)
        ↓
Data Transformation (Cleaning & Normalization)
        ↓
SQLite Database (faculty.db)
        ↓
FastAPI Service
```

---

## Tech Stack

- **Ingestion:** Python, Requests, BeautifulSoup
- **Transformation:** Pandas
- **Storage:** SQLite
- **Database Access:** SQLAlchemy
- **API / Serving:** FastAPI
- **API Documentation:** Swagger (OpenAPI)

---

## Database Design

- **Database:** `faculty.db`

- **Table:** `faculty`
- Here we scraped total 111 faculty's details
- RangeIndex: 111 entries, 0 to 110
-  Data columns (total 6 columns):
   
| Column          | Type               | Non-Null Count | Description                |
|-----------------|--------------------|----------------|----------------------------|
| faculty_id      | TEXT (Primary Key) | 111            | Unique faculty identifier  |
| name            | TEXT               | 111            | Faculty name               |
| profile_url     | TEXT               | 111            | Faculty profile URL        |
| education       | TEXT               | 111            | Education details          |
| email           | TEXT               | 110            | Email address              |
| contact_number  | TEXT               | 107            | Contact number             |
| research_area   | TEXT               | 108            | Research interests / areas |
---

## API Endpoints

The FastAPI service exposes faculty data through RESTful endpoints. All responses are returned in **JSON format** and are automatically documented using **Swagger (OpenAPI)**.

### 1. Get All Faculty

Returns a list of all faculty members available in the database.

**Endpoint**
```
GET /faculty
```

**Description**
- Fetches all faculty records
- Results are ordered by `faculty_id`
- Suitable for analytics, dashboards, and downstream processing

**Sample Response**
```json
[
  {
    "faculty_id": "F-4821",
    "name": "Abhishek Gupta",
    "profile_url": "https://www.daiict.ac.in/faculty/...",
    "education": "PhD (Electrical and Computer Engineering)",
    "email": "abhishek@daiict.ac.in",
    "contact_number": "+91-79-xxxxxxx",
    "research_area": "Machine Learning, Signal Processing"
  }
]
```

**HTTP Status Codes**
- `200 OK` – Successful response
- `500 Internal Server Error` – Database or server issue

---

## How to Run the Project

### 1. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pandas requests beautifulsoup4
```

### 2. Create the Database

Run the SQLAlchemy setup script to create `faculty.db` and the `faculty` table.

### 3. Run the API

```bash
uvicorn main:app --reload
```

### 4. Access the API

- API Endpoint: http://127.0.0.1:8000/faculty
- Swagger UI: http://127.0.0.1:8000/docs

---

## Key Data Engineering Concepts Applied

- Multi-page web scraping
- Data cleaning and normalization
- Relational schema design
- SQLite-based persistent storage
- API-based data serving with FastAPI

---

## Future Enhancements

- Pagination and filtering in APIs
- Faculty search by research area
- Semantic search using embeddings
- Containerized deployment using Docker

---

## Author

- **Kunal Pramanik | 202518001**
- **Jinal Sasiya | 202518062**  



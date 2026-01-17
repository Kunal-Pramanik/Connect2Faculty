# Faculty Finder – Data Engineering Pipeline

## Overview
Faculty Finder is an end-to-end **Data Engineering project** that builds a clean, structured, and API-accessible dataset of university faculty information.  
The system enables downstream **semantic search and NLP use cases** by exposing cleaned faculty bios and research interests through a FastAPI service.

This project focuses on **data ingestion, transformation, storage, and serving**, following real-world data engineering practices.

---

## Problem Statement
Faculty information is often scattered across multiple web pages and stored in unstructured formats.  
The objective of this project is to:
- Crawl faculty profile data from a university website
- Clean and normalize unstructured HTML content
- Store the processed data in a relational database
- Serve the data via an API for analytics and semantic search

---

## System Architecture

```
Faculty Web Pages (HTML)
        
        ↓
Data Ingestion (Web Scraping)
        
        ↓
Data Transformation (Cleaning & Normalization)
        
        ↓
PostgreSQL Storage
        
        ↓
FastAPI Service
        
        ↓
Downstream NLP / Semantic Search
```


---

## Tech Stack

- **Ingestion:** Python, Requests, BeautifulSoup  
- **Transformation:** Pandas, Text Cleaning  
- **Storage:** PostgreSQL  
- **API / Serving:** FastAPI  
- **Database Access:** SQLAlchemy  
- **API Documentation:** Swagger (OpenAPI)

---

## Database Design

**Database:** `Faculty_finder`  
**Schema:** `faculty_list`  
**Table:** `faculty`

| Column | Type | Description |
|------|-----|-------------|
| faculty_id | TEXT (Primary Key) | Unique faculty identifier |
| name | TEXT | Faculty name |
| education | TEXT | Education details |
| research_interests | TEXT | Research interests |
| profile_url | TEXT | Faculty profile URL |
| clean_text | TEXT | Cleaned text for NLP tasks |

---

## API Endpoints

The FastAPI service exposes faculty data through RESTful endpoints.  
All responses are returned in **JSON format** and are documented using Swagger (OpenAPI).

---
### Get All Faculty
 
Returns the complete list of faculty members with cleaned and structured information.  
This endpoint serves as the primary hand-off point for downstream analytics and NLP tasks.

**Sample Response**
```json
[
  {
    "faculty_id": "F-1",
    "name": "Abhishek Gupta",
    "education": "PhD (Electrical and Computer Engineering)",
    "research_interests": "Machine Learning, Signal Processing",
    "profile_url": "https://...",
    "clean_text": "machine learning signal processing ..."
  }
]
```

---
## How to Run the Project

### 1. Install Dependencies
pip install fastapi uvicorn sqlalchemy psycopg2 pandas

### 2. Start PostgreSQL
Ensure PostgreSQL is running and the database/table are created.

### 3. Run the API
uvicorn main:app --reload

### 4. Access the API
- API Endpoint: http://127.0.0.1:8000/faculty  
- Swagger UI: http://127.0.0.1:8000/docs  

---

## Key Data Engineering Concepts Applied
- Web data ingestion and scraping  
- Data cleaning and normalization  
- Relational schema design  
- Persistent storage using PostgreSQL  
- API-based data serving with FastAPI  

---

## Future Enhancements
- Semantic search using text embeddings  
- Full-text search in PostgreSQL  
- Pagination and filtering in APIs  
- Containerized deployment using Docker  

---

## Author
**Kunal Pramanik , Jinal Sasiya**  
MSc Data Science 

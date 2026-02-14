# ✨ Connect2Faculty – End-to-End Semantic Faculty Search System

An end-to-end Big Data Engineering (BDE) pipeline and semantic search platform.

Developed a custom crawler to scrape and clean university faculty data, implemented a high-dimensional vector search engine using FastAPI and Hugging Face transformers, and deployed a responsive Next.js frontend for real-time AI-powered mentor discovery.

---

## 🟢 Live System
**Hosted on Vercel & Render** 👉 [https://faculty-connect-data-riders-pi.vercel.app](https://faculty-connect-data-riders-pi.vercel.app/)

---

## 📑 Table of Contents

- [Overview](#overview)
- [Why Semantic Search?](#why-semantic-search)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Key Technical Expertise](#key-technical-expertise)
- [Project Structure](#project-structure)
- [Pipeline Workflow](#pipeline-workflow)
- [Data Schema & Engineering](#data-schema--engineering)
- [Semantic Search & Vector Retrieval](#semantic-search--vector-retrieval)
- [Data Intelligence & Statistics](#data-intelligence--statistics)
- [API Usage](#api-usage)
- [Installation & Setup](#installation--setup)
- [Cloud Deployment & Resilience](#cloud-deployment--resilience)
- [Help & Troubleshooting](#help--troubleshooting)
- [The Data Riders Team](#the-data-riders-team)

---

## <a id="overview"></a>🚀 Overview

**Connect2Faculty** is an intelligent faculty discovery platform that enables **semantic, intent-based search** over university faculty profiles, going beyond traditional keyword matching. 

### 💡 The Problem & Solution
Traditional search systems fail when terminology differs. A student searching for **"Financial Prediction"** might miss an expert listed under **"Stochastic Portfolio Theory"**. Connect2Faculty solves this by mapping research ideas into a shared **384-dimensional semantic vector space**, recognizing conceptual relationships between modern research terms and foundational specializations.

### 🔄 System Workflow
1. **Scrape & Ingest**: Automated crawling of faculty profiles using **BeautifulSoup4**.
2. **Clean & Transform**: Advanced text normalization and email de-obfuscation via **Pandas**.
3. **Embed & Index**: Generation of dense vector representations using **Hugging Face Transformers**.
4. **Search & Rank**: High-speed **Cosine Similarity** retrieval powered by **NumPy** and **FastAPI**.

---

## <a id="why-semantic-search"></a>💡 Why Semantic Search?

Keyword-based search relies on exact word matching and fails when user intent and terminology differ. In academic discovery, the same research area is often described using varied or specialized language.

Semantic search captures the **meaning and context** of queries and documents using vector embeddings, enabling intent-aware retrieval and robust handling of synonyms.

**Example:**  
A user searching *“I want to work on GenAI”* can correctly retrieve faculty profiles mentioning *“large language models”*, *“deep learning”*, or *“artificial intelligence”*, even when the exact term *“GenAI”* is absent.

As a result, semantic search provides more accurate faculty matching and a significantly improved search experience compared to traditional keyword search.

---

## <a id="system-architecture"></a> ⚙️ System Architecture

The project follows a modular, decoupled architecture to separate the heavy data engineering pipeline from the real-time AI inference and user interface.

```text
[ Web Sources: DA-IICT Faculty Directories ]
           ↓
[ Data Pipeline: scrapy.py → data_preprocessing.py → data_push_db.py ]
           ↓
[ Relational Storage: SQLite DB (faculty.db) ]
           ↓
[ AI Model Service: Hugging Face Router API → all-MiniLM-L6-v2 ]
           ↓
[ Production Backend: FastAPI (main.py + faculty_data.pkl) ]
           ↓
[ Frontend UI: Next.js 14 (Tailwind CSS + Lucide React) ]
```
---

## <a id="tech-stack"></a>🛠️ Tech Stack

The system is built using a modern, decoupled architecture to handle the requirements of data engineering and real-time AI inference.

### 🏗️ Backend & Data Engineering
* **Python 3.10+**: The core language for the entire data lifecycle and API development.
* **FastAPI**: A high-performance, asynchronous web framework used to serve search results with minimal latency.
* **BeautifulSoup4**: The primary tool for the automated scraping pipeline, handling complex and inconsistent HTML layouts.
* **Pandas & NumPy**: Used for rigorous data cleaning, ETL processes, and optimized matrix-based similarity calculations.
* **SQLite**: A lightweight relational database for persistent metadata storage.

### 🤖 Artificial Intelligence & NLP
* **Sentence-Transformers**: Specifically the `all-MiniLM-L6-v2` model, used to map research text into 384-dimensional semantic vectors.
* **Hugging Face Inference API**: Provides a scalable cloud environment for real-time model inference without heavy local resource usage.
* **Pickle (Serialization)**: Used to store and instantly load pre-computed vector embeddings for production speed.

### 🖥️ Frontend & UX
* **Next.js 14**: A modern React framework used for a responsive, "zero-build" user interface.
* **Tailwind CSS**: Utility-first styling used to create a professional, dark-themed academic dashboard.
* **Lucide React**: For high-quality, lightweight vector iconography.
---

## <a id="key-technical-expertise"></a>🧠 Key Technical Expertise

### 🛠️ Data Engineering & ETL
* **Automated Ingestion**: Developed a resilient multi-source scraper using **BeautifulSoup4** for deep metadata extraction.
* **Pipeline Architecture**: Engineered a modular ETL workflow for text normalization and email de-obfuscation.
* **Relational Storage**: Architected a dual-persistence layer using **SQLite** and **Pickle** for high-speed retrieval.

### 🤖 AI & Semantic Discovery
* **Neural Vectorization**: Leveraged **Transformers** (`all-MiniLM-L6-v2`) to map expertise into a 384-dimensional space.
* **Optimized Retrieval**: Implemented high-concurrency similarity ranking using **NumPy** matrix operations.
* **Contextual Matching**: Solved the "keyword gap" by enabling intent-based discovery.

### 🌐 Full-Stack Deployment
* **Asynchronous Backend**: Built a high-performance **FastAPI** engine for real-time inference.
* **Modern Frontend**: Developed a responsive dashboard using **Next.js 14** and **Tailwind CSS**.
* **Cloud Infrastructure**: Orchestrated a decoupled deployment on **Render** and **Vercel** with integrated resilience.

---
## <a id="project-structure"></a>📂 Project Structure

```bash
Connect2Faculty/
├── backend/                  # FastAPI Production Server
│   ├── main.py               # API logic & Semantic Retrieval
│   ├── faculty_data.pkl      # Serialized vector database
│   └── requirements.txt      # Backend dependencies
├── data_pipeline/            # Data Engineering & ETL Module
│   ├── scrapy.py             # BeautifulSoup4 Scraper
│   ├── data_preprocessing.py # Text normalization & Email de-obfuscation
│   ├── data_push_db.py       # SQL table creation & data loading
│   ├── faculty.db            # SQLite metadata storage
│   └── data.ipynb            # EDA & Data Statistics
├── frontend/                 # Next.js 14 Web Application
│   ├── src/app/page.tsx      # Semantic search UI
│   └── tailwind.config.ts    # Custom styling
└── README.md                 # Project documentation
```

---
## <a id="pipeline-workflow"></a>🔄 Pipeline Workflow

The project implements a resilient ETL pipeline that automates the transition from raw web sources to a structured AI database.

### 📥 1. Extraction (scrapy.py)
* **Targeted Crawling**: Scrapes 5 categories of faculty directories for 100% coverage.
* **Deep Scrape**: Navigates into individual profile links to extract biographies and publications.
* **Resilience**: Integrated 1s delays and custom headers to ensure stable ingestion.

### 🔄 2. Transformation (data_preprocessing.py)
* **Text Normalization**: Regex-based cleaning of research interests for high-quality embeddings.
* **Email De-obfuscation**: Automated recovery of contact details from web-protected formats.
* **Integrity Filters**: Drops incomplete records and maps standardized Faculty IDs (F-XXX).

### 📤 3. Loading (data_push_db.py)
* **Metadata Persistence**: Structured data is committed to a relational SQLite database.
* **Vector Serialization**: Pre-computed embeddings are stored in a Pickle (.pkl) file for O(1) loading.

---

## <a id="data-schema--engineering"></a>🗄️ Data Schema & Engineering

The system utilizes a dual-storage strategy: a relational **SQLite** database(`faculty.db`) for structured metadata and a serialized **Pickle** vector store for high-speed AI retrieval.

### 📊 Database Schema (faculty table)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **faculty_id** | `TEXT (PK)` | Unique identifier (e.g., F-001). |
| **Name** | `TEXT` | Full name of the faculty member. |
| **Email** | `TEXT` | De-obfuscated contact address. |
| **Specialization** | `TEXT` | Primary academic domain. |
| **Research_Interests**| `TEXT` | Normalized text for vector embeddings. |
| **Qualification** | `TEXT` | Academic background. |
| **Profile_URL** | `TEXT` | Link to institutional profile. |
| **Image_URL** | `TEXT` | Path to profile image. |

### ⚙️ Engineering Highlights
* **Primary Key Indexing**: Optimized `faculty_id` for fast metadata retrieval.
* **Data Normalization**: Cleaned and standardized all text inputs during the ETL process.
* **Hybrid Storage**: Combined SQL for relational data with Pickle for high-dimensional vector math.

---
## <a id="semantic-search--vector-retrieval"></a>🧠 Semantic Search & Vector Retrieval

Unlike traditional search, Connect2Faculty understands the **intent** behind your query using high-dimensional vector math.

### 1. Neural Representation
* **Model**: Sentence-Transformers `all-MiniLM-L6-v2`.
* **Latent Space**: Maps research interests into a **384-dimensional space**.
* **Semantic Awareness**: Recognizes conceptual relationships between varied academic terminologies.

### 2. Retrieval Engine
* **Real-time Inference**: Queries are vectorized via **Hugging Face Inference API**.
* **Mathematical Ranking**: Uses **NumPy-powered Cosine Similarity** to calculate the distance between user intent and faculty expertise.
* **Production Speed**: Pre-computed embeddings in **Pickle** format allow for sub-millisecond search performance.

---
## <a id="data-intelligence--statistics"></a>📊 Data Intelligence & Statistics

### 📉 Global Dataset Insights( `data_eda.ipynb` )
* **Education Quality**: 84.40% of faculty hold a PhD.
* **Research Productivity**: Average of 7.41 publications per faculty (Range: 0 - 50).
* **Information Density**: 55.05% have detailed teaching info available.

### 📊 Full Column-wise Data Quality (Null Analysis)

| # | Column Name | Non-Null Count | Availability | System Significance |
| :--- | :--- | :--- | :--- | :--- |
| 0 | **Name** | 112 | 100% | Primary UI display identifier. |
| 1 | **Profile URL** | 112 | 100% | Foundation for deep-crawling. |
| 2 | **Qualification** | 110 | 98.2% | Academic background context. |
| 3 | **Phone** | 79 | 70.5% | Optional direct contact info. |
| 4 | **Address** | 77 | 68.7% | Physical office location. |
| 5 | **Email** | 111 | 99.1% | Core student-faculty contact. |
| 6 | **Specialization** | 109 | 97.3% | Secondary semantic search anchor. |
| 7 | **Image URL** | 112 | 100% | Visual profile representation. |
| 8 | **Biography** | 69 | 61.6% | Detailed career context for NLP. |
| 9 | **Research Interests**| 109 | 97.3% | Primary source for vector embeddings. |
| 10 | **Teaching** | 60 | 53.5% | Pedagogical background. |
| 11 | **Publications** | 70 | 62.5% | Research output context. |

### 🧠 Semantic Retrieval Intelligence
* **Index Density**: 109 high-quality profiles post-cleaning.
* **Vector Coverage**: 100% mapping of research context into 384-dim space.
* **Contact Efficiency**: 99.1% email availability for faculty discovery.

---

## <a id="api-usage"></a>🧪 API Usage

The **Connect2Faculty** backend is powered by **FastAPI**, providing a high-concurrency asynchronous interface for both literal metadata retrieval and neural semantic search.

---

### ▶️ Start the Server

To launch the backend locally, use the **Uvicorn ASGI server**:

```bash
uvicorn main:app --reload --port 8000
```
### 🔗 System Endpoints

| Method | Endpoint                                   | Description                                                                 |
|--------|--------------------------------------------|-----------------------------------------------------------------------------|
| GET    | `/`                                        | Serves the integrated frontend UI.                                          |
| GET    | `/faculty`                                 | Retrieves the full directory of **109 verified faculty records**.           |
| GET    | `/faculty/search?query_str=...`            | Executes a **keyword-based search** across names and specializations.       |
| GET    | `/faculty/semantic-search?query_str=...`   | **AI-Powered Retrieval**: Maps user intent into a **384-dimensional vector space**. |

### 📌 Example: Semantic Search Request

**Request**
```http
GET /faculty/semantic-search?query_str=deep learning for healthcare
```
**Sample Response**
```json
{
  "query": "deep learning for healthcare",
  "results": [
    {
      "faculty_id": "F-005",
      "name": "Ajay beniwal",
      "match_percentage": "94.2%",
      "specialization": "Flexible and Printable Electronics for Healthcare...",
      "email": "ajay_beniwal@dau.ac.in"
    }
  ]
}
```

---

## <a id="installation--setup"></a>⚙️ Installation & Setup: A Step-by-Step Guide

This guide walks you through setting up the complete **Connect2Faculty** ecosystem, ensuring the data pipeline, AI backend, and user interface are fully synchronized.

---

## Step 1: Environment Preparation

Before beginning, ensure you have **Python 3.10+** and **Node.js (LTS)** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/Kunal-Pramanik/Faculty-Finder.git
cd Faculty-Finder
```
### 2. Obtain an API Token

- Visit **Hugging Face** and generate a free **Access Token**.
- This token is required to vectorize search queries in real time.

---

## Step 2: Backend & AI Engine Setup

The backend handles the semantic search logic and serves the faculty data.

### 1. Navigate to Backend

```bash
cd backend
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### Configure Environment Variables

Create a `.env` file inside the `backend` directory and add your token:

```env
HF_TOKEN=your_hugging_face_token_here
```
### 4. Launch the FastAPI Server

```bash
uvicorn main:app --reload --port 8000
```
- The server will now be live at: ``` http://localhost:8000```

---

## Step 3: Frontend & Dashboard Setup

The frontend provides the responsive interface for interacting with the semantic search engine.

### 1. Navigate to Frontend
Open a new terminal window and run:

    cd frontend

### 2. Install Node Packages

    npm install

### 3. Start the Development Server

    npm run dev

The dashboard will be accessible at:``` http://localhost:3000```

---
## Step 4: Data Pipeline (Optional)

If you wish to re-scrape or update the faculty database, follow these steps inside the `data_pipeline` directory.

### 1. Run the Scraper
- Execute `scrapy.py` to crawl institutional pages and collect raw HTML.

### 2. Pre-process Data
- Run `data_preprocessing.py` to clean text and de-obfuscate emails.

### 3. Update Database
- Run `data_push_db.py` to commit changes to the SQLite and Pickle storage layers.

---
## <a id="cloud-deployment--resilience"></a>☁️ Cloud Deployment & Resilience

The system is architected for high availability and consistent performance in a production environment.

* **Decoupled Deployment**: The **FastAPI** backend is hosted on **Render**, while the **Next.js 14** frontend is deployed on **Vercel** for optimal edge delivery.
* **Self-Healing Thread**: Implemented a background **Keep-Alive Thread** in `main.py` that periodically pings the server instance to prevent Render's free tier from entering "sleep mode," ensuring zero cold-start latency for users.
* **Inference Offloading**: Leverages the **Hugging Face Inference API** to handle heavy transformer computations, keeping the core backend lightweight and cost-efficient.
* **State Persistence**: Uses serialized **Pickle** storage to ensure the vector database is instantly available across server restarts.

---
## <a id="help--troubleshooting"></a>❓ Help & Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **API Error: 401 Unauthorized** | Ensure your `HF_TOKEN` is correctly set in your environment variables. |
| **Search Latency (Cold Start)** | The first query may take ~20s if the Hugging Face model is warming up. |
| **ModuleNotFoundError** | Run `pip install -r requirements.txt` to ensure all NLP dependencies are met. |
| **Empty Search Results** | Verify that `faculty_data.pkl` is present in the backend directory. |
| **Server Idling** | If the API is unresponsive, restart the service to reactivate the Keep-Alive thread. |

----
## <a id="the-data-riders-team"></a>👥 The Data Riders Team

This project was developed by **The Data Riders** to streamline faculty discovery through AI and robust data pipelines.

* **Kunal Pramanik** – Data Engineering & Backend Architecture.
* **Jinal Sasiya** – Frontend Development & UI/UX Design.

---

from fastapi import FastAPI , Query
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List, Optional

# SQLite connection
DATABASE_URL = "sqlite:///faculty.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

app = FastAPI(title="Faculty API (SQLite)")

class FacultyResponse(BaseModel):
    faculty_id: str
    name: str
    profile_url: Optional[str]
    education: Optional[str]
    email: Optional[str]
    contact_number: Optional[str]
    research_area: Optional[str]

@app.get("/faculty", response_model=List[FacultyResponse])
def get_faculty():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    faculty_id,
                    name,
                    profile_url,
                    education,
                    email,
                    contact_number,
                    research_area
                FROM faculty
                ORDER BY faculty_id
            """)
        )
        return result.mappings().all()



@app.get(
    "/faculty-details-by-name",
    response_model=List[FacultyResponse],
    summary="Get details by faculty name",
    description="Enter a faculty name to retrieve their details"
)
def get_research_area_by_name(
    name: str = Query(..., description="Full name of the faculty")
):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM faculty
                WHERE name = :name
            """),
            {"name": name}
        )
        return result.mappings().all()


@app.get(
    "/search-by-research-area",
    response_model=List[str],
    summary="Search faculty by research area keyword"
)
def search_faculty_by_research_area(
    keyword: str = Query(..., description="Keyword like Machine Learning")
):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT name
                FROM faculty
                WHERE LOWER(research_area) LIKE LOWER(:keyword)
            """),
            {"keyword": f"%{keyword}%"}
        )
        return [row["name"] for row in result.mappings()]

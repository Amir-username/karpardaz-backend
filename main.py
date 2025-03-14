# username=amirnaji@example.com password=123456789
from fastapi import FastAPI
from .database import create_db_and_tables
from .routes.employer_route import employer_router
from .routes.jobseeker_route import jobseeker_router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(employer_router)
app.include_router(jobseeker_router)

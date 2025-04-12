from fastapi import FastAPI
from .database import create_db_and_tables
from .routes.employer_route import employer_router
from .routes.jobseeker_route import jobseeker_router
from .routes.advertise_route import advertise_router
from .routes.employer_detail_route import employer_detail_router
from .routes.advertise_search_route import search_router
# from .routes.jobseeker_detail_route import jobseeker_detail_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# CORS setup
origins = [
    "https://karpardaz-frontend.vercel.app/",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
    # "https://karpardaz-frontend.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(employer_router)
app.include_router(jobseeker_router)
app.include_router(advertise_router)
app.include_router(employer_detail_router)
app.include_router(search_router)
# app.include_router(jobseeker_detail_router)

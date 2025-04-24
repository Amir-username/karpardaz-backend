from fastapi import FastAPI
from .database import create_db_and_tables, delete_jdetail_table
from .routes.employer_route import employer_router
from .routes.jobseeker_route import jobseeker_router
from .routes.advertise_route import advertise_router
from .routes.employer_detail_route import employer_detail_router
from .routes.advertise_search_route import search_router
from .routes.jobseeker_detail_route import jobseeker_detail_router
from .routes.jobseeker_advertise_route import jobseeker_advertise_router
from .routes.jobseeker_ad_search_route import joseeker_ad_search_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# CORS setup
# origins = [
#     "https://karpardaz-frontend.vercel.app/",
#     "http://localhost:3000",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://karpardaz-frontend.vercel.app/"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # delete_jdetail_table()



app.include_router(employer_router, tags=["Employers"])
app.include_router(employer_detail_router, tags=["Employers Detail"])
app.include_router(advertise_router, tags=["Employer Advertisements"])
app.include_router(search_router, tags=["Search Advertisements"])
app.include_router(jobseeker_router, tags=["Jobseekers"])
app.include_router(jobseeker_detail_router, tags=["Jobseekers Detail"])
app.include_router(jobseeker_advertise_router, tags=[
                   "Jobseeker Advertisements"])
app.include_router(joseeker_ad_search_router, tags=[
                   "Search Jobseeker Advertisements"])

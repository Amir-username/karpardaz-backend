from fastapi import FastAPI
from .database import create_db_and_tables, delete_jdetail_table
from .routes.employer.employer_route import employer_router
from .routes.jobseeker.jobseeker_liked_ads_route import jobseeker_liked_ads_router
from .routes.employer.employer_liked_ads_route import employer_liked_ads_router
from .routes.jobseeker.jobseeker_route import jobseeker_router
from .routes.employer.advertise_route import advertise_router
from .routes.employer.employer_detail_route import employer_detail_router
from .routes.employer.advertise_search_route import search_router
from .routes.jobseeker.jobseeker_detail_route import jobseeker_detail_router
from .routes.jobseeker.jobseeker_advertise_route import jobseeker_advertise_router
from .routes.jobseeker.jobseeker_ad_search_route import joseeker_ad_search_router
from .routes.resume_route import resume_router
from .routes.current_user_route import current_user_router
from .routes.jobseeker.jobseeker_avatar_route import jobseeker_avatar_router
from .routes.employer.employer_avatar_route import employer_avatar_router
from .routes.jobseeker.jobseeker_backdrop_route import jobseeker_backdrop_router
from .routes.employer.employer_backdrop_route import employer_backdrop_router
from .routes.requests.employer_ad_request_route import employer_ad_request_router
from .routes.requests.jobseeker_ad_request_route import jobseeker_ad_request_router
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


app.include_router(employer_router, tags=["Employers"])
app.include_router(employer_detail_router, tags=["Employers Detail"])
app.include_router(advertise_router, tags=["Employer Advertisements"])
app.include_router(search_router, tags=["Search Advertisements"])
app.include_router(jobseeker_router, tags=["Jobseekers"])
app.include_router(jobseeker_liked_ads_router, tags=['Liked Advertisements'])
app.include_router(employer_liked_ads_router, tags=[
                   'Liked Jobseeker Advertisements'])
app.include_router(jobseeker_detail_router, tags=["Jobseekers Detail"])
app.include_router(jobseeker_advertise_router, tags=[
                   "Jobseeker Advertisements"])
app.include_router(joseeker_ad_search_router, tags=[
                   "Search Jobseeker Advertisements"])
app.include_router(resume_router, tags=['Resume'])
app.include_router(jobseeker_avatar_router, tags=['Jobseeker Avatar'])
app.include_router(employer_avatar_router, tags=['Employer Avatar'])
app.include_router(jobseeker_backdrop_router, tags=['Jobseeker Backdrop'])
app.include_router(employer_backdrop_router, tags=['Employer Backdrop'])
app.include_router(current_user_router, tags=['Current User'])
app.include_router(employer_ad_request_router, tags=[
                   'Employer Advertise Request'])
app.include_router(jobseeker_ad_request_router, tags=[
                   'Jobseeker Advertise Request'])

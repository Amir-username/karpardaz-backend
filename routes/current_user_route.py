from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..models.EmployerDetail import EmployerDetail
from ..auth.employer_auth import get_current_employer
from ..auth.jobseeker_auth import get_current_jobseeker
from ..session.session import get_session
from ..models.JobSeekerDetail import JobSeekerDetail


current_user_router = APIRouter()


@current_user_router.get('/current-jobseeker/')
def current_jobseeker(
    jobseeker: JobSeekerDetail = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    result = session.exec(query).first()

    if result:
        return result
    else:
        return jobseeker


@current_user_router.get('/current-employer/')
def current_employer(
    employer: EmployerDetail = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    result = session.exec(query).first()

    if result:
        return result
    else:
        return employer

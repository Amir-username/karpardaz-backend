from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ...models.JobSeekerDetail import JobSeekerDetail, JobSeekerDetailCreate, JobSeekerDetailUpdate
from ...models.JobSeeker import JobSeeker
from ...auth.jobseeker_auth import get_current_jobseeker
from ...session.session import get_session


jobseeker_detail_router = APIRouter()


@jobseeker_detail_router.post('/jobseeker-detail/', response_model=JobSeekerDetail)
def create_jobseeker_detail(
    detail: JobSeekerDetailCreate,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    db = JobSeekerDetail.model_validate(detail)
    db.firstname = jobseeker.firstname
    db.lastname = jobseeker.lastname
    db.jobseeker = jobseeker
    db.jobseeker_id = jobseeker.id

    session.add(db)
    session.commit()
    session.refresh(db)

    return db


@jobseeker_detail_router.get('/jobseeker-detail/{id}', response_model=JobSeekerDetail)
def read_jobseeker_detail(
    id: int,
    session: Session = Depends(get_session)
):
    query = select(JobSeekerDetail).where(JobSeekerDetail.id == id)
    result = session.exec(query).first()

    print(result)

    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@jobseeker_detail_router.patch('/jobseeker-detail/{id}', response_model=JobSeekerDetail)
def update_jobseeker_detail(
    id: int,
    jobseeker_update: JobSeekerDetailUpdate,
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    query = select(JobSeekerDetail).where(JobSeekerDetail.id == id)
    result = session.exec(query).first()

    if (result.jobseeker_id == jobseeker.id):
        update_data = jobseeker_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        session.add(result)
        session.commit()
        session.refresh(result)

    return result


@jobseeker_detail_router.delete('/jobseeker-detail/{id}')
def update_jobseeker_detail(
    id: int,
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    query = select(JobSeekerDetail).where(JobSeekerDetail.id == id)
    result = session.exec(query).first()

    if (jobseeker.id == result.jobseeker_id):
        session.delete(result)
        session.commit()

        return 'deleted jobseeker detail'

    return None

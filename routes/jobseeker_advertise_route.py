from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, desc
from ..models.JobSeekerAd import JobSeekerAd, JobSeekerAdCreate, JobSeekrAdUpdate
from ..models.JobSeeker import JobSeeker
from ..models.JobSeekerDetail import JobSeekerDetail
from ..auth.jobseeker_auth import get_current_jobseeker
from ..session.session import get_session


jobseeker_advertise_router = APIRouter()


def get_jobseeker_ad_or_404(
    id: int,
    session: Session = Depends(get_session),
    jobseeker_id: int | None = None
) -> JobSeekerAd:
    query = select(JobSeekerAd).where(JobSeekerAd.id == id)
    if jobseeker_id:
        query = query.where(JobSeekerAd.jobseeker_id == jobseeker_id)

    advertisement = session.exec(query).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )
    return advertisement


@jobseeker_advertise_router.post("/jobseeker-ads/", response_model=JobSeekerAd)
def create_jobseeker_ad(
    advertisement: JobSeekerAdCreate,
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    result = session.exec(query).first()

    ad = JobSeekerAd(
        firstname=result.firstname,
        lastname=result.lastname,
        title=advertisement.title,
        position=result.position,
        experience=result.experience,
        salary=result.salary,
        job_group=result.job_group,
        is_remote=result.is_remote,
        is_internship=result.is_internship,
        gender=result.gender,
        technologies=result.technologies,
        is_portfolio=result.is_portfolio,
        description=advertisement.description,
        jobseeker_id=result.jobseeker_id,
        jobseeker=result,
    )

    db_advertisement = JobSeekerAd.model_validate(ad)
    # db_advertisement.jobseeker_id = result.jobseeker_id
    # db_advertisement.jobseeker = result.jobseeker
    session.add(db_advertisement)
    session.commit()
    session.refresh(db_advertisement)
    return db_advertisement


@jobseeker_advertise_router.get("/jobseeker-ads/", response_model=list[JobSeekerAd])
def read_jobseeker_ads(session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    statement = select(JobSeekerAd).order_by(
        desc(JobSeekerAd.id)).offset(offset).limit(limit)
    results = session.exec(statement).all()
    return results


@jobseeker_advertise_router.get("/jobseeker-own-ads/{jobseeker_id}", response_model=list[JobSeekerAd])
def read_jobseeker_ads(jobseeker_id, session: Session = Depends(get_session)):
    statement = select(JobSeekerAd).order_by(
        desc(JobSeekerAd.id)).where(JobSeekerAd.jobseeker_id == jobseeker_id)
    results = session.exec(statement).all()
    return results


@jobseeker_advertise_router.get("/jobseeker-ads/{ad_id}", response_model=JobSeekerAd)
def read_jobseeker_ad(ad_id: int, session: Session = Depends(get_session)):
    advertisement = session.get(JobSeekerAd, ad_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@jobseeker_advertise_router.get("/my-jobseeker-ads/", response_model=list[JobSeekerAd])
def read_my_jobseeker_ad(
    current_jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    query = select(JobSeekerAd).where(
        JobSeekerAd.jobseeker_id == current_jobseeker.id)
    advertisements = session.exec(query).all()
    return advertisements


@jobseeker_advertise_router.patch("/jobseeker-ads/{id}", response_model=JobSeekerAd)
def update_jobseeker_ad(
    id: int,
    advertisement: JobSeekrAdUpdate,
    session: Session = Depends(get_session),
    current_jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    db_advertisement = get_jobseeker_ad_or_404(
        id, session, current_jobseeker.id)

    update_data = advertisement.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_advertisement, key, value)

    session.add(db_advertisement)
    session.commit()
    session.refresh(db_advertisement)

    return db_advertisement


@jobseeker_advertise_router.delete("/jobseeker-ads/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jobseeker_ad(
    id: int,
    session: Session = Depends(get_session),
    current_jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    advertisement = get_jobseeker_ad_or_404(id, session, current_jobseeker.id)

    session.delete(advertisement)
    session.commit()

    return None

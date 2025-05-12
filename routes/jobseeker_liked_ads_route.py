from fastapi import APIRouter, Depends, HTTPException
from ..auth.jobseeker_auth import get_current_jobseeker
from ..models.JobSeeker import JobSeeker
from sqlmodel import Session, select
from ..session.session import get_session
from ..models.JobSeekerDetail import JobSeekerDetail
from ..models.Advertise import Advertise

jobseeker_liked_ads_router = APIRouter()


@jobseeker_liked_ads_router.get('/jobseeker-like-ad/{advertise_id}')
def advertise_like(
    advertise_id: int,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_detail = session.exec(query).first()

    if jobseeker_detail:
        liked_advertise = session.get(Advertise, advertise_id)
        if liked_advertise:
            jobseeker_detail.liked_advertisements.append(liked_advertise)
            session.add(jobseeker_detail)
            session.commit()
            session.refresh(jobseeker_detail)

            return jobseeker_detail.liked_advertisements
    else:
        raise HTTPException(404, 'jobseeker detail not found')

    return None


@jobseeker_liked_ads_router.get('/jobseeker-dislike-ad/{advertise_id}')
def advertise_dislike(
    advertise_id: int,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_detail = session.exec(query).first()

    if jobseeker_detail:
        liked_advertise = session.get(Advertise, advertise_id)
        if liked_advertise:
            jobseeker_detail.liked_advertisements.remove(liked_advertise)
            session.add(jobseeker_detail)
            session.commit()
            session.refresh(jobseeker_detail)

            return jobseeker_detail.liked_advertisements
    else:
        raise HTTPException(404, 'jobseeker detail not found')

    return None


@jobseeker_liked_ads_router.get('/jobseeker-favorites/')
def jobseeker_favorites(
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    jobseeker_detail_query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_detail = session.exec(jobseeker_detail_query).first()

    if not jobseeker_detail:
        raise HTTPException(404, 'jobseeker detail not found')

    favorites = jobseeker_detail.liked_advertisements

    return favorites

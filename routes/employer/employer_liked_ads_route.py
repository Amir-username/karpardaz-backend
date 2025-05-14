from fastapi import APIRouter, Depends, HTTPException
from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from sqlmodel import Session, select
from ...session.session import get_session
from ...models.EmployerDetail import EmployerDetail
from ...models.JobSeekerAd import JobSeekerAd

employer_liked_ads_router = APIRouter()


@employer_liked_ads_router.get('/employer-like-ad/{advertise_id}')
def advertise_like(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    employer_detail = session.exec(query).first()

    if employer_detail:
        liked_advertise = session.get(JobSeekerAd, advertise_id)
        if liked_advertise:
            employer_detail.liked_jobseeker_ads.append(liked_advertise)
            session.add(employer_detail)
            session.commit()
            session.refresh(employer_detail)

            return employer_detail.liked_jobseeker_ads
    else:
        raise HTTPException(404, 'employer detail not found')

    return None


@employer_liked_ads_router.get('/employer-dislike-ad/{advertise_id}')
def advertise_dislike(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    employer_detail = session.exec(query).first()

    if employer_detail:
        liked_advertise = session.get(JobSeekerAd, advertise_id)
        if liked_advertise:
            employer_detail.liked_jobseeker_ads.remove(liked_advertise)
            session.add(employer_detail)
            session.commit()
            session.refresh(employer_detail)

            return employer_detail.liked_jobseeker_ads
    else:
        raise HTTPException(404, 'employer detail not found')

    return None


@employer_liked_ads_router.get('/employer-favorites/')
def employer_favorites(
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    employer_detail_query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    employer_detail = session.exec(employer_detail_query).first()

    if not employer_detail:
        raise HTTPException(404, 'employer detail not found')

    favorites = employer_detail.liked_jobseeker_ads

    ids = (fav.id for fav in favorites)

    return ids

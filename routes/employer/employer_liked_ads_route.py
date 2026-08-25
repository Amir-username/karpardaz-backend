from fastapi import APIRouter, Depends

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from sqlmodel import Session
from ...session.session import get_session
from ...logic.employer_logic import like_ad, dislike_ad, get_favorites

employer_liked_ads_router = APIRouter()


@employer_liked_ads_router.get('/employer-like-ad/{advertise_id}')
def advertise_like(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return like_ad(session, advertise_id, employer)


@employer_liked_ads_router.get('/employer-dislike-ad/{advertise_id}')
def advertise_dislike(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return dislike_ad(session, advertise_id, employer)


@employer_liked_ads_router.get('/employer-favorites/')
def employer_favorites(
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return get_favorites(session, employer)


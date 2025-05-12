from fastapi import APIRouter, Depends, Query
from ...session.session import get_session
from ...models.JobSeekerAd import JobSeekerAd
from sqlmodel import Session, select, or_, desc


joseeker_ad_search_router = APIRouter()


@joseeker_ad_search_router.get('/jobeeker-ads/search/', response_model=list[JobSeekerAd])
def search_jobseeker_advertises(
    session: Session = Depends(get_session),
    q: str | None = Query(None, min_length=2)
):
    query = select(JobSeekerAd).order_by(
        desc(JobSeekerAd.id))
    if q:
        query = select(JobSeekerAd).filter(
            or_(
                JobSeekerAd.title.ilike(f"%{q}%"),
                JobSeekerAd.description.ilike(f"%{q}%")
            )
        ).order_by(
            desc(JobSeekerAd.id))

    result = session.exec(query).all()

    return result

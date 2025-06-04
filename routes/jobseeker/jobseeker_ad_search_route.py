from fastapi import APIRouter, Depends, Query
from ...session.session import get_session
from ...models.JobSeekerAd import JobSeekerAd
from ...models.JobSeekerDetail import JobSeekerDetail
from sqlmodel import Session, select, or_, desc
from ...Enums.experience_enum import ExperienceEnum
from ...Enums.gender_enum import GenderEnum
from ...Enums.position_enum import PositionEnum
from ...Enums.salary_enum import SalaryEnum


joseeker_ad_search_router = APIRouter()


@joseeker_ad_search_router.get('/jobseeker-ads/search/', response_model=list[JobSeekerAd])
def search_jobseeker_advertises(
    session: Session = Depends(get_session),
    search_q: str | None = Query(None, min_length=2),
    is_internship: bool | None = Query(
        None),
    is_remote: bool | None = Query(
        None),
    is_portfolio: bool | None = Query(
        None),
    experience: ExperienceEnum | None = Query(None),
    salary: SalaryEnum | None = Query(None),
    gender: GenderEnum | None = Query(None),
    position: PositionEnum | None = Query(None),
    offset: int = 0,
    limit: int = 10
):
    filters = []

    if search_q:
        filters.append(
            or_(
                JobSeekerAd.title.ilike(f"%{search_q}%"),
                JobSeekerAd.description.ilike(f"%{search_q}%"),
            )
        ).order_by(
            desc(JobSeekerAd.id))

    if is_internship is not None:
        filters.append(JobSeekerAd.is_internship == is_internship)
    if is_remote is not None:
        filters.append(JobSeekerAd.is_remote == is_remote)
    if is_portfolio is not None:
        filters.append(JobSeekerAd.is_portfolio == is_portfolio)

    if experience is not None:
        filters.append(JobSeekerAd.experience == experience)
    if salary is not None:
        filters.append(JobSeekerAd.salary == salary)
    if gender is not None:
        filters.append(JobSeekerAd.gender == gender)
    if position is not None:
        filters.append(JobSeekerAd.position == position)

    filter_query = select(JobSeekerAd).where(
        *filters).order_by(desc(JobSeekerAd.id)).offset(offset=offset).limit(limit=limit)
    result = session.exec(filter_query).all()

    return result

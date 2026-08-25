from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ...session.session import get_session
from ...logic.employer_logic import search_ads
from ...Enums.experience_enum import ExperienceEnum
from ...Enums.salary_enum import SalaryEnum
from ...Enums.gender_enum import GenderEnum
from ...Enums.position_enum import PositionEnum

search_router = APIRouter()


@search_router.get('/jobs/search/')
def search_advertises(
    session: Session = Depends(get_session),
    search_q: str | None = Query(None, min_length=2),
    city_q: str | None = Query(None, min_length=2),
    is_internship: bool | None = Query(None),
    is_remote: bool | None = Query(None),
    is_portfolio: bool | None = Query(None),
    experience: ExperienceEnum | None = Query(None),
    salary: SalaryEnum | None = Query(None),
    gender: GenderEnum | None = Query(None),
    position: PositionEnum | None = Query(None),
    offset: int = 0,
    limit: int = 10
):
    return search_ads(
        session,
        search_q=search_q, city_q=city_q,
        is_internship=is_internship, is_remote=is_remote, is_portfolio=is_portfolio,
        experience=experience, salary=salary, gender=gender, position=position,
        offset=offset, limit=limit,
    )


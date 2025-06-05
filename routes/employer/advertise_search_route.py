from fastapi import APIRouter, Depends, Query
from ...session.session import get_session
from ...models.Advertise import Advertise, AdvertisePublic
from sqlmodel import Session, select, or_, desc, func
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
                Advertise.title.ilike(f"%{search_q}%"),
                Advertise.description.ilike(f"%{search_q}%"),
                Advertise.employer.has(company_name=search_q),
            )
        )
    if city_q:
        filters.append(Advertise.city.ilike(f"%{city_q}%"))

    if is_internship is not None:
        filters.append(Advertise.is_internship == is_internship)
    if is_remote is not None:
        filters.append(Advertise.is_remote == is_remote)
    if is_portfolio is not None:
        filters.append(Advertise.is_portfolio == is_portfolio)

    if experience is not None:
        filters.append(Advertise.experience == experience)
    if salary is not None:
        filters.append(Advertise.salary == salary)
    if gender is not None:
        filters.append(Advertise.gender == gender)
    if position is not None:
        filters.append(Advertise.position == position)

    total_items = session.exec(
        select(func.count()).select_from(Advertise)).one()
    total_pages = (total_items + limit - 1) // limit

    filter_query = select(Advertise).where(
        *filters).order_by(desc(Advertise.id)).offset(offset=offset).limit(limit=limit)
    result = session.exec(filter_query).all()

    response = {
        'total_pages': total_pages,
        'advertises': result
    }
    return response

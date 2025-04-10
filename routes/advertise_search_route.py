from fastapi import APIRouter, Depends, Query
from ..session.session import get_session
from ..models.Advertise import Advertise, AdvertisePublic
from sqlmodel import Session, select, or_


search_router = APIRouter()


@search_router.get('/jobs/search/', response_model=list[AdvertisePublic])
def search_advertises(
    session: Session = Depends(get_session),
    q: str | None = Query(None, min_length=2)
):
    query = select(Advertise)
    if q:
        query = select(Advertise).filter(
            or_(
                Advertise.title.ilike(f"%{q}%"),
                Advertise.description.ilike(f"%{q}%")
            )
        )

    result = session.exec(query).all()

    return result

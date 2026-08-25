
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from ...models.Advertise import AdvertiseCreate, AdvertisePublic, AdvertiseUpdate
from ...session.session import get_session
from ...logic.employer_logic import (
    create_ad,
    get_ads_list,
    get_ads_by_employer,
    get_ad,
    get_my_ads,
    update_ad,
    remove_ad,
)

advertise_router = APIRouter()


@advertise_router.post("/advertisements/", response_model=AdvertisePublic)
def create_advertisement(
    advertisement: AdvertiseCreate,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    return create_ad(session, advertisement, employer)


@advertise_router.get("/advertisements/")
def read_advertisements(session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    return get_ads_list(session, offset, limit)


@advertise_router.get("/employer-ads/{employer_id}", response_model=list[AdvertisePublic])
def read_advertisements_by_employer(employer_id: int, session: Session = Depends(get_session)):
    return get_ads_by_employer(session, employer_id)


@advertise_router.get("/advertisements/{advertisement_id}", response_model=AdvertisePublic)
def read_advertisement(advertisement_id: int, session: Session = Depends(get_session)):
    return get_ad(session, advertisement_id)


@advertise_router.get("/my-advertisements/", response_model=list[AdvertisePublic])
def read_my_advertisements(
    current_employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return get_my_ads(session, current_employer)


@advertise_router.patch("/advertisements/{id}", response_model=AdvertisePublic)
def update_advertisement(
    id: int,
    advertisement: AdvertiseUpdate,
    session: Session = Depends(get_session),
    current_employer: Employer = Depends(get_current_employer)
):
    return update_ad(session, id, advertisement, current_employer)


@advertise_router.delete("/advertisements/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(
    id: int,
    session: Session = Depends(get_session),
    current_employer: Employer = Depends(get_current_employer)
):
    return remove_ad(session, id, current_employer)


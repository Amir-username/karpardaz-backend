from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, desc, func
from ...models.Advertise import Advertise, AdvertiseCreate, AdvertisePublic, AdvertiseUpdate, GenderEnum, PositionEnum
from ...models.Employer import Employer
from ...models.EmployerDetail import EmployerDetail
from ...auth.employer_auth import get_current_employer
from ...session.session import get_session


advertise_router = APIRouter()


def get_advertisement_or_404(
    id: int,
    session: Session = Depends(get_session),
    employer_id: int | None = None
) -> Advertise:
    query = select(Advertise).where(Advertise.id == id)
    if employer_id:
        query = query.where(Advertise.employer_id == employer_id)

    advertisement = session.exec(query).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )
    return advertisement


@advertise_router.post("/advertisements/", response_model=AdvertisePublic)
def create_advertisement(
    advertisement: AdvertiseCreate,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    result = session.exec(query).first()

    ad = Advertise(
        title=advertisement.title,
        position=advertisement.position,
        experience=advertisement.experience,
        salary=advertisement.salary,
        job_group=advertisement.job_group,
        is_remote=advertisement.is_remote,
        city=advertisement.city,
        is_internship=advertisement.is_internship,
        gender=advertisement.gender,
        benefits=advertisement.benefits,
        technologies=advertisement.technologies,
        is_portfolio=advertisement.is_portfolio,
        description=advertisement.description,
        employer_id=result.id,
        employer=result

    )
    db_advertisement = Advertise.model_validate(ad)
    session.add(db_advertisement)
    session.commit()
    session.refresh(db_advertisement)
    return db_advertisement


@advertise_router.get("/advertisements/")
def read_advertisements(session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    total_items = session.exec(
        select(func.count()).select_from(Advertise)).one()
    total_pages = (total_items + limit - 1) // limit

    
    statement = select(Advertise).order_by(
        desc(Advertise.id)).offset(offset).limit(limit)
    results = session.exec(statement).all()

    response = {
        'total_pages': total_pages,
        'advertises': results
    }
    return response


@advertise_router.get("/employer-ads/{employer_id}", response_model=list[AdvertisePublic])
def read_advertisements_by_employer(employer_id: int, session: Session = Depends(get_session)):
    statement = select(Advertise).order_by(
        desc(Advertise.id)).where(Advertise.employer_id == employer_id)
    results = session.exec(statement).all()
    return results


@advertise_router.get("/advertisements/{advertisement_id}", response_model=AdvertisePublic)
def read_advertisement(advertisement_id: int, session: Session = Depends(get_session)):
    advertisement = session.get(Advertise, advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@advertise_router.get("/my-advertisements/", response_model=list[AdvertisePublic])
def read_my_advertisements(
    current_employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(Advertise).where(
        Advertise.employer_id == current_employer.id)
    advertisements = session.exec(query).all()
    return advertisements


@advertise_router.patch("/advertisements/{id}", response_model=AdvertisePublic)
def update_advertisement(
    id: int,
    advertisement: AdvertiseUpdate,
    session: Session = Depends(get_session),
    current_employer: Employer = Depends(get_current_employer)
):
    db_advertisement = get_advertisement_or_404(
        id, session, current_employer.id)

    update_data = advertisement.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_advertisement, key, value)

    session.add(db_advertisement)
    session.commit()
    session.refresh(db_advertisement)

    return db_advertisement


@advertise_router.delete("/advertisements/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(
    id: int,
    session: Session = Depends(get_session),
    current_employer: Employer = Depends(get_current_employer)
):
    advertisement = get_advertisement_or_404(id, session, current_employer.id)

    session.delete(advertisement)
    session.commit()

    return None

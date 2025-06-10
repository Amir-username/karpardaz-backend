from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ...models.Employer import Employer
from ...models.EmployerDetail import EmployerDetail, EmployerDetailCreate, EmployerDetailUpdate
from ...auth.employer_auth import get_current_employer
from ...session.session import get_session


employer_detail_router = APIRouter()


@employer_detail_router.post('/employer-detail/', response_model=EmployerDetail)
def create_employer_detail(
    detail: EmployerDetailCreate,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    db = EmployerDetail.model_validate(detail)
    db.employer = employer
    db.employer_id = employer.id
    db.company_name = employer.company_name

    session.add(db)
    session.commit()
    session.refresh(db)

    return db


@employer_detail_router.get('/employer-detail/{id}', response_model=EmployerDetail)
def read_employer_detail(id: int, session: Session = Depends(get_session)):
    query = select(EmployerDetail).where(EmployerDetail.id == id)
    result = session.exec(query).first()

    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@employer_detail_router.get('/employer-details/', response_model=list[EmployerDetail])
def read_all_employers(session: Session = Depends(get_session)):
    query = select(EmployerDetail)
    result = session.exec(query).all()

    return result


@employer_detail_router.patch('/employer-detail/{id}', response_model=EmployerDetail)
def update_employer_detail(
    id: int,
    employer_update: EmployerDetailUpdate,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    query = select(EmployerDetail).where(EmployerDetail.id == id)
    result = session.exec(query).first()

    if (result.employer_id == employer.id):
        update_data = employer_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        session.add(result)
        session.commit()
        session.refresh(result)

    return result


@employer_detail_router.delete('/employer-detail/{id}')
def delete_employer_detail(
    id: int,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    query = select(EmployerDetail).where(EmployerDetail.id == id)
    result = session.exec(query).first()

    if (employer.id == result.employer_id):
        session.delete(result)
        session.commit()

        return 'deleted employer detail'

    return None

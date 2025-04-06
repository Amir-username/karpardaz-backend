from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, desc
from ..models.Employer import Employer
from ..models.EmployerDetail import EmployerDetail
from ..auth.employer_auth import get_current_employer
from ..session.session import get_session


employer_detail_router = APIRouter()


@employer_detail_router.post('/employer-detail/', response_model=EmployerDetail)
def create_employer_detail(
    detail: EmployerDetail,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    db = EmployerDetail.model_validate(detail)
    db.employer = employer
    db.employer_id = employer.id

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


@employer_detail_router.patch('/employer-detail/')
def update_employer_detail():
    pass


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

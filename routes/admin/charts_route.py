from fastapi import APIRouter, Depends
from ...models.JobSeekerDetail import JobSeekerDetail
from ...models.Advertise import Advertise
from sqlmodel import Session, select
from ...session.session import get_session
from ...Enums.gender_enum import GenderEnum
from ...Enums.salary_enum import SalaryEnum

chart_router = APIRouter()


@chart_router.get('/charts/gender')
def get_gender_chart(
    session: Session = Depends(get_session)
):
    male_query = select(JobSeekerDetail).where(
        JobSeekerDetail.gender == GenderEnum.MALE)
    male_result = session.exec(male_query).all()

    female_query = select(JobSeekerDetail).where(
        JobSeekerDetail.gender == GenderEnum.FEMALE)
    female_result = session.exec(female_query).all()

    return {
        'title': 'gender',
        'male': len(male_result),
        'female': len(female_result)
    }


@chart_router.get('/charts/employer-salary')
def get_employer_salary_chart(
    session: Session = Depends(get_session)
):
    intern = session.exec(select(Advertise).where(
        Advertise.salary == SalaryEnum.INTERN)).all()
    junior = session.exec(select(Advertise).where(
        Advertise.salary == SalaryEnum.JUNIOR)).all()
    midlevel = session.exec(select(Advertise).where(
        Advertise.salary == SalaryEnum.MIDLEVEL)).all()
    senior = session.exec(select(Advertise).where(
        Advertise.salary == SalaryEnum.SENIOR)).all()
    neg = session.exec(select(Advertise).where(
        Advertise.salary == SalaryEnum.NEGOTIATED)).all()

    return {
        'title': 'advertise salary',
        'intern': len(intern),
        'junior': len(junior),
        'midlevel': len(midlevel),
        'senior': len(senior),
        'neg': len(neg)
    }

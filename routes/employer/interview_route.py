
from fastapi import APIRouter, Depends
from sqlmodel import Session

from ...auth.employer_auth import get_current_employer
from ...auth.jobseeker_auth import get_current_jobseeker
from ...models.Employer import Employer
from ...models.JobSeeker import JobSeeker
from ...session.session import get_session
from ...logic.employer_logic import (
    create_interview_logic,
    add_interview_answers_logic,
    get_interview_logic,
    remove_interview,
)

interview_router = APIRouter()


@interview_router.post('/create-interview/')
def create_interview(
    advertise_id: int,
    questions: list[str],
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return create_interview_logic(session, advertise_id, questions, employer)


@interview_router.post('/create-answers/{interview_id}')
def create_answers(
    interview_id: int,
    user_answers: list[str],
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    return add_interview_answers_logic(session, interview_id, user_answers, jobseeker)


@interview_router.get('/get-interview/{advertise_id}')
def get_interview(advertise_id: int, session: Session = Depends(get_session)):
    return get_interview_logic(session, advertise_id)


@interview_router.delete('/delete-interview/{advertise_id}')
def delete_interview(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return remove_interview(session, advertise_id, employer)


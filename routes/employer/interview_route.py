from ...session.session import get_session
from ...models.Employer import Employer
from ...models.JobSeeker import JobSeeker
from ...models.Interview import Interview
from ...models.Advertise import Advertise
from fastapi import APIRouter, Depends, HTTPException
from ...auth.employer_auth import get_current_employer
from ...auth.jobseeker_auth import get_current_jobseeker
from sqlmodel import Session, select


interview_router = APIRouter()


@interview_router.post('/create-interview/')
def create_interview(
    advertise_id: int,
    questions: list[str],
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    advertise = session.get(Advertise, advertise_id)
    if not advertise:
        raise HTTPException(status_code=404, detail="Advertise not found")

    if advertise.employer_id == employer.id:
        interview = Interview(
            questions=questions,
            advertise_id=advertise_id,
            advertise=advertise,
        )

        advertise.interview = interview

        session.add_all([interview, advertise])
        session.commit()
        session.refresh(interview)
        session.refresh(advertise)

        return interview


@interview_router.post('/create-answers/{interview_id}')
def create_answers(
    interview_id: int,
    user_answers: list[str],
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    interview = session.get(Interview, interview_id)
    if interview:
        db_answer = {
            'jobseeker_id': jobseeker.id,
            'answers': user_answers
        }

        for ans in interview.answers:
            if ans.get('jobseeker_id') == jobseeker.id:
                return interview

        interview.answers = interview.answers + [db_answer]
        interview.jobseeker_ids = interview.jobseeker_ids + [jobseeker.id]

        session.add(interview)
        session.commit()
        session.refresh(interview)

        return interview


@interview_router.get('/get-interview/{advertise_id}')
def get_interview(
    advertise_id: int,
    session: Session = Depends(get_session)
):
    advertise = session.get(Advertise, advertise_id)
    if not advertise:
        raise HTTPException(404, 'Advertise not found')
    interview = session.exec(select(Interview).where(
        Interview.advertise_id == advertise_id)).first()
    if not interview:
        raise HTTPException(404, 'Interview not found')
    
    return interview


@interview_router.delete('/delete-interview/{advertise_id}')
def delete_interview(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    advertise = session.get(Advertise, advertise_id)

    if not advertise:
        raise HTTPException(404, 'Advertise not found')

    query = select(Interview).where(Interview.advertise_id == advertise_id)
    result = session.exec(query).first()

    if not result:
        raise HTTPException(404, 'Interview not found')

    if employer.id == advertise.employer_id:
        session.delete(result)
        session.commit()
    else:
        raise HTTPException(401, 'You dont have permision for that')

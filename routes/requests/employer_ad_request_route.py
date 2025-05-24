from fastapi import APIRouter, Depends, HTTPException
from ...models.JobSeeker import JobSeeker
from ...auth.jobseeker_auth import get_current_jobseeker
from ...models.JobSeekerDetail import JobSeekerDetail
from ...models.AdRequest import AdRequest
from ...models.Advertise import Advertise
from ...session.session import Session, get_session
from ...Enums.status_enum import StatusEnum
from sqlmodel import select


employer_ad_request_router = APIRouter()


@employer_ad_request_router.post('/ad-request/')
def employer_ad_request(
    advertise_id: int,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    result = session.exec(query).first()

    advertise_query = select(Advertise).where(Advertise.id == advertise_id)
    advertise = session.exec(advertise_query).first()

    if not advertise:
        raise HTTPException(404, 'advertise not found')

    if result:
        ad_request = AdRequest(
            jobseeker=result,
            jobseeker_id=result.id,
            advertise=advertise,
            advertise_id=advertise.id,
            status=StatusEnum.PENDING
        )

        session.add(ad_request)
        session.commit()
        session.refresh(ad_request)

        return ad_request
    
    raise HTTPException(404, 'jobseeker detail not found')

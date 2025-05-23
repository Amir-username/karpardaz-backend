from fastapi import APIRouter, Depends
from ...models.JobSeeker import JobSeeker
from ...auth.jobseeker_auth import get_current_jobseeker
from ...models.JobSeekerDetail import JobSeekerDetail
from ...models.AdRequest import AdRequest
from ...models.Advertise import Advertise
from ...session.session import Session, get_session
from ...Enums.status_enum import StatusEnum


employer_ad_request_router = APIRouter()


@employer_ad_request_router.post('/ad-request/')
def employer_ad_request(
    advertise: Advertise,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    advertise_model = Advertise.model_validate(advertise)
    ad_request = AdRequest(
        jobseeker=jobseeker,
        jobseeker_id=jobseeker.id,
        advertise=advertise_model,
        advertise_id=advertise_model.id,
        status=StatusEnum.PENDING
    )

    session.add(ad_request)
    session.commit()
    session.refresh(ad_request)

    return ad_request

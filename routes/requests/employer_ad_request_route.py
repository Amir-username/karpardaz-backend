from fastapi import APIRouter, Depends, HTTPException
from ...models.JobSeeker import JobSeeker
from ...auth.jobseeker_auth import get_current_jobseeker
from ...auth.employer_auth import get_current_employer
from ...models.JobSeekerDetail import JobSeekerDetail
from ...models.AdRequest import AdRequest
from ...models.Advertise import Advertise
from ...models.Employer import Employer
from ...session.session import Session, get_session
from ...Enums.status_enum import StatusEnum
from sqlmodel import select, and_


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


@employer_ad_request_router.get('/get-jobseeker-requests/')
def get_jobseeker_requests(
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session),
    # offset: int = 0,
    # limit: int = 10
):
    jobseeker_query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_result = session.exec(jobseeker_query).first()

    if not jobseeker_result:
        raise HTTPException(404, 'jobseeker detail not found')

    requests = jobseeker_result.requests

    return requests


@employer_ad_request_router.get('/get-adrequest-jobseekers/{advertise_id}')
def get_ad_request_jobseekers(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    advertise = session.get(Advertise, advertise_id)
    jobseekers: list[JobSeekerDetail] = []

    for request in advertise.requests:
        jobseekers.append(request.jobseeker)

    return jobseekers


@employer_ad_request_router.post('/change-request-status/')
def change_request_status(
    request_id: int,
    status: StatusEnum,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    request = session.get(AdRequest, request_id)
    if not request:
        raise HTTPException(404, 'request detail not found')

    if request.advertise.employer_id == employer.id:
        request.status = status
        session.add(request)
        session.commit()
        session.refresh(request)


@employer_ad_request_router.get('/advertise-requests/{advertise_id}')
def get_advertise_request(
    advertise_id: int,
    session: Session = Depends(get_session)
):
    query = select(AdRequest).where(AdRequest.advertise_id == advertise_id)
    requests = session.exec(query).all()

    if not requests:
        raise HTTPException(404, 'requests not found')

    return requests


@employer_ad_request_router.get('/get-request-status/{jobseeker_id}')
def get_request_status(
    jobseeker_id: int,
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(AdRequest).where(
        and_(AdRequest.jobseeker_id ==
             jobseeker_id, AdRequest.advertise_id == advertise_id)
    )

    request = session.exec(query).first()

    if request:
        return request.status

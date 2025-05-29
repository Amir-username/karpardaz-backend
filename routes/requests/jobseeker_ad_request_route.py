from fastapi import APIRouter, Depends, HTTPException
from ...models.JobSeeker import JobSeeker
from ...auth.jobseeker_auth import get_current_jobseeker
from ...auth.employer_auth import get_current_employer
from ...models.EmployerDetail import EmployerDetail
from ...models.JobSeekerAdRequest import JobSeekerAdRequest
from ...models.JobSeekerAd import JobSeekerAd
from ...models.Employer import Employer
from ...session.session import Session, get_session
from ...Enums.status_enum import StatusEnum
from sqlmodel import select


jobseeker_ad_request_router = APIRouter()


@jobseeker_ad_request_router.post('/jobseeker-ad-request/')
def jobseeker_ad_request(
    advertise_id: int,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    result = session.exec(query).first()

    advertise_query = select(JobSeekerAd).where(JobSeekerAd.id == advertise_id)
    advertise = session.exec(advertise_query).first()

    if not advertise:
        raise HTTPException(404, 'advertise not found')

    if result:
        ad_request = JobSeekerAdRequest(
            employer=result,
            employer_id=result.id,
            advertise=advertise,
            advertise_id=advertise.id,
            status=StatusEnum.PENDING
        )

        session.add(ad_request)
        session.commit()
        session.refresh(ad_request)

        return ad_request

    raise HTTPException(404, 'employer detail not found')


@jobseeker_ad_request_router.get('/get-employer-requests/')
def get_employer_requests(
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session),
):
    employer_query = select(EmployerDetail).where(
        EmployerDetail.employer_id == employer.id)
    employer_result = session.exec(employer_query).first()

    if not employer_result:
        raise HTTPException(404, 'employer detail not found')

    return employer_result.requests


@jobseeker_ad_request_router.get('/get-adrequest-employers/{advertise_id}')
def get_ad_request_jobseekers(
    advertise_id: int,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    advertise = session.get(JobSeekerAd, advertise_id)
    employers: list[EmployerDetail] = []

    for request in advertise.requests:
        employers.append(request.employer)

    return employers


@jobseeker_ad_request_router.patch('/change-jobseeker-request-status/')
def change_request_status(
    request_id: int,
    status: StatusEnum,
    jobseeker: JobSeeker = Depends(get_current_jobseeker),
    session: Session = Depends(get_session)
):
    request = session.get(JobSeekerAdRequest, request_id)
    if not request:
        raise HTTPException(404, 'request detail not found')

    if request.advertise.jobseeker_id == jobseeker.id:
        request.status = status
        session.add(request)
        session.commit()
        session.refresh(request)


@jobseeker_ad_request_router.get('/jobseeker-ads-requests/{advertise_id}')
def get_advertise_request(
    advertise_id: int,
    session: Session = Depends(get_session)
):
    query = select(JobSeekerAdRequest).where(
        JobSeekerAdRequest.advertise_id == advertise_id)
    requests = session.exec(query).all()

    if not requests:
        raise HTTPException(404, 'requests not found')

    return requests

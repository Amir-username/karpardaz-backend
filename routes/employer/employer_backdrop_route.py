from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from ...session.session import get_session
from ...logic.employer_logic import upload_backdrop, get_backdrop, get_backdrop_by_employer_id

employer_backdrop_router = APIRouter()


@employer_backdrop_router.post('/employer-backdrop/upload/')
async def upload_backdrop_endpoint(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    return await upload_backdrop(session, file, employer)


@employer_backdrop_router.get("/employer-backdrop/{backdrop_id}")
async def get_backdrop_endpoint(backdrop_id: int, session: Session = Depends(get_session)):
    return get_backdrop(session, backdrop_id)


@employer_backdrop_router.get("/get-employer-backdrop/{employer_id}")
async def get_backdrop_by_employer(employer_id: int, session: Session = Depends(get_session)):
    return get_backdrop_by_employer_id(session, employer_id)


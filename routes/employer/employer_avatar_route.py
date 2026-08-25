from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from ...session.session import get_session
from ...logic.employer_logic import upload_avatar, get_avatar, get_avatar_by_employer_id

employer_avatar_router = APIRouter()


@employer_avatar_router.post('/employer-avatar/upload/')
async def upload_avatar_endpoint(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    return await upload_avatar(session, file, employer)


@employer_avatar_router.get("/employer-avatar/{avatar_id}")
async def get_avatar_endpoint(avatar_id: int, session: Session = Depends(get_session)):
    return get_avatar(session, avatar_id)


@employer_avatar_router.get('/get-employer-avatar/{employer_id}')
def get_current_employer_avatar(employer_id: int, session: Session = Depends(get_session)):
    return get_avatar_by_employer_id(session, employer_id)


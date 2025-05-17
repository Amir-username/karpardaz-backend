from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlmodel import Session, select
from ...auth.employer_auth import get_current_employer
from ...models.EmployerAvatar import EmployerAvatar
from ...models.Employer import Employer
from ...models.EmployerDetail import EmployerDetail
from ...session.session import get_session


employer_avatar_router = APIRouter()


@employer_avatar_router.post('/employer-avatar/upload/')
async def upload_avatar(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:  # 2MB limit
        raise HTTPException(400, "File too large (max 2MB)")

    employer_detail = session.exec(
        select(EmployerDetail).where(
            EmployerDetail.employer_id == employer.id)
    ).first()
    if not employer_detail:
        raise HTTPException(404, "User detail not found")

    avatar_record = EmployerAvatar(
        file_name=file.filename,
        file_data=contents,
        employer_id=employer_detail.id,
        employer=employer_detail
    )
    employer_detail.avatar = avatar_record
    session.add(avatar_record)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)

    return {"message": "Avatar uploaded successfully"}


@employer_avatar_router.get("/employer-avatar/{avatar_id}")
async def get_avatar(
    avatar_id: int,
    session: Session = Depends(get_session)
):
    avatar_record = session.get(EmployerAvatar, avatar_id)
    if not avatar_record:
        raise HTTPException(404, "Avatar not found")

    return Response(
        content=avatar_record.file_data,
        media_type="image/jpeg" if avatar_record.file_name.lower().endswith(
            ".jpg") or avatar_record.file_name.lower().endswith(".jpeg") else "image/png",
        headers={
            "Content-Disposition": f"inline; filename={avatar_record.file_name}"
        }
    )


@employer_avatar_router.get('/get-employer-avatar/{employer_id}')
def get_current_employer_avatar(
    employer_id: int,
    session: Session = Depends(get_session)
):
    query = select(EmployerAvatar).where(
        EmployerAvatar.employer_id == employer_id)
    result = session.exec(query).first()

    if not result:
        raise HTTPException(404, "Avatar not found")

    return Response(
        content=result.file_data,
        media_type="image/jpeg" if result.file_name.lower().endswith(
            ".jpg") or result.file_name.lower().endswith(".jpeg") else "image/png",
        headers={
            "Content-Disposition": f"inline; filename={result.file_name}"
        }
    )

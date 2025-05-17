from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlmodel import Session, select
from ...auth.employer_auth import get_current_employer
from ...models.EmployerBackDrop import EmployerBackdrop
from ...models.Employer import Employer
from ...models.EmployerDetail import EmployerDetail
from ...session.session import get_session


employer_backdrop_router = APIRouter()


@employer_backdrop_router.post('/employer-backdrop/upload/')
async def upload_backdrop(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(400, "File too large (max 2MB)")

    employer_detail = session.exec(
        select(EmployerDetail).where(EmployerDetail.employer_id == employer.id)
    ).first()
    if not employer_detail:
        raise HTTPException(404, "User detail not found")

    backdrop_record = EmployerBackdrop(
        file_name=file.filename,
        file_data=contents,
        employer_id=employer_detail.id,
        employer=employer_detail
    )
    employer_detail.backdrop_image = backdrop_record
    session.add(backdrop_record)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)

    return {"message": "Backdrop uploaded successfully"}


@employer_backdrop_router.get("/employer-backdrop/{backdrop_id}")
async def get_Backdrop(
    backdrop_id: int,
    session: Session = Depends(get_session)
):
    backdrop_record = session.get(EmployerBackdrop, backdrop_id)
    if not backdrop_record:
        raise HTTPException(404, "Backdrop not found")

    return Response(
        content=backdrop_record.file_data,
        media_type="image/jpeg" if backdrop_record.file_name.lower().endswith(
            ".jpg") or backdrop_record.file_name.lower().endswith(".jpeg") else "image/png",
        headers={
            "Content-Disposition": f"inline; filename={backdrop_record.file_name}"
        }
    )

@employer_backdrop_router.get("/get-employer-backdrop/{employer_id}")
async def get_Backdrop(
    employer_id: int,
    session: Session = Depends(get_session)
):
    backdrop_record = session.get(EmployerBackdrop, employer_id)
    if not backdrop_record:
        raise HTTPException(404, "Backdrop not found")

    return Response(
        content=backdrop_record.file_data,
        media_type="image/jpeg" if backdrop_record.file_name.lower().endswith(
            ".jpg") or backdrop_record.file_name.lower().endswith(".jpeg") else "image/png",
        headers={
            "Content-Disposition": f"inline; filename={backdrop_record.file_name}"
        }
    )

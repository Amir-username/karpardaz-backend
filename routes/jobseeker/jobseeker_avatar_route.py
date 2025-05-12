from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlmodel import Session, select
from ...auth.jobseeker_auth import get_current_jobseeker
from ...models.JobSeekerAvatar import JobSeekerAvatar
from ...models.JobSeeker import JobSeeker
from ...models.JobSeekerDetail import JobSeekerDetail
from ...session.session import get_session


jobseeker_avatar_router = APIRouter()

@jobseeker_avatar_router.post('/jobseeker-avatar/upload/')
async def upload_avatar(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:  # 2MB limit
        raise HTTPException(400, "File too large (max 2MB)")

    jobseeker_detail = session.exec(
        select(JobSeekerDetail).where(JobSeekerDetail.user_id == jobseeker.id)
    ).first()
    if not jobseeker_detail:
        raise HTTPException(404, "User detail not found")

    avatar_record = JobSeekerAvatar(
        file_name=file.filename,
        file_data=contents,
        jobseeker_id=jobseeker_detail.id,
        jobseeker=jobseeker_detail
    )
    jobseeker_detail.avatar = avatar_record
    session.add(avatar_record)
    session.add(jobseeker_detail)
    session.commit()
    session.refresh(jobseeker_detail)

    return {"message": "Avatar uploaded successfully"}

@jobseeker_avatar_router.get("/jobseeker-avatar/{avatar_id}")
async def get_avatar(
    avatar_id: int,
    session: Session = Depends(get_session)
):
    avatar_record = session.get(JobSeekerAvatar, avatar_id)
    if not avatar_record:
        raise HTTPException(404, "Avatar not found")

    return Response(
        content=avatar_record.file_data,
        media_type="image/jpeg" if avatar_record.file_name.lower().endswith(".jpg") or avatar_record.file_name.lower().endswith(".jpeg") else "image/png",
        headers={
            "Content-Disposition": f"inline; filename={avatar_record.file_name}"
        }
    )

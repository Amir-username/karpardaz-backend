from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlmodel import Session, select
from ...auth.jobseeker_auth import get_current_jobseeker
from ...models.JobSeekerBackdrop import JobSeekerBackdrop
from ...models.JobSeeker import JobSeeker
from ...models.JobSeekerDetail import JobSeekerDetail
from ...session.session import get_session


jobseeker_backdrop_router = APIRouter()


@jobseeker_backdrop_router.post('/jobseeker-backdrop/upload/')
async def upload_backdrop(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(400, "File too large (max 2MB)")

    jobseeker_detail = session.exec(
        select(JobSeekerDetail).where(
            JobSeekerDetail.jobseeker_id == jobseeker.id)
    ).first()
    if not jobseeker_detail:
        raise HTTPException(404, "User detail not found")

    backdrop_record = JobSeekerBackdrop(
        file_name=file.filename,
        file_data=contents,
        jobseeker_id=jobseeker_detail.id,
        jobseeker=jobseeker_detail
    )
    jobseeker_detail.backdrop_image = backdrop_record
    session.add(backdrop_record)
    session.add(jobseeker_detail)
    session.commit()
    session.refresh(jobseeker_detail)

    return {"message": "Backdrop uploaded successfully"}


@jobseeker_backdrop_router.get("/jobseeker-backdrop/{backdrop_id}")
async def get_Backdrop(
    backdrop_id: int,
    session: Session = Depends(get_session)
):
    backdrop_record = session.get(JobSeekerBackdrop, backdrop_id)
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


@jobseeker_backdrop_router.get("/get-jobseeker-backdrop/{jobseeker_id}")
async def get_Backdrop(
    jobseeker_id: int,
    session: Session = Depends(get_session)
):
    query = select(JobSeekerBackdrop).where(
        JobSeekerBackdrop.jobseeker_id == jobseeker_id)
    backdrop_record = session.exec(query).first()
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

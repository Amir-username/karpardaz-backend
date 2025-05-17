from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlmodel import Session, select
from ..auth.jobseeker_auth import get_current_jobseeker
from ..models.Resume import Resume
from ..models.JobSeeker import JobSeeker
from ..models.JobSeekerDetail import JobSeekerDetail
from ..session.session import get_session


resume_router = APIRouter()


@resume_router.post('/resume/upload/')
async def upload_resume(
        file: UploadFile = File(...),
        session: Session = Depends(get_session),
        jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    query = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_detail_result = session.exec(query).first()

    try:
        if file.content_type != "application/pdf":
            raise HTTPException(
                400, "Invalid file type - must be application/pdf")

        contents = await file.read()

        resume_record = Resume(
            file_name=file.filename,
            file_data=contents,
            jobseeker_id=jobseeker_detail_result.id,
            jobseeker=jobseeker_detail_result
        )

        session.add(resume_record)
        session.commit()

        jobseeker_detail_result.resume = resume_record
        session.add(jobseeker_detail_result)
        session.commit()
        session.refresh(jobseeker_detail_result)

        return {"message": "Resume uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@resume_router.get("/resume/{resume_id}")
async def get_resume(
    resume_id: int,
    session: Session = Depends(get_session)
):
    resume_record = session.get(Resume, resume_id)
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found")

    return Response(
        content=resume_record.file_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={resume_record.file_name}"}
    )


@resume_router.get("/get-resume/{jobseeker_id}")
async def get_jobseeker_resume(
    jobseeker_id: int,
    session: Session = Depends(get_session)
):
    query = select(Resume).where(Resume.jobseeker_id == jobseeker_id)
    resume_record = session.exec(query).first()
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found")

    return Response(
        content=resume_record.file_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={resume_record.file_name}"}
    )


@resume_router.delete("/resume/{resume_id}")
def delete_resume(
    resume_id: int,
    session: Session = Depends(get_session),
    jobseeker: JobSeeker = Depends(get_current_jobseeker)
):
    resume = select(Resume).where(Resume.id == resume_id)
    resume_res = session.exec(resume).first()
    if not resume_res:
        raise HTTPException(status_code=404, detail="Resume not found")

    jobseeker_detail = select(JobSeekerDetail).where(
        JobSeekerDetail.jobseeker_id == jobseeker.id)
    jobseeker_detail_res = session.exec(jobseeker_detail).first()

    if jobseeker_detail_res.resume.id == resume_res.id:
        session.delete(resume_res)
        session.commit()
        return {
            'message': 'resume has been deleted'
        }

    return None

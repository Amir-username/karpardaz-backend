from fastapi import HTTPException, status, UploadFile, Response
from sqlmodel import Session
from datetime import timedelta

from auth.employer_auth import authenticate_employer, get_current_employer
from auth.token import Token, create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.password import get_password_hash
from models.Employer import Employer, EmployerCreate, EmployerPublic, EmployerUpdate
from models.EmployerDetail import EmployerDetail, EmployerDetailCreate, EmployerDetailUpdate
from models.EmployerAvatar import EmployerAvatar
from models.EmployerBackDrop import EmployerBackdrop
from models.Advertise import Advertise, AdvertiseCreate, AdvertisePublic, AdvertiseUpdate
from models.Interview import Interview
from repository.employer_repo import (
    get_employer_by_email,
    create_employer,
    count_employers,
    get_all_employers,
    get_employer_by_id,
    update_employer_fields,
    delete_employer as repo_delete_employer,
    get_employer_detail_by_employer_id,
    create_employer_detail,
    get_employer_detail_by_id,
    get_all_employer_details,
    update_employer_detail_fields,
    delete_employer_detail as repo_delete_employer_detail,
    count_advertisements,
    get_all_advertisements,
    get_advertisements_by_employer_id,
    get_advertisement_by_id,
    get_advertisement_by_id_and_employer,
    create_advertisement,
    update_advertisement_fields,
    delete_advertisement as repo_delete_advertisement,
    get_jobseeker_ad_by_id,
    like_jobseeker_ad,
    dislike_jobseeker_ad,
    get_avatar_by_id,
    get_avatar_by_employer_id,
    save_avatar,
    get_backdrop_by_id,
    get_backdrop_by_employer_id,
    save_backdrop,
    get_interview_by_advertise_id,
    create_interview,
    add_interview_answers,
    delete_interview as repo_delete_interview,
)


# ─── Auth ───────────────────────────────────────────────────────

def login_employer(form_data) -> Token:
    employer = authenticate_employer(form_data.username, form_data.password)
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": employer.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def register_employer(session: Session, employer_in: EmployerCreate) -> EmployerPublic:
    existing = get_employer_by_email(session, employer_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(employer_in.password)
    db_employer = Employer.model_validate(
        employer_in, update={"hashed_password": hashed_password}
    )
    return create_employer(session, db_employer)


def get_employers_list(session: Session, offset: int, limit: int) -> dict:
    total_items = count_employers(session)
    total_pages = (total_items + limit - 1) // limit
    employers = get_all_employers(session, offset, limit)
    return {"total_pages": total_pages, "employers": employers}


def get_employer(session: Session, employer_id: int) -> EmployerPublic:
    employer = get_employer_by_id(session, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


def update_employer(session: Session, employer_id: int, employer_in: EmployerUpdate, current_user: Employer) -> EmployerPublic:
    if current_user.id != employer_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")

    db_employer = get_employer_by_id(session, employer_id)
    if not db_employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    updates = employer_in.model_dump(exclude_unset=True)
    if "password" in updates and updates["password"]:
        updates["hashed_password"] = get_password_hash(updates.pop("password"))
    else:
        updates.pop("password", None)

    return update_employer_fields(session, db_employer, **updates)


def remove_employer(session: Session, employer_id: int, current_user: Employer) -> None:
    if current_user.id != employer_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")

    employer = get_employer_by_id(session, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    repo_delete_employer(session, employer)


# ─── Employer Detail ────────────────────────────────────────────

def create_detail(session: Session, detail_in: EmployerDetailCreate, employer: Employer) -> EmployerDetail:
    db = EmployerDetail.model_validate(detail_in)
    db.employer = employer
    db.employer_id = employer.id
    db.company_name = employer.company_name
    return create_employer_detail(session, db)


def get_detail(session: Session, detail_id: int) -> EmployerDetail:
    result = get_employer_detail_by_id(session, detail_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employer detail not found")
    return result


def get_all_details(session: Session) -> list[EmployerDetail]:
    return get_all_employer_details(session)


def update_detail(session: Session, detail_id: int, detail_in: EmployerDetailUpdate, employer: Employer) -> EmployerDetail:
    result = get_employer_detail_by_id(session, detail_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employer detail not found")
    if result.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this detail")

    updates = detail_in.model_dump(exclude_unset=True)
    return update_employer_detail_fields(session, result, **updates)


def remove_detail(session: Session, detail_id: int, employer: Employer):
    result = get_employer_detail_by_id(session, detail_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employer detail not found")
    if result.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this detail")

    repo_delete_employer_detail(session, result)
    return "deleted employer detail"


# ─── Advertisements ────────────────────────────────────────────

def _get_employer_detail_or_404(session: Session, employer: Employer) -> EmployerDetail:
    detail = get_employer_detail_by_employer_id(session, employer.id)
    if not detail:
        raise HTTPException(status_code=404, detail="Employer detail not found")
    return detail


def create_ad(session: Session, ad_in: AdvertiseCreate, employer: Employer) -> AdvertisePublic:
    employer_detail = _get_employer_detail_or_404(session, employer)

    ad = Advertise(
        title=ad_in.title,
        position=ad_in.position,
        experience=ad_in.experience,
        salary=ad_in.salary,
        job_group=ad_in.job_group,
        is_remote=ad_in.is_remote,
        city=ad_in.city,
        is_internship=ad_in.is_internship,
        gender=ad_in.gender,
        benefits=ad_in.benefits,
        technologies=ad_in.technologies,
        is_portfolio=ad_in.is_portfolio,
        description=ad_in.description,
        employer_id=employer_detail.id,
        employer=employer_detail,
    )
    return create_advertisement(session, Advertise.model_validate(ad))


def get_ads_list(session: Session, offset: int, limit: int) -> dict:
    total_items = count_advertisements(session)
    total_pages = (total_items + limit - 1) // limit
    ads = get_all_advertisements(session, offset, limit)
    return {"total_pages": total_pages, "advertises": ads}


def get_ads_by_employer(session: Session, employer_id: int) -> list[AdvertisePublic]:
    return get_advertisements_by_employer_id(session, employer_id)


def get_ad(session: Session, ad_id: int) -> AdvertisePublic:
    ad = get_advertisement_by_id(session, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


def get_my_ads(session: Session, employer: Employer) -> list[AdvertisePublic]:
    return get_advertisements_by_employer_id(session, employer.id)


def update_ad(session: Session, ad_id: int, ad_in: AdvertiseUpdate, employer: Employer) -> AdvertisePublic:
    db_ad = get_advertisement_by_id_and_employer(session, ad_id, employer.id)
    if not db_ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    updates = ad_in.model_dump(exclude_unset=True)
    return update_advertisement_fields(session, db_ad, **updates)


def remove_ad(session: Session, ad_id: int, employer: Employer) -> None:
    ad = get_advertisement_by_id_and_employer(session, ad_id, employer.id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    repo_delete_advertisement(session, ad)


# ─── Ad Search ──────────────────────────────────────────────────

def search_ads(session: Session, *, search_q: str | None, city_q: str | None,
               is_internship: bool | None, is_remote: bool | None, is_portfolio: bool | None,
               experience, salary, gender, position,
               offset: int, limit: int) -> dict:
    from sqlmodel import or_

    filters = []
    if search_q:
        filters.append(
            or_(
                Advertise.title.ilike(f"%{search_q}%"),
                Advertise.description.ilike(f"%{search_q}%"),
                Advertise.employer.has(company_name=search_q),
            )
        )
    if city_q:
        filters.append(Advertise.city.ilike(f"%{city_q}%"))
    if is_internship is not None:
        filters.append(Advertise.is_internship == is_internship)
    if is_remote is not None:
        filters.append(Advertise.is_remote == is_remote)
    if is_portfolio is not None:
        filters.append(Advertise.is_portfolio == is_portfolio)
    if experience is not None:
        filters.append(Advertise.experience == experience)
    if salary is not None:
        filters.append(Advertise.salary == salary)
    if gender is not None:
        filters.append(Advertise.gender == gender)
    if position is not None:
        filters.append(Advertise.position == position)

    from repository.employer_repo import search_advertisements
    total_items = count_advertisements(session)
    total_pages = (total_items + limit - 1) // limit
    results = search_advertisements(session, filters, offset, limit)

    return {"total_pages": total_pages, "advertises": results}


# ─── Likes ──────────────────────────────────────────────────────

def like_ad(session: Session, advertise_id: int, employer: Employer) -> list:
    employer_detail = _get_employer_detail_or_404(session, employer)
    jobseeker_ad = get_jobseeker_ad_by_id(session, advertise_id)
    if not jobseeker_ad:
        raise HTTPException(status_code=404, detail="Job seeker ad not found")
    return like_jobseeker_ad(session, employer_detail, jobseeker_ad)


def dislike_ad(session: Session, advertise_id: int, employer: Employer) -> list:
    employer_detail = _get_employer_detail_or_404(session, employer)
    jobseeker_ad = get_jobseeker_ad_by_id(session, advertise_id)
    if not jobseeker_ad:
        raise HTTPException(status_code=404, detail="Job seeker ad not found")
    return dislike_jobseeker_ad(session, employer_detail, jobseeker_ad)


def get_favorites(session: Session, employer: Employer) -> list[int]:
    employer_detail = _get_employer_detail_or_404(session, employer)
    return [fav.id for fav in employer_detail.liked_jobseeker_ads]


# ─── Avatar ──────────────────────────────────────────────────────

async def upload_avatar(session: Session, file: UploadFile, employer: Employer) -> dict:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 2MB)")

    employer_detail = _get_employer_detail_or_404(session, employer)

    avatar_record = EmployerAvatar(
        file_name=file.filename,
        file_data=contents,
        employer_id=employer_detail.id,
        employer=employer_detail,
    )
    save_avatar(session, avatar_record, employer_detail)
    return {"message": "Avatar uploaded successfully"}


def get_avatar(session: Session, avatar_id: int) -> Response:
    avatar = get_avatar_by_id(session, avatar_id)
    if not avatar:
        raise HTTPException(404, "Avatar not found")
    return _build_image_response(avatar.file_name, avatar.file_data)


def get_avatar_by_employer(session: Session, employer_id: int) -> Response:
    employer_detail = _get_employer_detail_or_404(session, employer_id)
    # need actual employer object for _get_employer_detail_or_404 — use repo directly
    avatar = get_avatar_by_employer_id(session, employer_detail.id)
    if not avatar:
        raise HTTPException(404, "Avatar not found")
    return _build_image_response(avatar.file_name, avatar.file_data)


def get_avatar_by_employer_id(session: Session, employer_detail_id: int) -> Response:
    avatar = get_avatar_by_employer_id(session, employer_detail_id)
    if not avatar:
        raise HTTPException(404, "Avatar not found")
    return _build_image_response(avatar.file_name, avatar.file_data)


# ─── Backdrop ────────────────────────────────────────────────────

async def upload_backdrop(session: Session, file: UploadFile, employer: Employer) -> dict:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type - must be JPEG or PNG")

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 5MB)")

    employer_detail = _get_employer_detail_or_404(session, employer)

    backdrop_record = EmployerBackdrop(
        file_name=file.filename,
        file_data=contents,
        employer_id=employer_detail.id,
        employer=employer_detail,
    )
    save_backdrop(session, backdrop_record, employer_detail)
    return {"message": "Backdrop uploaded successfully"}


def get_backdrop(session: Session, backdrop_id: int) -> Response:
    backdrop = get_backdrop_by_id(session, backdrop_id)
    if not backdrop:
        raise HTTPException(404, "Backdrop not found")
    return _build_image_response(backdrop.file_name, backdrop.file_data)


def get_backdrop_by_employer_id(session: Session, employer_detail_id: int) -> Response:
    backdrop = get_backdrop_by_employer_id(session, employer_detail_id)
    if not backdrop:
        raise HTTPException(404, "Backdrop not found")
    return _build_image_response(backdrop.file_name, backdrop.file_data)


# ─── Interview ───────────────────────────────────────────────────

def create_interview_logic(session: Session, advertise_id: int, questions: list[str], employer: Employer) -> Interview:
    advertise = get_advertisement_by_id(session, advertise_id)
    if not advertise:
        raise HTTPException(status_code=404, detail="Advertise not found")
    if advertise.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    interview = Interview(
        questions=questions,
        advertise_id=advertise_id,
        advertise=advertise,
    )
    return create_interview(session, interview, advertise)


def add_interview_answers_logic(session: Session, interview_id: int, user_answers: list[str], jobseeker) -> Interview:
    interview = get_interview_by_advertise_id(session, interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    for ans in interview.answers:
        if ans.get("jobseeker_id") == jobseeker.id:
            return interview  # already answered

    db_answer = {"jobseeker_id": jobseeker.id, "answers": user_answers}
    interview.answers = interview.answers + [db_answer]
    interview.jobseeker_ids = interview.jobseeker_ids + [jobseeker.id]

    return add_interview_answers(session, interview)


def get_interview_logic(session: Session, advertise_id: int) -> Interview:
    advertise = get_advertisement_by_id(session, advertise_id)
    if not advertise:
        raise HTTPException(status_code=404, detail="Advertise not found")

    interview = get_interview_by_advertise_id(session, advertise_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return interview


def remove_interview(session: Session, advertise_id: int, employer: Employer) -> None:
    advertise = get_advertisement_by_id(session, advertise_id)
    if not advertise:
        raise HTTPException(status_code=404, detail="Advertise not found")

    interview = get_interview_by_advertise_id(session, advertise_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if employer.id != advertise.employer_id:
        raise HTTPException(status_code=401, detail="You don't have permission for that")

    repo_delete_interview(session, interview)


# ─── Helpers ────────────────────────────────────────────────────

def _build_image_response(file_name: str, file_data: bytes) -> Response:
    media_type = "image/jpeg" if file_name.lower().endswith((".jpg", ".jpeg")) else "image/png"
    return Response(
        content=file_data,
        media_type=media_type,
        headers={"Content-Disposition": f"inline; filename={file_name}"},
    )

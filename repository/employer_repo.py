from typing import Optional
from sqlmodel import Session, select, func, desc, or_

from models.Employer import Employer
from models.EmployerDetail import EmployerDetail
from models.EmployerAvatar import EmployerAvatar
from models.EmployerBackDrop import EmployerBackdrop
from models.Advertise import Advertise
from models.Interview import Interview
from models.JobSeekerAd import JobSeekerAd


# ─── Employer CRUD ──────────────────────────────────────────────

def get_employer_by_email(session: Session, email: str) -> Optional[Employer]:
    return session.exec(select(Employer).where(Employer.email == email)).first()


def create_employer(session: Session, employer: Employer) -> Employer:
    session.add(employer)
    session.commit()
    session.refresh(employer)
    return employer


def count_employers(session: Session) -> int:
    return session.exec(select(func.count()).select_from(Employer)).one()


def get_all_employers(session: Session, offset: int, limit: int) -> list[Employer]:
    return session.exec(select(Employer).offset(offset).limit(limit)).all()


def get_employer_by_id(session: Session, employer_id: int) -> Optional[Employer]:
    return session.get(Employer, employer_id)


def update_employer_fields(session: Session, employer: Employer, **updates) -> Employer:
    for key, value in updates.items():
        if value is not None:
            setattr(employer, key, value)
    session.add(employer)
    session.commit()
    session.refresh(employer)
    return employer


def delete_employer(session: Session, employer: Employer) -> None:
    session.delete(employer)
    session.commit()


# ─── Employer Detail CRUD ───────────────────────────────────────

def get_employer_detail_by_employer_id(session: Session, employer_id: int) -> Optional[EmployerDetail]:
    return session.exec(
        select(EmployerDetail).where(EmployerDetail.employer_id == employer_id)
    ).first()


def create_employer_detail(session: Session, detail: EmployerDetail) -> EmployerDetail:
    session.add(detail)
    session.commit()
    session.refresh(detail)
    return detail


def get_employer_detail_by_id(session: Session, detail_id: int) -> Optional[EmployerDetail]:
    return session.exec(
        select(EmployerDetail).where(EmployerDetail.id == detail_id)
    ).first()


def get_all_employer_details(session: Session) -> list[EmployerDetail]:
    return session.exec(select(EmployerDetail)).all()


def update_employer_detail_fields(session: Session, detail: EmployerDetail, **updates) -> EmployerDetail:
    for key, value in updates.items():
        if value is not None:
            setattr(detail, key, value)
    session.add(detail)
    session.commit()
    session.refresh(detail)
    return detail


def delete_employer_detail(session: Session, detail: EmployerDetail) -> None:
    session.delete(detail)
    session.commit()


# ─── Advertisements ─────────────────────────────────────────────

def count_advertisements(session: Session) -> int:
    return session.exec(select(func.count()).select_from(Advertise)).one()


def get_all_advertisements(session: Session, offset: int, limit: int) -> list[Advertise]:
    return session.exec(
        select(Advertise).order_by(desc(Advertise.id)).offset(offset).limit(limit)
    ).all()


def get_advertisements_by_employer_id(session: Session, employer_id: int) -> list[Advertise]:
    return session.exec(
        select(Advertise).order_by(desc(Advertise.id)).where(Advertise.employer_id == employer_id)
    ).all()


def get_advertisement_by_id(session: Session, ad_id: int) -> Optional[Advertise]:
    return session.get(Advertise, ad_id)


def get_advertisement_by_id_and_employer(
    session: Session, ad_id: int, employer_id: int
) -> Optional[Advertise]:
    return session.exec(
        select(Advertise).where(Advertise.id == ad_id, Advertise.employer_id == employer_id)
    ).first()


def create_advertisement(session: Session, advertisement: Advertise) -> Advertise:
    session.add(advertisement)
    session.commit()
    session.refresh(advertisement)
    return advertisement


def update_advertisement_fields(session: Session, ad: Advertise, **updates) -> Advertise:
    for key, value in updates.items():
        if value is not None:
            setattr(ad, key, value)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


def delete_advertisement(session: Session, ad: Advertise) -> None:
    session.delete(ad)
    session.commit()


def search_advertisements(
    session: Session,
    filters: list,
    offset: int,
    limit: int,
) -> list[Advertise]:
    query = select(Advertise)
    if filters:
        query = query.where(*filters)
    query = query.order_by(desc(Advertise.id)).offset(offset).limit(limit)
    return session.exec(query).all()


# ─── Likes ──────────────────────────────────────────────────────

def get_jobseeker_ad_by_id(session: Session, ad_id: int) -> Optional[JobSeekerAd]:
    return session.get(JobSeekerAd, ad_id)


def like_jobseeker_ad(session: Session, employer_detail: EmployerDetail, jobseeker_ad: JobSeekerAd) -> list:
    employer_detail.liked_jobseeker_ads.append(jobseeker_ad)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)
    return employer_detail.liked_jobseeker_ads


def dislike_jobseeker_ad(session: Session, employer_detail: EmployerDetail, jobseeker_ad: JobSeekerAd) -> list:
    employer_detail.liked_jobseeker_ads.remove(jobseeker_ad)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)
    return employer_detail.liked_jobseeker_ads


# ─── Avatar ──────────────────────────────────────────────────────

def get_avatar_by_id(session: Session, avatar_id: int) -> Optional[EmployerAvatar]:
    return session.get(EmployerAvatar, avatar_id)


def get_avatar_by_employer_id(session: Session, employer_detail_id: int) -> Optional[EmployerAvatar]:
    return session.exec(
        select(EmployerAvatar).where(EmployerAvatar.employer_id == employer_detail_id)
    ).first()


def save_avatar(session: Session, avatar: EmployerAvatar, employer_detail: EmployerDetail) -> EmployerAvatar:
    employer_detail.avatar = avatar
    session.add(avatar)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)
    return avatar


# ─── Backdrop ────────────────────────────────────────────────────

def get_backdrop_by_id(session: Session, backdrop_id: int) -> Optional[EmployerBackdrop]:
    return session.get(EmployerBackdrop, backdrop_id)


def get_backdrop_by_employer_id(session: Session, employer_detail_id: int) -> Optional[EmployerBackdrop]:
    return session.exec(
        select(EmployerBackdrop).where(EmployerBackdrop.employer_id == employer_detail_id)
    ).first()


def save_backdrop(session: Session, backdrop: EmployerBackdrop, employer_detail: EmployerDetail) -> EmployerBackdrop:
    employer_detail.backdrop_image = backdrop
    session.add(backdrop)
    session.add(employer_detail)
    session.commit()
    session.refresh(employer_detail)
    return backdrop


# ─── Interview ───────────────────────────────────────────────────

def get_interview_by_advertise_id(session: Session, advertise_id: int) -> Optional[Interview]:
    return session.exec(
        select(Interview).where(Interview.advertise_id == advertise_id)
    ).first()


def create_interview(session: Session, interview: Interview, advertise: Advertise) -> Interview:
    advertise.interview = interview
    session.add_all([interview, advertise])
    session.commit()
    session.refresh(interview)
    session.refresh(advertise)
    return interview


def add_interview_answers(session: Session, interview: Interview) -> Interview:
    session.add(interview)
    session.commit()
    session.refresh(interview)
    return interview


def delete_interview(session: Session, interview: Interview) -> None:
    session.delete(interview)
    session.commit()

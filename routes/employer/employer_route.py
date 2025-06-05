from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from ...auth.employer_auth import authenticate_employer
from ...auth.token import Token, create_access_token
from ...config import ACCESS_TOKEN_EXPIRE_MINUTES
from ...models.Employer import Employer, EmployerCreate, EmployerPublic, EmployerUpdate
from sqlmodel import Session, select, func
from ...session.session import get_session
from ...password import get_password_hash
from ...auth.employer_auth import get_current_employer

employer_router = APIRouter()


@employer_router.post("/employer/login")
async def login_for_access_token_employer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
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


# Employer CRUD

# Create Employer
@employer_router.post("/employers/", response_model=EmployerPublic)
def create_employer(*, session: Session = Depends(get_session), employer: EmployerCreate):
    # Check if email already exists
    existing_employer = session.exec(select(Employer).where(
        Employer.email == employer.email)).first()
    if existing_employer:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(employer.password)

    # Create the employer
    db_employer = Employer.model_validate(
        employer, update={"hashed_password": hashed_password})
    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer


# Get all Employers
@employer_router.get("/employers/")
def read_employers(*, session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    total_items = session.exec(
        select(func.count()).select_from(Employer)).one()
    total_pages = (total_items + limit - 1) // limit

    query = select(Employer).offset(offset=offset).limit(limit=limit)
    employers = session.exec(query).all()

    response = {
        'total_pages': total_pages,
        'advertises': employers
    }
    return response

# Ger Employer by ID


@employer_router.get("/employers/{employer_id}", response_model=EmployerPublic)
def read_employer(*, session: Session = Depends(get_session), employer_id: int):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


# Update Employer by ID
@employer_router.patch("/employers/{employer_id}", response_model=EmployerPublic)
def update_employer(*, session: Session = Depends(get_session), employer_id: int, employer: EmployerUpdate,
                    current_user: Employer = Depends(get_current_employer)):

    if current_user.id != employer_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this profile")

    db_employer = session.get(Employer, employer_id)
    if not db_employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    # Update fields if provided
    if employer.company_name:
        db_employer.company_name = employer.company_name
    if employer.email:
        db_employer.email = employer.email
    if employer.password:
        db_employer.hashed_password = get_password_hash(employer.password)

    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer


# Delete Employer by ID
@employer_router.delete("/employers/{employer_id}")
def delete_employer(*, session: Session = Depends(get_session), employer_id: int, current_user: Employer = Depends(get_current_employer)):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    session.delete(employer)
    session.commit()
    return None


# @employer_router.delete("/employers/{employer_id}")
# def delete_employer(*, session: Session = Depends(get_session), employer_id: int,
#                     current_user: Union[Employer, Admin] = Depends(get_current_employer_or_admin)):

#     if isinstance(current_user, Admin):
#         user_to_delete = session.get(Employer, employer_id)
#         if not user_to_delete:
#             raise HTTPException(status_code=404, detail="User not found")
#         session.delete(user_to_delete)
#         session.commit()
#         return

#     if isinstance(current_user, Employer):
#         employer = session.get(Employer, employer_id)
#         if not employer:
#             raise HTTPException(status_code=404, detail="Employer not found")
#         session.delete(employer)
#         session.commit()
#         return None

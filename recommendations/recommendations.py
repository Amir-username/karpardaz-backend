# app/routers/recommendations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

from ..models.JobSeeker import JobSeeker
from ..session.session import get_session
from ..auth.jobseeker_auth import get_current_jobseeker

from ..models.Advertise import Advertise, AdvertisePublic
from ..models.JobSeekerDetail import JobSeekerDetail
from ..Enums.experience_enum import ExperienceEnum
from ..Enums.position_enum import PositionEnum
from ..Enums.gender_enum import GenderEnum

recommend_router = APIRouter()

# Helper functions
def one_hot_encode(value, vocabulary: list) -> List[int]:
    """Create one-hot encoded vector for a single value"""
    return [1 if value == item else 0 for item in vocabulary]

def multi_hot_encode(values: list, vocabulary: list) -> List[int]:
    """Create multi-hot encoded vector for multiple values"""
    return [1 if item in values else 0 for item in vocabulary]

def pre_filter_ads(job_seeker: JobSeekerDetail, all_ads: List[Advertise]) -> List[Advertise]:
    """Apply hard constraints to filter ads"""
    filtered = []
    for ad in all_ads:
        # Remote work filter
        # if job_seeker.is_remote and not ad.is_remote:
        #     continue
            
        # # Internship filter
        # if job_seeker.is_internship and not ad.is_internship:
        #     continue
            
        # Gender compatibility filter
        if ad.gender != GenderEnum.NO_DIFFERENCE:
            if job_seeker.gender == GenderEnum.NO_DIFFERENCE:
                continue
            elif ad.gender != job_seeker.gender:
                continue
                
        filtered.append(ad)
    return filtered

def vectorize_entities(job_seeker: JobSeekerDetail, ads: List[Advertise]):
    """Create feature vectors for recommendation"""
    # Build vocabularies from available data
    job_groups = sorted(set([ad.job_group for ad in ads] + [job_seeker.job_group]))
    tech_skills = sorted(set(tech for ad in ads for tech in ad.technologies) 
                         | set(job_seeker.technologies))
    
    # Fixed enums vocabularies
    position_vocab = list(PositionEnum)
    experience_vocab = list(ExperienceEnum)
    
    # Vectorize job seeker
    seeker_vector = []
    seeker_vector += one_hot_encode(job_seeker.position, position_vocab)
    seeker_vector += one_hot_encode(job_seeker.experience, experience_vocab)
    seeker_vector += one_hot_encode(job_seeker.job_group, job_groups)
    seeker_vector += multi_hot_encode(job_seeker.technologies, tech_skills)
    
    # Vectorize ads
    ad_vectors = []
    for ad in ads:
        ad_vector = []
        ad_vector += one_hot_encode(ad.position, position_vocab)
        ad_vector += one_hot_encode(ad.experience, experience_vocab)
        ad_vector += one_hot_encode(ad.job_group, job_groups)
        ad_vector += multi_hot_encode(ad.technologies, tech_skills)
        ad_vectors.append(ad_vector)
        
    return np.array(seeker_vector), np.array(ad_vectors)

def calculate_similarities(seeker_vector, ad_vectors) -> np.ndarray:
    """Compute cosine similarity between job seeker and ads"""
    # Add epsilon to avoid division by zero
    epsilon = 1e-8
    seeker_norm = seeker_vector / (np.linalg.norm(seeker_vector) + epsilon)
    ad_norms = ad_vectors / (np.linalg.norm(ad_vectors, axis=1, keepdims=True) + epsilon)
    return cosine_similarity(seeker_norm.reshape(1, -1), ad_norms)[0]

def recommend_ads(
    job_seeker: JobSeekerDetail, 
    all_ads: List[Advertise], 
    top_n: int = 10
) -> List[Advertise]:
    """Main recommendation function"""
    # Apply hard constraints
    filtered_ads = pre_filter_ads(job_seeker, all_ads)
    if not filtered_ads:
        return []

    # Generate vectors
    seeker_vec, ad_vecs = vectorize_entities(job_seeker, filtered_ads)
    
    # Calculate similarities
    similarities = calculate_similarities(seeker_vec, ad_vecs)
    
    # Rank and return top N
    ranked_indices = np.argsort(similarities)[::-1]
    return [filtered_ads[i] for i in ranked_indices[:top_n]]

# FastAPI Endpoint
@recommend_router.get("/recommendation-jobs/", response_model=List[AdvertisePublic])
async def get_job_recommendations(
    *,
    session: Session = Depends(get_session),
    current_user: JobSeeker = Depends(get_current_jobseeker),
    top_n: int = 10
):
    """
    Get personalized job recommendations for authenticated job seeker
    
    Parameters:
    - top_n: Number of recommendations to return (default: 10)
    
    Returns:
    - List of recommended job advertisements
    """
    # Get job seeker profile
    job_seeker = session.exec(
        select(JobSeekerDetail)
        .where(JobSeekerDetail.jobseeker_id == current_user.id)
    ).first()
    
    if not job_seeker:
        raise HTTPException(
            status_code=404, 
            detail="Job seeker profile not found. Please complete your profile."
        )

    # Get active job advertisements
    # Add .where(Advertise.is_active == True) if you have an is_active flag
    statement = select(Advertise)
    all_ads = session.exec(statement).all()

    # Get recommendations
    recommended_ads = recommend_ads(job_seeker, all_ads, top_n=top_n)
    
    # Convert to public response model
    return [
        AdvertisePublic(
            id=ad.id,
            employer_id=ad.employer_id,
            title=ad.title,
            position=ad.position,
            experience=ad.experience,
            salary=ad.salary,
            job_group=ad.job_group,
            city=ad.city,
            is_remote=ad.is_remote,
            is_internship=ad.is_internship,
            gender=ad.gender,
            benefits=ad.benefits,
            technologies=ad.technologies,
            is_portfolio=ad.is_portfolio,
            description=ad.description
        )
        for ad in recommended_ads
    ]
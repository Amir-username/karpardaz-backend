# Karpardaz Backend

A comprehensive job portal backend API built with FastAPI, featuring intelligent job recommendations and a dual-sided marketplace for employers and job seekers.

## 🌐 Live Demo

**API Documentation**: [https://underlying-umeko-univercityproject317-ea179cc6.koyeb.app/docs](https://underlying-umeko-univercityproject317-ea179cc6.koyeb.app/docs)

Explore the interactive API documentation and test all endpoints directly in your browser.

## 🚀 Features

### Core Functionality
- **Dual User System**: Separate authentication and workflows for employers and job seekers
- **Job Advertisement System**: Complete job posting and management
- **Job Seeker Profiles**: Detailed profiles with skills, preferences, and portfolio
- **Intelligent Recommendations**: ML-powered job matching using cosine similarity
- **Application Management**: Request system for job applications
- **Interview Scheduling**: Built-in interview management
- **File Management**: Avatar and backdrop image uploads
- **Resume Management**: Resume upload and management system

### Advanced Features
- **Smart Filtering**: Location, gender, remote work, and technology-based filtering
- **Like System**: Mutual liking between employers and job seekers
- **Admin Dashboard**: Analytics and user management
- **Search & Discovery**: Advanced search capabilities
- **Real-time Matching**: Dynamic recommendation engine

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLModel
- **Authentication**: JWT with OAuth2PasswordBearer
- **Machine Learning**: scikit-learn for recommendations
- **Password Security**: bcrypt
- **Validation**: Pydantic
- **File Handling**: python-multipart

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip package manager

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd karpardaz-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📚 API Documentation

### Authentication Endpoints

#### Job Seeker Authentication
- `POST /jobseeker/register` - Register new job seeker
- `POST /jobseeker/login` - Login job seeker
- `GET /jobseeker/me` - Get current job seeker profile

#### Employer Authentication
- `POST /employer/register` - Register new employer
- `POST /employer/login` - Login employer
- `GET /employer/me` - Get current employer profile

### Job Advertisement Endpoints

#### Employer Job Management
- `POST /employer/advertise` - Create job advertisement
- `GET /employer/advertise` - Get employer's job advertisements
- `PUT /employer/advertise/{id}` - Update job advertisement
- `DELETE /employer/advertise/{id}` - Delete job advertisement

#### Job Search & Discovery
- `GET /search/advertise` - Search job advertisements
- `GET /recommendation-jobs/` - Get personalized job recommendations

### Job Seeker Profile Endpoints

#### Profile Management
- `POST /jobseeker/detail` - Create job seeker profile
- `GET /jobseeker/detail` - Get job seeker profile
- `PUT /jobseeker/detail` - Update job seeker profile

#### Job Seeker Advertisements
- `POST /jobseeker/advertise` - Create job seeker advertisement
- `GET /jobseeker/advertise` - Get job seeker advertisements
- `GET /search/jobseeker-advertise` - Search job seeker profiles

### Interaction Endpoints

#### Like System
- `POST /jobseeker/liked-ads` - Like job advertisement
- `GET /jobseeker/liked-ads` - Get liked job advertisements
- `POST /employer/liked-ads` - Like job seeker advertisement
- `GET /employer/liked-ads` - Get liked job seeker advertisements

#### Application Management
- `POST /employer/ad-request` - Send job application request
- `POST /jobseeker/ad-request` - Send job seeker application request
- `GET /employer/ad-request` - Get received applications
- `GET /jobseeker/ad-request` - Get sent applications

### File Management
- `POST /jobseeker/avatar` - Upload job seeker avatar
- `POST /employer/avatar` - Upload employer avatar
- `POST /jobseeker/backdrop` - Upload job seeker backdrop
- `POST /employer/backdrop` - Upload employer backdrop
- `POST /resume` - Upload resume

### Interview Management
- `POST /interview` - Schedule interview
- `GET /interview` - Get interviews
- `PUT /interview/{id}` - Update interview
- `DELETE /interview/{id}` - Cancel interview

### Admin Endpoints
- `GET /admin/charts` - Get analytics data
- `GET /admin/users` - Get all users
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Delete user

## 🗄️ Database Schema

### Core Models

#### User Models
- **Employer**: Company information and authentication
- **JobSeeker**: Personal information and authentication
- **Admin**: Administrative user

#### Detail Models
- **EmployerDetail**: Extended employer information
- **JobSeekerDetail**: Extended job seeker information

#### Advertisement Models
- **Advertise**: Job advertisements posted by employers
- **JobSeekerAd**: Job seeker profiles/advertisements

#### Relationship Models
- **JobSeekerLikedAdsLink**: Many-to-many relationship for liked job ads
- **EmployerLikedAdsLink**: Many-to-many relationship for liked job seeker ads

#### Request Models
- **AdRequest**: Job application requests
- **JobSeekerAdRequest**: Job seeker application requests

#### Supporting Models
- **Resume**: Resume file management
- **Interview**: Interview scheduling
- **Project**: Project portfolio management

## 🤖 Recommendation Engine

The system includes an intelligent recommendation engine that:

1. **Pre-filters** job advertisements based on hard constraints:
   - Location compatibility
   - Gender preferences
   - Remote work preferences

2. **Vectorizes** entities using:
   - One-hot encoding for categorical data (position, experience)
   - Multi-hot encoding for skills and technologies
   - Dynamic vocabulary building from available data

3. **Calculates** cosine similarity between job seeker profiles and job advertisements

4. **Ranks** and returns the most relevant job recommendations

### Usage
```python
# Get personalized recommendations
GET /recommendation-jobs/?top_n=10
```

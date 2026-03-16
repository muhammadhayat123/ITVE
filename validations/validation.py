from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    # Basic Info
    institute_name: str
    name: str
    phone: str
    cnic: str
    gender: str

    # Account Info
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    # Location
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Dates as strings (DD-MM-YYYY)
    date_of_birth: str
    institute_age: str

    # Experience
    experience_years: int

    # Self Rating (1-10 scale recommended)
    technology_awareness: int
    leadership: int
    communication: int
    management: int
    motivation: int
    teaching_skills: int

    # Optional
    promo_code: Optional[str] = None




class SchoolEditProfile(BaseModel):
    institute_name: Optional[str] = Field(None, min_length=3, max_length=150)
    bio: Optional[str] = Field(None, min_length=10, max_length=500)

    gender: Optional[str] = None
    date_of_institute: Optional[str] = None

    phone: Optional[str] = Field(None, pattern=r"^\+92\d{10}$")
    email: Optional[EmailStr] = None

    username: Optional[str] = Field(None, pattern="^[a-zA-Z0-9_]+$")

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    profile_image: Optional[str] = None
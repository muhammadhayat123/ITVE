from fastapi import Depends, FastAPI, APIRouter, HTTPException, dependencies, status
from validations.validation import UserCreate
from config.db import users_collection
from utils.util_helper import hash_password
from validations.validation import SchoolEditProfile
from utils.util_helper import verify_token, create_access_token, decode_access_token




user_route = APIRouter()









# -------------------------------
# Sign-up Route
# -------------------------------
@user_route.post("/sign-up", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate,):
    try:
        existing_user = users_collection.find_one({
            "$or": [
                {"email": user.email},
                {"username": user.username}
            ]
        })

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        hashed_password = hash_password(user.password)

        new_user = {
            "institute_name": user.institute_name,
            "name": user.name,
            "phone": user.phone,
            "cnic": user.cnic,
            "gender": user.gender,
            "username": user.username,
            "email": user.email,
            "password": hashed_password,
            "location": {
                "latitude": user.latitude,
                "longitude": user.longitude
            },
            "date_of_birth": user.date_of_birth,
            "institute_age": user.institute_age,
            "experience_years": user.experience_years,
            "technology_awareness": user.technology_awareness,
            "leadership": user.leadership,
            "communication": user.communication,
            "management": user.management,
            "motivation": user.motivation,
            "teaching_skills": user.teaching_skills,
            "promo_code": user.promo_code
        }

        result = users_collection.insert_one(new_user)

        token = create_access_token(data={
                "email": new_user["email"],
                "username": new_user["username"],
                "user_id": str(result.inserted_id)

                })
        

        user_data = {
            "email": new_user["email"],
            "username": new_user["username"],
            "user_id": str(result.inserted_id),
            "token": token
        }


        return {
            "data": user_data,
            "message": "User Signed up successfully",
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# -------------------------------
# Get School Profile Route
# -------------------------------
@user_route.get("/profile/{username}", status_code=status.HTTP_200_OK)
def get_school_profile(username: str):
    try:
        user = users_collection.find_one({"username": username})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = {
            "basic_info": {
                "school_name": user.get("institute_name"),
                "institute_details": {
                    "experience_years": user.get("experience_years"),
                    "date_of_birth": user.get("date_of_birth"),
                    "institute_age": user.get("institute_age")
                },
                "contact_info": {
                    "phone": user.get("phone"),
                    "email": user.get("email")
                },
                "profile_image": user.get("profile_image", None)
            },
            "statistics": {
                "followers": user.get("followers", 0),
                "students": user.get("students", 0),
                "following": user.get("following", 0)
            },
            "details": {
                "rank": user.get("rank", None),
                "principal": user.get("principal", None),
                "enrolled_students": user.get("enrolled_students", 0),
                "alumni": user.get("alumni", 0)
            },
            "facilities": {
                "available_facilities": user.get("available_facilities", []),
                "laboratories": user.get("laboratories", [])
            },
            "other": {
                "location": user.get("location", {}),
                "profile_badge": user.get("profile_badge", None)
            }
        }

        return {"status": "success", "data": profile}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    




# -------------------------------
# Edit School Profile Route
# -------------------------------

@user_route.put("/edit-profile/{username}",dependencies=[Depends(verify_token)],status_code=status.HTTP_200_OK)
def edit_school_profile(username: str, profile: SchoolEditProfile):

    try:
        user = users_collection.find_one({"username": username})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check unique email
        existing_email = users_collection.find_one({
            "email": profile.email,
            "_id": {"$ne": user["_id"]}
        })

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already in use")

        # Check unique username
        existing_username = users_collection.find_one({
            "username": profile.username,
            "_id": {"$ne": user["_id"]}
        })

        if existing_username:
            raise HTTPException(status_code=400, detail="Username already in use")

        update_data = {
            "institute_name": profile.institute_name,
            "bio": profile.bio,
            "gender": profile.gender,
            "date_of_institute": profile.date_of_institute,
            "phone": profile.phone,
            "email": profile.email,
            "username": profile.username,
            "profile_image": profile.profile_image,
            "location": {
                "latitude": profile.latitude,
                "longitude": profile.longitude
            }
        }

        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": update_data}
        )

        return {
            "status": "success",
            "message": "Profile updated successfully",
            "data": update_data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
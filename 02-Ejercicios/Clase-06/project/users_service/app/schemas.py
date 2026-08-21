from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
    )
    email: EmailStr


class UserResponse(UserCreate):
    id: int

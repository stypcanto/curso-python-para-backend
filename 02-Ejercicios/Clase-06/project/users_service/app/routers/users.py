from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas import (
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

users: list[dict] = []


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
):
    user = {
        "id": len(users) + 1,
        **data.model_dump(),
    }

    users.append(user)

    return user


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users():
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado",
    )

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete, update

from app.DBSettings.database import async_session_maker
from app.DBSettings.models import User
from app.DBSettings.schemas import UserCreate
from app.settings.dependencies import pwd_context, create_jwt_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register/")
async def register_user(user: UserCreate):
    async with async_session_maker() as session:
        query = select(User).filter(User.username == user.username)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return {"message": "User registered successfully"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session_maker() as session:
        query = select(User).filter(User.username == form_data.username)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user or not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = create_jwt_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_username(current_user=Depends(get_current_user)):
    async with async_session_maker() as session:
        query = select(User.username).filter(User.id == current_user["user_id"])
        result = await session.execute(query)
        username = result.scalar()
        if not username:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username}


@router.put("/update-username")
async def update_username(new_username: str, current_user=Depends(get_current_user)):
    async with async_session_maker() as session:
        query = select(User).filter(User.username == new_username)
        result = await session.execute(query)
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        update_query = (
            update(User)
            .where(User.id == current_user["user_id"])
            .values(username=new_username)
        )
        await session.execute(update_query)
        await session.commit()
        return {"message": "Username updated successfully", "new_username": new_username}


@router.delete("/delete")
async def delete_account(current_user=Depends(get_current_user)):
    async with async_session_maker() as session:
        delete_query = delete(User).where(User.id == current_user["user_id"])
        result = await session.execute(delete_query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        await session.commit()
        return {"message": "User deleted successfully"}

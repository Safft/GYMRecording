from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload
from typing import List, Dict

from app.DBSettings.database import async_session_maker
from app.DBSettings.models import ExerciseResult, ExerciseType
from app.DBSettings.schemas import (
    ExerciseResultCreate, ExerciseResultUpdate, ExerciseResultRead,
    ExerciseTypeCreate, ExerciseTypeRead
)
from app.settings.dependencies import get_current_user

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)

@router.post("/", response_model=ExerciseResultRead)
async def add_exercise(result: ExerciseResultCreate, current_user=Depends(get_current_user)):
    """Записать тренировку"""
    async with async_session_maker() as session:
        query = select(ExerciseType).filter(ExerciseType.id == result.exercise_type_id)
        result_exercise = await session.execute(query)
        exercise_type = result_exercise.scalars().first()

        if not exercise_type:
            raise HTTPException(status_code=404, detail="Exercise type not found")

        db_result = ExerciseResult(
            exercise_type_id=result.exercise_type_id,
            sets=result.sets,
            reps=result.reps,
            weight=result.weight,
            user_id=current_user["user_id"]
        )
        session.add(db_result)
        await session.commit()
        await session.refresh(db_result)

        query = select(ExerciseResult).where(ExerciseResult.id == db_result.id).options(selectinload(ExerciseResult.exercise_type))
        result = await session.execute(query)
        db_result = result.scalars().first()

        return db_result

@router.get("/", response_model=List[ExerciseResultRead])
async def get_exercises(current_user=Depends(get_current_user)):
    """Получить все тренировки пользователя"""
    async with async_session_maker() as session:
        query = select(ExerciseResult).filter(ExerciseResult.user_id == current_user["user_id"]).options(selectinload(ExerciseResult.exercise_type))
        result = await session.execute(query)
        return result.scalars().all()

@router.put("/{record_id}", response_model=ExerciseResultRead)
async def update_exercise(record_id: int, update_data: ExerciseResultUpdate, current_user=Depends(get_current_user)):
    """Обновить тренировку"""
    async with async_session_maker() as session:
        query = select(ExerciseResult).filter(ExerciseResult.id == record_id, ExerciseResult.user_id == current_user["user_id"])
        result = await session.execute(query)
        record = result.scalars().first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        update_query = update(ExerciseResult).where(ExerciseResult.id == record_id).values(
            exercise_type_id=update_data.exercise_type_id or record.exercise_type_id,
            sets=update_data.sets or record.sets,
            reps=update_data.reps or record.reps,
            weight=update_data.weight or record.weight,
        )
        await session.execute(update_query)
        await session.commit()

        query = select(ExerciseResult).where(ExerciseResult.id == record_id).options(selectinload(ExerciseResult.exercise_type))
        result = await session.execute(query)
        updated_record = result.scalars().first()

        return updated_record

@router.delete("/{record_id}")
async def delete_exercise(record_id: int, current_user=Depends(get_current_user)):
    """Удалить тренировку"""
    async with async_session_maker() as session:
        query = select(ExerciseResult).filter(ExerciseResult.id == record_id, ExerciseResult.user_id == current_user["user_id"])
        result = await session.execute(query)
        record = result.scalars().first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        await session.execute(delete(ExerciseResult).where(ExerciseResult.id == record_id))
        await session.commit()
        return {"message": "Record deleted successfully"}

@router.post("/types", response_model=ExerciseTypeRead)
async def create_exercise_type(exercise: ExerciseTypeCreate):
    """Создать новый тип упражнения"""
    async with async_session_maker() as session:
        query = select(ExerciseType).filter(ExerciseType.name == exercise.name)
        result = await session.execute(query)
        existing_exercise = result.scalars().first()

        if existing_exercise:
            raise HTTPException(status_code=400, detail="Exercise type already exists")

        db_exercise = ExerciseType(name=exercise.name)
        session.add(db_exercise)
        await session.commit()
        await session.refresh(db_exercise)
        return db_exercise

@router.get("/types", response_model=List[ExerciseTypeRead])
async def get_exercise_types():
    """Получить все доступные упражнения"""
    async with async_session_maker() as session:
        query = select(ExerciseType)
        result = await session.execute(query)
        return result.scalars().all()

@router.get("/stats", response_model=Dict[str, float])
async def get_exercise_stats(current_user=Depends(get_current_user)):
    """Получает статистику по тренировкам пользователя"""
    async with async_session_maker() as session:
        query = select(
            func.count(ExerciseResult.id).label("total_exercises"),
            func.sum(ExerciseResult.weight * ExerciseResult.reps).label("total_weight"),
            func.avg(ExerciseResult.reps).label("average_reps"),
        ).filter(ExerciseResult.user_id == current_user["user_id"])

        result = await session.execute(query)
        stats = result.fetchone()

        return {
            "total_exercises": stats.total_exercises or 0,
            "total_weight": stats.total_weight or 0,
            "average_reps": round(stats.average_reps or 0, 2),
        }
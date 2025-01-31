from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class ExerciseTypeCreate(BaseModel):
    """Схема для создания типа упражнения"""
    name: str

class ExerciseTypeRead(ExerciseTypeCreate):
    """Схема для чтения типа упражнения"""
    id: int

    class Config:
        from_attributes = True

class ExerciseResultBase(BaseModel):
    """Базовая схема тренировки"""
    sets: int
    reps: int
    weight: float

class ExerciseResultCreate(ExerciseResultBase):
    """Схема для создания тренировки"""
    exercise_type_id: int

class ExerciseResultUpdate(BaseModel):
    """Схема для обновления тренировки"""
    exercise_type_id: int | None = None
    sets: int | None = None
    reps: int | None = None
    weight: float | None = None

class ExerciseResultRead(ExerciseResultBase):
    """Схема для чтения тренировки"""
    id: int
    date: datetime
    exercise_type: ExerciseTypeRead  # 🟢 Теперь возвращается `ExerciseTypeRead`

    class Config:
        from_attributes = True

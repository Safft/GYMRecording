from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.DBSettings.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    exercises = relationship("ExerciseResult", back_populates="user")

class ExerciseType(Base):
    __tablename__ = "exercise_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class ExerciseResult(Base):
    __tablename__ = "exercise_results"
    id = Column(Integer, primary_key=True, index=True)
    exercise_type_id = Column(Integer, ForeignKey("exercise_types.id"), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="exercises")
    exercise_type = relationship("ExerciseType")

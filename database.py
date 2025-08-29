# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    fitness_goal = Column(String(100))
    dietary_preferences = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

class FitnessLog(Base):
    __tablename__ = 'fitness_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    activity_type = Column(String(50), nullable=False)
    duration = Column(Integer)  # in minutes
    calories_burned = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    meal_type = Column(String(50))
    food_item = Column(String(100), nullable=False)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plan_content = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

class NutritionPlan(Base):
    __tablename__ = 'nutrition_plans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plan_content = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

class MotivationalText(Base):
    __tablename__ = 'motivational_texts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    text_content = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    engine = create_engine('sqlite:///health_coach.db')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
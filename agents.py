# agents.py
import ollama
from datetime import datetime, timedelta
from database import get_session, FitnessLog, NutritionLog

class FitnessCoachAgent:
    def analyze_fitness_data(self, user_id, session):
        # Get last 7 days of fitness data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        logs = session.query(FitnessLog).filter(
            FitnessLog.user_id == user_id,
            FitnessLog.created_at >= start_date
        ).all()
        
        total_duration = sum(log.duration for log in logs) if logs else 0
        total_calories = sum(log.calories_burned for log in logs) if logs else 0
        activities = [log.activity_type for log in logs]
        
        prompt = f"""
        Analyze this fitness data for user {user_id}:
        - Total exercise duration last 7 days: {total_duration} minutes
        - Total calories burned: {total_calories}
        - Activities: {', '.join(activities) if activities else 'None'}
        
        Provide a brief analysis and recommendation for the next week's workout plan.
        Focus on progressive overload and variety. Be specific with exercise types, duration, and frequency.
        """
        
        try:
            response = ollama.chat(
                model='llama3',
                messages=[
                    {"role": "system", "content": "You are a professional fitness coach. Provide concise, actionable advice with specific recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating fitness analysis: {str(e)}. Please ensure Ollama is running and the llama3 model is installed."

class NutritionCoachAgent:
    def analyze_nutrition_data(self, user_id, session):
        # Get last 7 days of nutrition data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        logs = session.query(NutritionLog).filter(
            NutritionLog.user_id == user_id,
            NutritionLog.created_at >= start_date
        ).all()
        
        total_calories = sum(log.calories for log in logs) if logs else 0
        avg_daily_calories = total_calories / 7 if logs else 0
        avg_protein = sum(log.protein for log in logs) / 7 if logs else 0
        avg_carbs = sum(log.carbs for log in logs) / 7 if logs else 0
        avg_fats = sum(log.fats for log in logs) / 7 if logs else 0
        
        # Get user info for context
        user = session.query(User).filter(User.id == user_id).first()
        user_info = f"Age: {user.age}, Weight: {user.weight}kg, Height: {user.height}cm, Goal: {user.fitness_goal}" if user else ""
        
        prompt = f"""
        Analyze this nutrition data for user {user_id} ({user_info}):
        - Average daily calories: {avg_daily_calories:.2f}
        - Average daily protein: {avg_protein:.2f}g
        - Average daily carbs: {avg_carbs:.2f}g
        - Average daily fats: {avg_fats:.2f}g
        
        Provide a brief analysis and specific recommendations for a balanced nutrition plan.
        Consider macronutrient balance, meal timing, and food suggestions.
        """
        
        try:
            response = ollama.chat(
                model='llama3',
                messages=[
                    {"role": "system", "content": "You are a professional nutritionist. Provide concise, actionable advice with specific food and meal recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating nutrition analysis: {str(e)}. Please ensure Ollama is running and the llama3 model is installed."

class MotivationalAgent:
    def generate_motivational_text(self, user_id, fitness_goal, user_data=None):
        user_context = ""
        if user_data:
            user_context = f"User profile: {user_data.age} years old, {user_data.weight}kg, {user_data.height}cm. "
        
        prompt = f"""
        {user_context}Generate a short, motivational message for a user with this fitness goal: {fitness_goal}.
        Make it encouraging, personalized, and actionable. Keep it under 2 sentences.
        """
        
        try:
            response = ollama.chat(
                model='llama3',
                messages=[
                    {"role": "system", "content": "You are an enthusiastic motivational coach. Create inspiring, concise messages that encourage action."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Stay motivated and keep working towards your goal: {fitness_goal}! Error: {str(e)}"
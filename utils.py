# utils.py
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def create_fitness_chart(fitness_data):
    df = pd.DataFrame(fitness_data)
    if df.empty:
        return None
    fig = px.line(df, x='date', y='duration', title='Exercise Duration Over Time')
    return fig

def create_nutrition_chart(nutrition_data):
    df = pd.DataFrame(nutrition_data)
    if df.empty:
        return None
    fig = px.bar(df, x='date', y='calories', title='Daily Calorie Intake')
    return fig

def create_macronutrient_chart(nutrition_data):
    df = pd.DataFrame(nutrition_data)
    if df.empty:
        return None
    fig = px.line(df, x='date', y=['protein', 'carbs', 'fats'], 
                  title='Macronutrient Intake Over Time',
                  labels={'value': 'Grams', 'variable': 'Macronutrient'})
    return fig
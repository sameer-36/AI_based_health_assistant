# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import init_db, get_session, User, FitnessLog, NutritionLog, WorkoutPlan, NutritionPlan, MotivationalText
from agents import FitnessCoachAgent, NutritionCoachAgent, MotivationalAgent
from utils import create_fitness_chart, create_nutrition_chart, create_macronutrient_chart

# Initialize database
engine = init_db()
session = get_session(engine)

# Initialize AI agents
fitness_agent = FitnessCoachAgent()
nutrition_agent = NutritionCoachAgent()
motivational_agent = MotivationalAgent()

st.set_page_config(page_title="Personal Health Coach", layout="wide")

# Sidebar for user selection/creation
st.sidebar.title("User Management")
user_option = st.sidebar.radio("Choose Option", ["Existing User", "New User"])

if user_option == "New User":
    with st.sidebar.form("user_form"):
        username = st.text_input("Username")
        age = st.number_input("Age", min_value=1, max_value=120)
        weight = st.number_input("Weight (kg)", min_value=1.0)
        height = st.number_input("Height (cm)", min_value=1.0)
        fitness_goal = st.selectbox("Fitness Goal", [
            "Weight Loss", "Muscle Gain", "Maintenance", "Endurance", "General Fitness"
        ])
        dietary_preferences = st.multiselect("Dietary Preferences", [
            "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Paleo", "No Restrictions"
        ])
        
        submitted = st.form_submit_button("Create User")
        if submitted:
            new_user = User(
                username=username,
                age=age,
                weight=weight,
                height=height,
                fitness_goal=fitness_goal,
                dietary_preferences=", ".join(dietary_preferences)
            )
            session.add(new_user)
            session.commit()
            st.sidebar.success(f"User {username} created successfully!")

# Get all users for selection
users = session.query(User).all()
user_options = {user.username: user.id for user in users}

if user_options:
    selected_username = st.sidebar.selectbox("Select User", list(user_options.keys()))
    
    if selected_username:
        user_id = user_options[selected_username]
        user = session.query(User).filter(User.id == user_id).first()
        
        st.title(f"Personal Health Coach for {selected_username}")
        st.subheader(f"Goal: {user.fitness_goal}")
        
        # Display user info
        with st.expander("User Profile"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Age:** {user.age}")
                st.write(f"**Weight:** {user.weight} kg")
            with col2:
                st.write(f"**Height:** {user.height} cm")
                st.write(f"**Dietary Preferences:** {user.dietary_preferences}")
            with col3:
                st.write(f"**Goal:** {user.fitness_goal}")
                st.write(f"**Member since:** {user.created_at.date()}")
        
        # Display motivational text
        if st.button("Get Motivational Message"):
            motivational_text = motivational_agent.generate_motivational_text(user_id, user.fitness_goal, user)
            new_text = MotivationalText(
                user_id=user_id,
                text_content=motivational_text
            )
            session.add(new_text)
            session.commit()
            st.info(motivational_text)
        
        # Tabs for different functionalities
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Dashboard", "Log Activities", "Nutrition Log", "Generate Plans", "History"
        ])
        
        with tab1:
            st.header("Fitness & Nutrition Dashboard")
            
            # Get last 7 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            # Fitness data
            fitness_logs = session.query(FitnessLog).filter(
                FitnessLog.user_id == user_id,
                FitnessLog.created_at >= start_date
            ).all()
            
            if fitness_logs:
                fitness_data = [{
                    'date': log.created_at.date(),
                    'duration': log.duration,
                    'calories_burned': log.calories_burned,
                    'activity': log.activity_type
                } for log in fitness_logs]
                
                fig1 = create_fitness_chart(fitness_data)
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)
                
                # Summary statistics
                total_duration = sum(log.duration for log in fitness_logs)
                avg_duration = total_duration / len(fitness_logs)
                total_calories = sum(log.calories_burned for log in fitness_logs)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Exercise Time", f"{total_duration} minutes")
                with col2:
                    st.metric("Average Session", f"{avg_duration:.1f} minutes")
                with col3:
                    st.metric("Calories Burned", f"{total_calories:.0f}")
            else:
                st.info("No fitness data available for the last 7 days.")
            
            st.divider()
            
            # Nutrition data
            nutrition_logs = session.query(NutritionLog).filter(
                NutritionLog.user_id == user_id,
                NutritionLog.created_at >= start_date
            ).all()
            
            if nutrition_logs:
                nutrition_data = [{
                    'date': log.created_at.date(),
                    'calories': log.calories,
                    'protein': log.protein,
                    'carbs': log.carbs,
                    'fats': log.fats
                } for log in nutrition_logs]
                
                fig2 = create_nutrition_chart(nutrition_data)
                if fig2:
                    st.plotly_chart(fig2, use_container_width=True)
                
                fig3 = create_macronutrient_chart(nutrition_data)
                if fig3:
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Summary statistics
                total_calories = sum(log.calories for log in nutrition_logs)
                avg_daily_calories = total_calories / 7
                avg_protein = sum(log.protein for log in nutrition_logs) / 7
                avg_carbs = sum(log.carbs for log in nutrition_logs) / 7
                avg_fats = sum(log.fats for log in nutrition_logs) / 7
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Avg. Daily Calories", f"{avg_daily_calories:.0f}")
                with col2:
                    st.metric("Avg. Protein", f"{avg_protein:.1f}g")
                with col3:
                    st.metric("Avg. Carbs", f"{avg_carbs:.1f}g")
                with col4:
                    st.metric("Avg. Fats", f"{avg_fats:.1f}g")
            else:
                st.info("No nutrition data available for the last 7 days.")
        
        with tab2:
            st.header("Log Fitness Activity")
            with st.form("fitness_form"):
                activity_type = st.selectbox("Activity Type", [
                    "Running", "Walking", "Cycling", "Swimming", "Weight Training", 
                    "Yoga", "Pilates", "HIIT", "Other"
                ])
                duration = st.number_input("Duration (minutes)", min_value=1, max_value=300)
                calories_burned = st.number_input("Calories Burned", min_value=1)
                notes = st.text_area("Notes")
                
                submitted = st.form_submit_button("Log Activity")
                if submitted:
                    new_log = FitnessLog(
                        user_id=user_id,
                        activity_type=activity_type,
                        duration=duration,
                        calories_burned=calories_burned,
                        notes=notes
                    )
                    session.add(new_log)
                    session.commit()
                    st.success("Activity logged successfully!")
        
        with tab3:
            st.header("Log Nutrition Intake")
            with st.form("nutrition_form"):
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
                food_item = st.text_input("Food Item")
                calories = st.number_input("Calories", min_value=0)
                protein = st.number_input("Protein (g)", min_value=0.0)
                carbs = st.number_input("Carbs (g)", min_value=0.0)
                fats = st.number_input("Fats (g)", min_value=0.0)
                
                submitted = st.form_submit_button("Log Food")
                if submitted:
                    new_log = NutritionLog(
                        user_id=user_id,
                        meal_type=meal_type,
                        food_item=food_item,
                        calories=calories,
                        protein=protein,
                        carbs=carbs,
                        fats=fats
                    )
                    session.add(new_log)
                    session.commit()
                    st.success("Food logged successfully!")
        
        with tab4:
            st.header("Generate Personalized Plans")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Workout Plan")
                if st.button("Generate Workout Plan", key="workout_btn"):
                    with st.spinner("Analyzing your fitness data..."):
                        analysis = fitness_agent.analyze_fitness_data(user_id, session)
                        new_plan = WorkoutPlan(
                            user_id=user_id,
                            plan_content=analysis
                        )
                        session.add(new_plan)
                        session.commit()
                        st.success("Workout plan generated!")
                        st.write(analysis)
            
            with col2:
                st.subheader("Nutrition Plan")
                if st.button("Generate Nutrition Plan", key="nutrition_btn"):
                    with st.spinner("Analyzing your nutrition data..."):
                        analysis = nutrition_agent.analyze_nutrition_data(user_id, session)
                        new_plan = NutritionPlan(
                            user_id=user_id,
                            plan_content=analysis
                        )
                        session.add(new_plan)
                        session.commit()
                        st.success("Nutrition plan generated!")
                        st.write(analysis)
        
        with tab5:
            st.header("History")
            
            history_option = st.selectbox("View History", [
                "Fitness Logs", "Nutrition Logs", "Workout Plans", "Nutrition Plans", "Motivational Texts"
            ])
            
            if history_option == "Fitness Logs":
                logs = session.query(FitnessLog).filter(FitnessLog.user_id == user_id).order_by(FitnessLog.created_at.desc()).all()
                if logs:
                    for log in logs:
                        st.write(f"{log.created_at.date()}: {log.activity_type} for {log.duration} minutes, {log.calories_burned} calories burned")
                        if log.notes:
                            st.caption(f"Notes: {log.notes}")
                        st.divider()
                else:
                    st.info("No fitness logs found.")
            
            elif history_option == "Nutrition Logs":
                logs = session.query(NutritionLog).filter(NutritionLog.user_id == user_id).order_by(NutritionLog.created_at.desc()).all()
                if logs:
                    for log in logs:
                        st.write(f"{log.created_at.date()}: {log.meal_type} - {log.food_item}")
                        st.caption(f"Calories: {log.calories}, Protein: {log.protein}g, Carbs: {log.carbs}g, Fats: {log.fats}g")
                        st.divider()
                else:
                    st.info("No nutrition logs found.")
            
            elif history_option == "Workout Plans":
                plans = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.generated_at.desc()).all()
                if plans:
                    for plan in plans:
                        st.write(f"Generated on: {plan.generated_at.date()}")
                        st.write(plan.plan_content)
                        st.divider()
                else:
                    st.info("No workout plans found.")
            
            elif history_option == "Nutrition Plans":
                plans = session.query(NutritionPlan).filter(NutritionPlan.user_id == user_id).order_by(NutritionPlan.generated_at.desc()).all()
                if plans:
                    for plan in plans:
                        st.write(f"Generated on: {plan.generated_at.date()}")
                        st.write(plan.plan_content)
                        st.divider()
                else:
                    st.info("No nutrition plans found.")
            
            elif history_option == "Motivational Texts":
                texts = session.query(MotivationalText).filter(MotivationalText.user_id == user_id).order_by(MotivationalText.generated_at.desc()).all()
                if texts:
                    for text in texts:
                        st.write(f"Generated on: {text.generated_at.date()}")
                        st.info(text.text_content)
                        st.divider()
                else:
                    st.info("No motivational texts found.")
else:
    st.info("Please create a user first using the sidebar.")

# Add footer with instructions
st.sidebar.markdown("---")
st.sidebar.info(
    "Ensure Ollama is running with the Llama 3 model installed. "
    "Run 'ollama pull llama3' in terminal if you haven't already."
)
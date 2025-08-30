#  Personal Health Coach with Ollama & Llama 3

A comprehensive health coaching application that uses **local AI** (via [Ollama](https://ollama.ai/) with **Llama 3**) to provide personalized **fitness** and **nutrition guidance**.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?style=for-the-badge&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-0.1.2-000000?style=for-the-badge)
![Llama 3](https://img.shields.io/badge/Llama-3-FF6F00?style=for-the-badge)

---

## 🚀 Features

- 👤 **User Management**: Create and manage multiple user profiles  
- 🏋️ **Fitness Tracking**: Log and visualize exercise activities  
- 🍎 **Nutrition Tracking**: Record and analyze daily food intake  
- 🤖 **AI-Powered Analysis**: Personalized workout and nutrition plans with **Llama 3**  
- 💬 **Motivational Content**: Get encouraging, goal-based messages  
- 📊 **Data Visualization**: Interactive charts showing progress over time  
- 📜 **History Tracking**: Review past activities, plans, and motivational messages  

---

## 📦 Prerequisites

- Python **3.8+**  
- **Ollama** installed on your system  
- **Llama 3** model downloaded  

---

## ⚙️ Installation

# 1. Clone or download this project:
   ```bash
   git clone https://github.com/your-username/health-coach-app.git
   cd health-coach-app

# 2. Install the required Python packages:

pip install -r requirements.txt


# 3. Install Ollama (if not already installed):

Visit Ollama Installation Guide

Or for Linux/Mac:

curl -fsSL https://ollama.ai/install.sh | sh



# 4. Download the Llama 3 model:

ollama pull llama3




---

# ▶️ Usage

1. Start the application:

streamlit run app.py


2. Open your browser at the URL shown in the terminal (default: http://localhost:8501)


3. Use the sidebar to:

Create or select a user profile

Navigate between tabs



# 4. Tabs include:

📊 Dashboard with activity & nutrition charts

🏋️ Log fitness activities

🍽️ Record nutrition intake

🤖 Generate personalized plans

📜 Review your history





---

# 📂 Project Structure

health-coach-app/
├── app.py              # Main Streamlit application
├── database.py         # Database models and initialization
├── agents.py           # AI agents for fitness, nutrition, and motivation
├── utils.py            # Utility functions for data visualization
├── requirements.txt    # Python dependencies
└── README.md           # Documentation


---

# 🗄️ Database Schema

The app uses SQLite with these tables:

users → User profiles & preferences

fitness_logs → Exercise activity records

nutrition_logs → Food intake records

workout_plans → Generated workout plans

nutrition_plans → Generated nutrition plans

motivational_texts → Personalized motivational messages



---

# 🤖 AI Integration

Powered by Ollama with the Llama 3 model:

Fitness data analysis & workout plan generation

Nutrition data analysis & meal recommendations

Motivational text generation


✅ All AI runs locally → Full privacy, no API costs


---

# 🔧 Customization

You can customize by modifying:

agents.py → AI prompts

app.py → Add new activity or food types

utils.py → Adjust visualization styles

database.py → Extend the schema



---

# 🛠️ Troubleshooting

Ollama not found → Ensure installed and running:

ollama --version

Llama 3 model missing → Run:

ollama pull llama3

Database issues → Delete health_coach.db to reset

Port already in use → Run:

streamlit run app.py --server.port 8502

Module errors → Reinstall dependencies:

pip install -r requirements.txt



---

# 📜 License

This project is open-source


---

# 🙋 Support

Ollama Documentation

Streamlit Documentation

Meta Llama 3 Information



---

⚠️ Disclaimer: This app is for educational & informational purposes only.
Always consult healthcare professionals before making significant fitness or nutrition changes.




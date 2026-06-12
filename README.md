⬡ HR Attrition Intelligence Engine
Executive Summary
The HR Attrition Intelligence Engine is an enterprise-grade analytics platform designed to diagnose, predict, and prevent employee turnover. Built with a decoupled architecture, it combines a high-density executive frontend with a powerful Python backend powered by Machine Learning and an integrated AI Data Agent.

Instead of traditional static reports, this platform allows HR leaders to visually explore predictive churn metrics and use natural language to query their workforce data in real-time.

🌟 Core Features
Predictive ML Analytics: Utilizes a Random Forest Classifier (trained on 15,000+ records) achieving 99.1% accuracy in predicting employee flight risk based on behavioral metrics like satisfaction, project load, and evaluation scores.

AI Data Co-Pilot: Integrates a LangChain + Groq LLM agent directly into the dashboard. Executives can ask complex, contextual questions about the dataset (e.g., "What is the average satisfaction of leavers in the Sales department?") and receive immediate, data-backed answers.

Conversational Memory: The AI agent is equipped with a short-term memory buffer, allowing for fluid, multi-turn follow-up questions without losing context.

High-Density Executive UI: A responsive, light-themed corporate dashboard featuring distinct views for Headcount, Terminations, Salary Distribution, and Performance mapping, built entirely without heavy frontend frameworks.

Decoupled Architecture: Clean separation of concerns. The AI/ML brain runs securely on a FastAPI cloud server (Render), while the interactive presentation layer is hosted globally via GitHub Pages.

🏗️ Architecture & Tech Stack
Frontend (The Presentation Layer)

HTML5 / CSS3: Custom-built FinTech-style aesthetic (no Bootstrap or Tailwind).

Vanilla JavaScript: Handles state management, view toggling, and asynchronous API calls.

Chart.js: Renders complex multidimensional data (bimodal distributions, tenure cliffs, feature importance mapping).

Backend (The Intelligence Layer)

Python: Core data processing.

FastAPI / Uvicorn: High-performance RESTful API infrastructure.

Scikit-Learn: Machine learning pipeline (LabelEncoding, StandardScaling, RandomForest).

LangChain / Groq (Llama 3): Powers the Pandas Dataframe Agent and conversational logic.

Pandas: Vectorized data manipulation.

🚀 Business Impact & Insights
During exploratory data analysis, the model identified several critical risk vectors:

The Year-5 Cliff: Churn peaks dramatically at 56.6% for employees reaching 5 years of tenure.

Compensation Sensitivity: Low-salary band employees exit at 4x the rate of high earners (29.7% vs 6.6%).

Bimodal Burnout: Employees leave for two distinct reasons: extreme disengagement (low hours/low eval) and severe burnout (high hours/high eval).

The Promotion Shield: Employees who received a promotion within the last 5 years are roughly 75% less likely to leave.

⚙️ Local Setup
To run this project locally on your machine:

Clone the repository

Bash
git clone https://github.com/YOUR-USERNAME/hr-ai-dashboard.git
cd hr-ai-dashboard
Install backend dependencies

Bash
pip install -r requirements.txt
Set your Groq API Key

Create a .env file or export it directly in your terminal:

Bash
export GROQ_API_KEY="gsk_your_api_key_here"
Start the FastAPI Backend

Bash
python -m uvicorn api:app --reload
Launch the Frontend

Simply double-click the index.html file to open it in any modern web browser.

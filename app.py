import os
import json
import re
import google.generativeai as genai
import streamlit as st # <--- Import Streamlit to access Cloud Secrets

# ===========================
# 1. SMART KEY LOADER (Works on Cloud & Local)
# ===========================
try:
    # Try loading from Streamlit Cloud Secrets first
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # If that fails (running locally), load from .env file
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

# Check if key loaded
if not api_key:
    raise ValueError("❌ API Key not found! Check your .env file or Streamlit Secrets.")

genai.configure(api_key=api_key)

# Use the STABLE model to avoid Rate Limits
MODEL_NAME = 'gemini-1.5-flash' 

# ===========================
# HELPER: ROBUST JSON CLEANER
# ===========================
def clean_json(text):
    text = text.strip()
    match = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start : end + 1]
    try:
        return json.loads(text)
    except:
        return {}

# ===========================
# AGENTS
# ===========================
class ProfileAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)
    
    def analyze(self, user_input):
        # We don't print() here because it doesn't show in the browser
        prompt = f"""
        You are an expert academic counselor. 
        Analyze the following student description and extract a structured profile.
        
        STUDENT DESCRIPTION:
        "{user_input}"
        
        Return ONLY a JSON object:
        {{
            "name": "Student Name",
            "grade": "Grade Level",
            "interests": ["list", "of", "interests"],
            "academic_strengths": ["list", "of", "strengths"],
            "constraints": {{
                "budget": "low/medium/high",
                "location_preference": ["country1", "country2"]
            }}
        }}
        """
        response = self.model.generate_content(prompt)
        return clean_json(response.text)

class UniversityAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.db_context = """
        University Database:
        1. MIT (USA): High tuition, Top grades, CS/AI.
        2. Stanford (USA): High tuition, Top grades, CS/Business.
        3. University of Toronto (Canada): Medium tuition, Research/AI.
        4. TUM Munich (Germany): Low tuition, Engineering.
        5. IIT Bombay (India): Low tuition, Competitive Tech.
        6. University of Melbourne (Australia): High tuition, Research.
        7. Georgia Tech (USA): Medium-High tuition, Engineering/CS.
        8. ETH Zurich (Switzerland): Low tuition, Top Engineering.
        """
    
    def recommend(self, profile):
        prompt = f"""
        You are a university admissions consultant.
        Suggest 3 universities based on this profile.
        DATABASE: {self.db_context}
        PROFILE: {json.dumps(profile)}
        Return ONLY a JSON object:
        {{
            "reach": [{{ "name": "Uni Name", "reason": "Why it's a reach" }}],
            "target": [{{ "name": "Uni Name", "reason": "Why it fits" }}],
            "safe": [{{ "name": "Uni Name", "reason": "Why it's safe" }}]
        }}
        """
        response = self.model.generate_content(prompt)
        return clean_json(response.text)

class ActionPlanAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_plan(self, profile, uni_recommendations):
        prompt = f"""
        You are a ruthless but supportive college admissions strategist.
        Create a high-stakes action plan.
        PROFILE: {json.dumps(profile)}
        TARGET UNIS: {json.dumps(uni_recommendations)}
        Return ONLY a JSON object:
        {{
            "gap_analysis": "What is missing? (e.g., 'Low SAT' or 'No leadership')",
            "the_spike": {{ "title": "Name of unique project", "description": "What to build/do" }},
            "timeline": [
                {{ "period": "Month 1-3", "action_items": ["item 1", "item 2"] }},
                {{ "period": "Month 4-6", "action_items": ["item 1", "item 2"] }}
            ]
        }}
        """
        response = self.model.generate_content(prompt)
        return clean_json(response.text)
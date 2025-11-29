import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the model that worked for you (e.g., 'gemini-1.5-flash' or 'gemini-2.0-flash-exp')
MODEL_NAME = 'gemini-2.5-flash' 

class ProfileAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)
    
    def analyze(self, user_input):
        print("... Profile Agent is thinking ...")
        
        prompt = f"""
        You are an expert academic counselor. 
        Analyze the following student description and extract a structured profile.
        
        STUDENT DESCRIPTION:
        "{user_input}"
        
        Return ONLY a JSON object (no markdown, no ```json tags) with this structure:
        {{
            "name": "Student Name (or 'Student' if not found)",
            "grade": "Grade Level (e.g. 10, 11, 12) as integer",
            "interests": ["list", "of", "interests"],
            "academic_strengths": ["list", "of", "strengths"],
            "constraints": {{
                "budget": "low/medium/high",
                "location_preference": ["country1", "country2"]
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean up the response to ensure it's pure JSON
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:-3]
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:-3]
                
            return json.loads(clean_text)
        except Exception as e:
            return {"error": f"Failed to parse profile: {str(e)}"}
        
class UniversityAgent:
    def __init__(self):
        self.model=genai.GenerativeModel(MODEL_NAME)
        self.db_context = """
        University Database:
        1. MIT (USA): High tuition, requires Top grades, known for CS, AI, Engineering.
        2. Stanford (USA): High tuition, requires Top grades, known for CS, Business.
        3. University of Toronto (Canada): Medium tuition, known for Research, AI.
        4. TUM Munich (Germany): Low tuition, known for Engineering, requires German skills sometimes.
        5. IIT Bombay (India): Low tuition, extremely competitive (JEE), known for Tech.
        6. University of Melbourne (Australia): High tuition, known for Research.
        Carnegie Mellon University (USA): High tuition, requires strong academics, known for CS, Robotics, AI.

        7.UC Berkeley (USA): High tuition, highly competitive, known for CS, Engineering, Research.

        8.Georgia Tech (USA): Medium-high tuition, competitive, known for Engineering, CS.

        9.Harvard University (USA): High tuition, requires top grades, known for Research, Business, CS.

        10.University of Cambridge (UK): High tuition (for internationals), requires excellent grades, known for Engineering, AI, Research.

        11.University of Oxford (UK): High tuition, very competitive, known for Mathematics, CS, Research.

        12.ETH Zürich (Switzerland): Low tuition, very competitive, known for Engineering, Robotics, Research.

        13.EPFL Lausanne (Switzerland): Low tuition, research-focused, known for Engineering, AI.

        14.National University of Singapore (NUS): Medium tuition, competitive, known for CS, Engineering, Research.

        15.Nanyang Technological University (NTU), Singapore: Medium tuition, strong in AI, Engineering, Research.

        16.University of Waterloo (Canada): Medium tuition, known for CS, Co-op programs, Engineering.

        17.McGill University (Canada): Medium tuition, research-oriented, strong in Engineering, CS.

        19.KTH Royal Institute of Technology (Sweden): Low tuition (EU), known for Engineering, CS.

        20.Seoul National University (South Korea): Low tuition, very competitive, known for Engineering, CS.

        21.KAIST (South Korea): Low tuition, top-tier science and tech institute, strong in AI, Robotics.

        22.University of Sydney (Australia): High tuition, known for Research, Engineering.
        """
    def recommend(self, profile):
        print(". . University Agent is searching for the best universities ..")
        prompt = f"""
        You are a university admissions consultant.
        Based on the database below and the student profile, suggest 3 universities.
        Classify them as:
        - REACH (Hard to get in)
        - TARGET (Good match)
        - SAFE (Likely to get in)

        DATABASE:
        {self.db_context}

        STUDENT PROFILE:
        {json.dumps(profile)}

        Return ONLY a JSON object with this structure:
        {{
            "reach": [{{ "name": "Uni Name", "reason": "Why it's a reach" }}],
            "target": [{{ "name": "Uni Name", "reason": "Why it fits" }}],
            "safe": [{{ "name": "Uni Name", "reason": "Why it's safe" }}]
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            clean_text = response.text.strip()
            # Clean json markdown if present
            if clean_text.startswith("```json"): clean_text = clean_text[7:-3]
            elif clean_text.startswith("```"): clean_text = clean_text[3:-3]
            return json.loads(clean_text)
        except Exception as e:
            return {"error": f"Failed to recommend universities: {str(e)}"}

# --- Quick Test Block ---
if __name__ == "__main__":
    # 1. Test Profile Agent
    profile_agent = ProfileAgent()
    user_input = "I have really good grades, straight As. I want to study CS in the USA but money is no object."
    print(f"\n📝 INPUT: {user_input}\n")
    
    profile = profile_agent.analyze(user_input)
    print("✅ Extracted Profile:")
    print(json.dumps(profile, indent=2))
    
    # 2. Test University Agent (Uses the profile we just extracted)
    uni_agent = UniversityAgent()
    recommendations = uni_agent.recommend(profile)
    
    print("\n✅ University Recommendations:")
    print(json.dumps(recommendations, indent=2))
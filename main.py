import streamlit as st
import json
from agents import ProfileAgent, UniversityAgent, ActionPlanAgent

st.set_page_config(page_title="SetLife-AI", page_icon="🎓", layout="wide")

st.title("🎓 SetLife-AI: Your AI Academic Counselor")
st.markdown("### From Confusion to Capstone in Minutes")

with st.sidebar:
    st.header("1. Your Profile")
    st.info("The more details you give, the sharper the strategy.")

    academics = st.text_area("Academic Stats", placeholder="Grade 11, GPA 3.8/4.0, SAT 1450(if applicable), Branch")
    interests = st.text_area("Interests", placeholder="I built a chess bot, I lead the debate club, I want to study AI.")
    budget = st.selectbox("What is your yearly tuition budget?", 
                      ["Low (< $10k)", "Medium ($10k - $40k)", "High (>$40k)", "Scholarship Required"])
    preferences = st.text_area("Preferences", placeholder="Budget: Medium, Location: USA/Canada, Financial Aid: Required")
    submit_btn = st.button("🚀 Build My Plan")

    # 4. Main Logic
if submit_btn:
    if not academics or not interests:
        st.error("Please fill in at least Academics and Interests!")
    else:
        # --- GLUE THE INPUTS TOGETHER ---
        # This solves your data quality issue
        full_user_prompt = f"""
        ACADEMICS: {academics}
        INTERESTS: {interests}
        BUDGET CONSTRAINT: {budget}
        PREFERENCES: {preferences}
        """

        # --- PHASE 1: PROFILE AGENT ---
        with st.spinner("🕵️ Analyzing your profile..."):
            try:
                profile_agent = ProfileAgent()
                profile = profile_agent.analyze(full_user_prompt)
            except Exception as e:
                st.error(f"Agent Error: {e}")
                st.stop()
        
        # Display Profile
        with st.expander("✅ Phase 1: Analyzed Profile", expanded=False):
            st.json(profile)

        # --- PHASE 2: UNIVERSITY AGENT ---
        with st.spinner("🏫 Researching universities..."):
            uni_agent = UniversityAgent()
            unis = uni_agent.recommend(profile)
        
        # Display Universities in Columns
        st.subheader("2. University Recommendations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Target")
            for u in unis.get("target", []):
                st.success(f"**{u['name']}**\n\n*{u['reason']}*")
        
        with col2:
            st.markdown("### 🚀 Reach")
            for u in unis.get("reach", []):
                st.warning(f"**{u['name']}**\n\n*{u['reason']}*")
        
        with col3:
            st.markdown("### 🛡️ Safe")
            for u in unis.get("safe", []):
                st.info(f"**{u['name']}**\n\n*{u['reason']}*")

        # --- PHASE 3: ACTION PLAN AGENT ---
        with st.spinner("📝 Drafting strategic plan..."):
            plan_agent = ActionPlanAgent()
            plan = plan_agent.generate_plan(profile, unis)
        
        st.divider()
        st.subheader("3. Strategic Action Plan")
        
        # Gap Analysis
        st.markdown(f"**⚠️ Gap Analysis:** {plan.get('gap_analysis', 'No analysis available')}")
        
        # The Spike
        spike = plan.get('the_spike', {})
        st.markdown(f"###  Recommended 'Spike' Project: {spike.get('title', 'Project')}")
        st.markdown(f"> {spike.get('description', 'No description')}")
        
        # Timeline
        st.markdown("### 📅 Execution Timeline")
        for period in plan.get('timeline', []):
            with st.container():
                st.markdown(f"**{period.get('period', 'Time')}** - *{period.get('focus', 'Focus')}*")
                for item in period.get('action_items', []):
                    st.markdown(f"- {item}")
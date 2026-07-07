import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load local environment variables for API keys
load_dotenv()

# Initialize OpenAI client (Make sure OPENAI_API_KEY is in your .env file)
# If deploying to Streamlit Cloud, add this to secrets instead
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

st.set_page_config(page_title="Go-Live Risk Simulator", layout="centered")

st.title("🚀 Go-Live Decision Risk Simulator")
st.subheader("An AI-Powered Software Deployment Risk Framework")

st.markdown("""
Evaluate technical readiness against business urgency. This simulator uses a composite risk formula layered with generative AI to simulate launch post-mortems.
""")

st.sidebar.header("🔧 Project Metrics")

# --- INPUTS ---
test_coverage = st.sidebar.slider("Test Coverage (%)", 0, 100, 80)
critical_bugs = st.sidebar.slider("Open Critical/Blocker Bugs", 0, 10, 2)
team_fatigue = st.sidebar.slider("Team Fatigue Level (%)", 0, 100, 40)
rollback_readiness = st.sidebar.slider("Rollback Automation Readiness (%)", 0, 100, 90)
business_urgency = st.sidebar.selectbox("Business Urgency / Market Pressure", ["Low", "Medium", "High"])

# --- DETERMINISTIC RISK ENGINE ---
# Basic formula adjusting for technical risks scaled by rollback capabilities
urgency_multipliers = {"Low": 1.0, "Medium": 1.2, "High": 1.5}
defect_penalty = critical_bugs * 15
coverage_gap = 100 - test_coverage

base_risk = (coverage_gap + defect_penalty + (team_fatigue * 0.5)) * urgency_multipliers[business_urgency]
mitigated_risk = base_risk * (1 - (rollback_readiness / 100))
final_score = min(max(int(mitigated_risk), 0), 100) # Clamp between 0 and 100

# --- DISPLAY RESULTS ---
st.write("---")
st.metric(label="Calculated Deployment Risk Score", value=f"{final_score}%")

if final_score < 35:
    st.success("🟢 STATUS: SAFE TO LAUNCH. Proceed with standard deployment protocols.")
elif final_score < 65:
    st.warning("🟡 STATUS: PROCEED WITH CAUTION. Heightened monitoring required.")
else:
    st.error("🔴 STATUS: HARD STOP / ABORT. Risk profile exceeds safe deployment thresholds.")

# --- AI SIMULATION LAYER ---
st.write("---")
st.subheader("🤖 AI Chaos Engineering Simulation")

if st.button("Simulate Launch Outcome"):
    if not client:
        st.info("💡 To generate AI narratives, add your `OPENAI_API_KEY` to the environment variables. Showing fallback mock response:")
        st.write("*Mock Outcome: The system launched successfully, but high team fatigue resulted in a delayed response to a minor database connection pool exhaustion at 2 AM.*")
    else:
        with st.spinner("AI is analyzing architecture states and simulating deployment chaos..."):
            prompt = f"""
            Act as an elite DevOps Architect and Site Reliability Engineer (SRE). 
            Analyze this deployment state and generate a realistic, dramatic 3-paragraph story of what happens over the next 24 hours if this team presses 'Go-Live'.
            
            Metrics:
            - Test Coverage: {test_coverage}%
            - Open Critical Bugs: {critical_bugs}
            - Team Fatigue: {team_fatigue}%
            - Rollback Readiness: {rollback_readiness}%
            - Market Urgency: {business_urgency}
            - Risk Score Calculated: {final_score}%
            
            Be highly technical, realistic, and brutally honest about the consequences of these metrics.
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating AI response: {e}")

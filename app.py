import streamlit as st
import os
import pickle
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

st.set_page_config(page_title="Pro Go-Live ML Simulator", layout="centered")
st.title("🚀 Go-Live Decision Risk Simulator (ML Pro Edition)")

# Load the trained machine learning model
@st.cache_resource
def load_ml_model():
    if os.path.exists("deployment_model.pkl"):
        with open("deployment_model.pkl", "rb") as f:
            return pickle.load(f)
    return None

model = load_ml_model()

# --- SIDEBAR INPUTS ---
st.sidebar.header("🔧 Live Project Metrics")
test_coverage = st.sidebar.slider("Test Coverage (%)", 0, 100, 80)
critical_bugs = st.sidebar.slider("Open Critical/Blocker Bugs", 0, 10, 2)
team_fatigue = st.sidebar.slider("Team Fatigue Level (%)", 0, 100, 40)
rollback_readiness = st.sidebar.slider("Rollback Automation Readiness (%)", 0, 100, 90)
urgency_label = st.sidebar.selectbox("Business Urgency / Market Pressure", ["Low", "Medium", "High"])

# Map urgency labels back to numerical values used during training
urgency_mapping = {"Low": 1.0, "Medium": 1.2, "High": 1.5}
urgency_val = urgency_mapping[urgency_label]

# --- ML PREDICTION ENGINE ---
st.write("---")
if model is None:
    st.error("⚠️ Pre-trained machine learning model binary (`deployment_model.pkl`) not found. Please execute `train_model.py` first to initialize your weights.")
else:
    # Package input data into a single-row DataFrame matching training layout
    input_data = pd.DataFrame([{
        'test_coverage': test_coverage,
        'critical_bugs': critical_bugs,
        'team_fatigue': team_fatigue,
        'rollback_readiness': rollback_readiness,
        'business_urgency': urgency_val
    }])
    
    # Extract prediction probability of class 1 (Failure/Incident)
    failure_probability = model.predict_proba(input_data)[0][1]
    final_score = int(failure_probability * 100)
    
    # Display Score Metric
    st.metric(label="ML-Predicted Production Incident Probability", value=f"{final_score}%")
    
    # 🛑 Rule-Based Hard Gates Guardrail (SRE best practice combined with ML)
    if test_coverage < 50 or critical_bugs > 0:
        st.error(f"🔴 STATUS: HARD STOP / ABORT. Gatekeeper Rule Triggered: Unresolved critical defects or sub-standard test coverage override predicted metrics.")
    elif final_score < 35:
        st.success("🟢 STATUS: SAFE TO LAUNCH. Predictive algorithms show nominal historical production risk indicators.")
    elif final_score < 65:
        st.warning("🟡 STATUS: PROCEED WITH CAUTION. Heightened anomaly monitoring and active on-call staffing required.")
    else:
        st.error("🔴 STATUS: HARD STOP / ABORT. High risk vector calculation detected by ML model.")

# --- AI SIMULATION LAYER ---
st.write("---")
st.subheader("🤖 AI Chaos Engineering Simulation")

if st.button("Simulate Launch Outcome"):
    if not client:
        st.info("💡 Supply an active `OPENAI_API_KEY` to run custom LLM workflows.")
    else:
        with st.spinner("AI is evaluating model inference vectors..."):
            prompt = f"""
            Act as an elite DevOps Architect and Site Reliability Engineer (SRE). 
            Analyze this deployment state and generate a realistic, dramatic 3-paragraph story of what happens over the next 24 hours if this team presses 'Go-Live'.
            
            Metrics & ML Inference Indicators:
            - Test Coverage: {test_coverage}%
            - Open Critical Bugs: {critical_bugs}
            - Team Fatigue: {team_fatigue}%
            - Rollback Readiness: {rollback_readiness}%
            - Market Urgency: {urgency_label}
            - ML Calculated Failure Probability: {final_score}%
            
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
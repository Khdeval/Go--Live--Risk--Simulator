# Go-Live Decision Risk Simulator

An interactive, data-driven release management framework designed to remove subjectivity and "gut feelings" from production deployment decisions. This application blends deterministic Site Reliability Engineering (SRE) metric equations with a Generative AI predictive pipeline to simulate production deployment risks, isolate architectural bottlenecks, and model realistic post-mortem scenarios.

🔗 **Live Application:**
---

## 📌 Project Overview

In the Software Development Lifecycle (SDLC), engineering teams constantly face intense friction: **balancing market-driven business urgency against systemic operational risk.** 

The **Go-Live Decision Risk Simulator** establishes an automated gatekeeping framework to evaluate a release candidate's readiness. By inputting key variables across technical metrics, team dynamics, and mitigation capabilities, the simulator quantifies the deployment safety margin and uses an LLM to generate predictive chaos engineering narratives.

### 🧩 Key Features
* **Composite Risk Engine:** Formulates real-time deployment risk percentages by calculating technical debt, bug density, and human capital fatigue.
* **Predictive AI SRE Layer:** Integrates an LLM pipeline that analyzes conflicting metric combinations to act as a virtual Site Reliability Engineer, providing a structural critique of the deployment state.
* **Chaos Engineering Narratives:** Dynamically generates complex, technically accurate "24-hour post-mortem" scenarios detailing the exact operational friction, memory leaks, or cascade failures a team would encounter post-launch.
* **Release Gate Visualizations:** Automatically maps inputs to hard operational thresholds (`Safe to Launch`, `Heightened Monitoring`, or `Hard Stop / Abort`) to streamline stakeholder alignment.

---

## 🧠 Core Architecture & Methodology

The application relies on a dual-engine architecture:
[User Interface (Streamlit)]
│
├──► [Deterministic Risk Engine] ──► Calculates Risk Score (0-100%)
│                                     └──► Maps to Gate Status (Green/Yellow/Red)
│
└──► [Generative AI Prompt Engine] ──► Restructures Metrics into Prompt
└──► OpenAI/Gemini API ──► Chaos Narrative
### 🧮 The Risk Calculation Logic
The deterministic engine models baseline structural risk multiplied by business urgency, offset by operational resilience coefficients:

$$\text{Deployment Risk} = f(\text{Coverage Gaps}, \text{Defect Density}, \text{Human Fatigue}) \times (1 - \text{Rollback Readiness})$$

* **Technical Debt & Defects:** Open blocker bugs apply an exponential penalty to the score, modeling the compounding nature of unpatched edge cases in production.
* **The Human Vector:** Incorporates team fatigue percentages to simulate higher human-error rates during high-stress off-hours deployments.
* **The Resilience Offset:** High rollback playbook and automation readiness act as a heavy mitigation factor, reducing the mathematical probability of a catastrophic, unrecoverable outage.

---

## 🛠️ Tech Stack & Dependencies

* **Frontend/UI:** Streamlit (Python-native web framework)
* **Logic/Calculations:** Pure Python 3.10+
* **AI Orchestration:** OpenAI API / Structured Prompt Engineering
* **Environment Management:** Python-dotenv

---

## ⚙️ Installation & Local Setup

### Prerequisites
* Python 3.10 or higher installed.
* An OpenAI API Key (or alternative LLM API provider setup).

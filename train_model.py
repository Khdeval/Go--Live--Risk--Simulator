import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

print("🤖 Generating historical deployment data...")
np.random.seed(42)
n_samples = 1000

# Generate realistic random features
test_coverage = np.random.uniform(40, 100, n_samples)
critical_bugs = np.random.randint(0, 6, n_samples)
team_fatigue = np.random.uniform(10, 100, n_samples)
rollback_readiness = np.random.uniform(20, 100, n_samples)
business_urgency = np.random.choice([1.0, 1.2, 1.5], n_samples) # Low, Med, High multiplier

# Create a ground-truth hidden formula for probability of failure
# High bugs, low coverage, high fatigue, and high urgency increase failure. High rollback decreases it slightly.
fail_probability = (
    (100 - test_coverage) * 0.3 + 
    (critical_bugs * 15) + 
    (team_fatigue * 0.2)
) * business_urgency * (1 - (rollback_readiness * 0.002))

# Normalize probability between 0 and 1
fail_probability = np.clip(fail_probability / 100, 0, 1)

# Target: 1 = Failed Deployment (Incident), 0 = Success
was_incident = np.random.binomial(1, fail_probability)

# Construct DataFrame
df = pd.DataFrame({
    'test_coverage': test_coverage,
    'critical_bugs': critical_bugs,
    'team_fatigue': team_fatigue,
    'rollback_readiness': rollback_readiness,
    'business_urgency': business_urgency,
    'was_incident': was_incident
})

# Train-Test Split
X = df.drop('was_incident', axis=1)
y = df['was_incident']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest Risk Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate Accuracy
accuracy = model.score(X_test, y_test)
print(f"Model trained successfully! Test Accuracy: {accuracy:.2%}")

# Save the trained model binary
with open("deployment_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved as 'deployment_model.pkl'")
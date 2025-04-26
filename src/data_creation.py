# 1_data_creation.py
# Updated to ensure all clients are age 20 or older

import os
import random
import pandas as pd
from faker import Faker
from datetime import date, timedelta

fake = Faker()

# Create necessary folders
os.makedirs('data/client_documents', exist_ok=True)
os.makedirs('data/compliance_policies', exist_ok=True)
os.makedirs('data/structured_data', exist_ok=True)

# 1. Generate Dummy Client Documents (with age >= 20)
today = date.today()
max_birth_date = today - timedelta(days=365 * 20)  # Ensure at least 20 years old

for i in range(30):
    dob = fake.date_of_birth(minimum_age=20, maximum_age=80)  # Enforce 20+
    doc_text = f"""
    Client Name: {fake.name()}
    Date of Birth: {dob}
    Address: {fake.address()}
    Income: ${random.randint(30000, 200000)}
    Employment Status: {random.choice(['Employed', 'Self-employed', 'Unemployed'])}
    ID Number: {fake.ssn()}
    """
    with open(f"data/client_documents/client_doc_{i+1}.txt", 'w') as f:
        f.write(doc_text)

print("✅ Dummy client documents created (age >= 20).")

# 2. Generate Dummy Compliance Policies
compliance_topics = [
    "Client address verification",
    "Income verification thresholds",
    "Employment status proof",
    "ID authenticity requirements",
    "High-risk client identification",
    "PEP (Politically Exposed Persons) screening rules",
    "AML (Anti-Money Laundering) reporting thresholds"
]

for i, topic in enumerate(compliance_topics):
    policy_text = f"""
    Policy Topic: {topic}

    Details:
    - Clients must provide proof of address no older than 3 months.
    - Minimum income for premium products: $75,000/year.
    - Self-employed clients must provide 2 years of tax returns.
    - IDs must be government-issued and unexpired.
    - Clients flagged as High-Risk must undergo Enhanced Due Diligence.
    - All PEPs must be reported to the compliance team.
    - AML reports must be filed for transactions above $10,000.
    """
    with open(f"data/compliance_policies/policy_{i+1}.txt", 'w') as f:
        f.write(policy_text)

print("✅ Dummy compliance policies created.")

# 3. Generate Structured Dummy Data for ML Model
records = []
for _ in range(1000):
    income = random.randint(30000, 200000)
    employment_status = random.choice(['Employed', 'Self-employed', 'Unemployed'])
    id_valid = random.choice([1, 0])
    address_valid = random.choice([1, 0])
    high_risk_flag = random.choice([1, 0])

    risk_score = 0

    if income < 60000:
        risk_score += random.uniform(0.3, 0.5)
    if employment_status == 'Unemployed':
        risk_score += random.uniform(0.2, 0.4)
    if id_valid == 0:
        risk_score += random.uniform(0.3, 0.5)
    if high_risk_flag == 1:
        risk_score += random.uniform(0.2, 0.4)

    # Add noise
    risk_score += random.uniform(-0.1, 0.1)

    # Final risk label
    risk_category = 'High Risk' if risk_score > 0.6 else 'Low Risk'

    # Inject noise
    if random.random() < 0.05:
        risk_category = 'High Risk' if risk_category == 'Low Risk' else 'Low Risk'

    records.append({
        'income': income,
        'employment_status': employment_status,
        'id_valid': id_valid,
        'address_valid': address_valid,
        'high_risk_flag': high_risk_flag,
        'risk_category': risk_category
    })

df = pd.DataFrame(records)
df.to_csv('data/structured_data/client_data.csv', index=False)

print("✅ Dummy structured client data (with noise) created.")

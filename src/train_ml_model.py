# 4_train_ml_model.py
# Train a machine learning model to predict client risk category
# Log everything to MLflow, including AUROC

import pandas as pd
import mlflow
import mlflow.sklearn
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

# Load the structured data
data_path = 'data/structured_data/client_data.csv'
df = pd.read_csv(data_path)

# Encode categorical variables
df['employment_status'] = df['employment_status'].map({
    'Employed': 0,
    'Self-employed': 1,
    'Unemployed': 2
})

df['risk_category'] = df['risk_category'].map({
    'Low Risk': 0,
    'High Risk': 1
})

# Prepare features and labels
X = df[['income', 'employment_status', 'id_valid', 'address_valid', 'high_risk_flag']]
y = df['risk_category']

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Setup MLflow experiment
mlflow.set_experiment('compliance_risk_prediction')

with mlflow.start_run():
    # Train a Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Predict
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]  # Probabilities for positive class

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    auroc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=True)

    print(f"Accuracy: {acc}")
    print(f"AUROC: {auroc}")
    print(classification_report(y_test, y_pred))

    # Log parameters, metrics, and model to MLflow
    mlflow.log_param('model_type', 'RandomForest')
    mlflow.log_metric('accuracy', acc)
    mlflow.log_metric('auroc', auroc)

    # Save model
    model_path = 'models/compliance_risk_model'
    os.makedirs('models', exist_ok=True)
    mlflow.sklearn.save_model(clf, path=model_path)

    print(f"Model saved at {model_path}")

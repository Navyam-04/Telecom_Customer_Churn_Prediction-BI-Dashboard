
# Churn Prediction using Random Forest - Python Script

# ================================================
# Step 1: Import Libraries & Load Data
# ================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

# Load training data
file_path = r"C:\yourpath\Prediction_Data.xlsx"
sheet_name = 'vw_ChurnData'
data = pd.read_excel(file_path, sheet_name=sheet_name)
print(data.head())

# ================================================
# Step 2: Data Preprocessing
# ================================================
# Drop non-predictive columns
data = data.drop(['Customer_ID', 'Churn_Category', 'Churn_Reason'], axis=1)

# Encode categorical variables
columns_to_encode = [
    'Gender', 'Married', 'State', 'Value_Deal', 'Phone_Service', 'Multiple_Lines',
    'Internet_Service', 'Internet_Type', 'Online_Security', 'Online_Backup',
    'Device_Protection_Plan', 'Premium_Support', 'Streaming_TV', 'Streaming_Movies',
    'Streaming_Music', 'Unlimited_Data', 'Contract', 'Paperless_Billing',
    'Payment_Method'
]

label_encoders = {}
for column in columns_to_encode:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Encode target variable
data['Customer_Status'] = data['Customer_Status'].map({'Stayed': 0, 'Churned': 1})

# Split into features and target
X = data.drop('Customer_Status', axis=1)
y = data['Customer_Status']

# Split into train-test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ================================================
# Step 3: Train Random Forest Model
# ================================================
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# ================================================
# Step 4: Evaluate Model
# ================================================
y_pred = rf_model.predict(X_test)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature Importance Plot
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(15, 6))
sns.barplot(x=importances[indices], y=X.columns[indices])
plt.title('Feature Importances')
plt.xlabel('Relative Importance')
plt.ylabel('Feature Names')
plt.show()

# ================================================
# Step 5: Use Model for Prediction on New Data
# ================================================
sheet_name = 'vw_JoinData'
new_data = pd.read_excel(file_path, sheet_name=sheet_name)
print(new_data.head())

# Keep original data for output
original_data = new_data.copy()
customer_ids = new_data['Customer_ID']

# Drop non-predictive columns
new_data = new_data.drop(['Customer_ID', 'Customer_Status', 'Churn_Category', 'Churn_Reason'], axis=1)

# Encode using saved encoders
for column in new_data.select_dtypes(include=['object']).columns:
    new_data[column] = label_encoders[column].transform(new_data[column])

# Predict
new_predictions = rf_model.predict(new_data)
original_data['Customer_Status_Predicted'] = new_predictions

# Filter predicted churners
original_data = original_data[original_data['Customer_Status_Predicted'] == 1]

# Save output
original_data.to_csv(r"C:\yourpath\Predictions.csv", index=False)

import pandas as pd
from  Load_Data import load_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# Load the data using the reusable function
data = load_data()

# Predicting If a Customer Will Use a Promo Code

# Feature engineering
data['Used_Promo'] = (data['Promo Code Used'] == 'Yes').astype(int)
features = ['Previous Purchases', 'Purchase Amount (USD)']  # example features
X = data[features]
y = data['Used_Promo']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
print("Accuracy:", clf.score(X_test, y_test))



#  assume frequent purchasers are likely to purchase next month
data['Likely_To_Purchase_Next_Month'] = data['Frequency of Purchases'].apply(
    lambda x: 1 if x in ['Weekly', 'Monthly'] else 0
)

# --- Step 2: Feature Engineering ---
data['Used_Discount'] = (data['Discount Applied'] == 'Yes').astype(int)
data['Used_Promo'] = (data['Promo Code Used'] == 'Yes').astype(int)

# Select relevant features
features = ['Previous Purchases', 'Purchase Amount (USD)', 'Used_Discount', 'Used_Promo']
X = data[features]
y = data['Likely_To_Purchase_Next_Month']

# --- Step 3: Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 4: Train Model ---
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# --- Step 5: Evaluate ---
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))


## Customer Churn Rate
# Customers not likely to purchase next month are considered churned
churned = data['Likely_To_Purchase_Next_Month'] == 0
churn_rate = churned.mean() * 100

print(f"Churn Rate: {churn_rate:.2f}%")


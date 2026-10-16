
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load the dataset
data = pd.read_csv("data/network_cases.csv")

# 2. Separate features and target
X = data.drop("fault", axis=1)
y = data["fault"]

print("Features:")
print(X.head())

print("\nTarget labels:")
print(y.head())

# 3. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nTraining examples:", len(X_train))
print("Testing examples:", len(X_test))

# 4. Create the ML model
model = DecisionTreeClassifier(random_state=42)

# 5. Train the model
model.fit(X_train, y_train)

# 6. Predict on the testing data
y_pred = model.predict(X_test)

# 7. Evaluate the model
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 8. Save the trained model
joblib.dump(model, "network_model.pkl")
print("\nModel saved successfully!")

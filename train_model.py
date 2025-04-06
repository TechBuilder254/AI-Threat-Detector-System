import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Example data: Replace this with actual feature data (e.g., open ports, unique services, etc.)
X = pd.DataFrame({
    'open_ports': [5, 8, 12, 6, 9, 3, 7, 4, 10, 11],  # Example feature: number of open ports
    'unique_services': [3, 4, 5, 3, 4, 1, 2, 3, 5, 6]  # Example feature: number of unique services
})

y = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0]  # Labels: 0 = Safe, 1 = Threat (example)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model
model_filename = 'model/threat_model.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)

# Evaluate the model (optional)
y_pred = model.predict(X_test)
print(f"Model accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Model saved as {model_filename}")

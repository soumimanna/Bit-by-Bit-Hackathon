import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# --- 1. Load and Prepare the Data ---
print("Loading feature dataset...")
df = pd.read_csv("features.csv")

# Handle potential missing values
if df.isnull().sum().sum() > 0:
    df = df.fillna(df.mean(numeric_only=True))

# Separate features (X) from the target label (y)
X = df.drop(columns=['model', 'run'])
y_str = df['model']

# Encode string labels into numbers
le = LabelEncoder()
y = le.fit_transform(y_str)

# --- 2. PCA Visualization for Model Separability ---
print("\nGenerating PCA plot to visualize model separation...")
# Scale features for PCA, as it's sensitive to feature scales
X_scaled = StandardScaler().fit_transform(X)

# Reduce dimensions to 2 for plotting
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)

# Create a DataFrame for plotting
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pca_df['model'] = y_str

# Plotting
plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='PC1', y='PC2',
    hue='model',
    palette=sns.color_palette("hsv", n_colors=len(df['model'].unique())),
    data=pca_df,
    s=100, # Marker size
    alpha=0.8
)
plt.title('Model Fingerprints in 2D Feature Space (PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid()
plt.legend(title='CNN Model')
plt.savefig('pca_model_separation.png')
print("PCA plot saved as 'pca_model_separation.png'")


# --- 3. Prediction Confidence Analysis ---
print("\nAnalyzing model prediction confidence...")
# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train the same Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Get prediction probabilities on the test set
probabilities = model.predict_proba(X_test)

# For each prediction, find the confidence score of the TRUE class
confidence_scores = []
for i, true_label_index in enumerate(y_test):
    confidence = probabilities[i][true_label_index]
    confidence_scores.append(confidence)

# Create a DataFrame to analyze the results
results_df = pd.DataFrame({
    'model_name': le.inverse_transform(y_test),
    'confidence': confidence_scores
})

# Calculate the average confidence for each model
avg_confidence = results_df.groupby('model_name')['confidence'].mean().sort_values(ascending=False)

print("\n--- Average Prediction Confidence per Model ---")
print(avg_confidence.to_string())
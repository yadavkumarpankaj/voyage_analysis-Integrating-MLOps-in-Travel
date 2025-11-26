"""
Training script for Gender Classification Model
Generates: scaler.pkl, pca.pkl, tuned_logistic_regression_model.pkl
"""
import pandas as pd
import numpy as np
import pickle
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sentence_transformers import SentenceTransformer

print("🚀 Training Gender Classification Model...")
print("=" * 60)

# Step 1: Create sample data if users.csv doesn't exist
import os
if not os.path.exists("data/users.csv"):
    print("\n📊 Creating sample users.csv data...")
    os.makedirs("data", exist_ok=True)
    
    # Generate realistic sample data
    np.random.seed(42)
    n_samples = 1000
    
    # Sample names (gender-typical for better model training)
    male_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 
                  'Thomas', 'Charles', 'Daniel', 'Matthew', 'Mark', 'Donald', 'Anthony', 'Paul',
                  'Steven', 'Andrew', 'Kenneth', 'Joshua', 'Kevin', 'Brian', 'George', 'Edward']
    female_names = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan',
                    'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa', 'Betty', 'Margaret', 'Sandra',
                    'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle', 'Dorothy', 'Carol',
                    'Amanda', 'Melissa']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas',
                  'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris']
    
    companies = ['Acme Factory', 'Wonka Company', 'Monsters CYA', 'Umbrella LTDA', '4You']
    
    data = []
    for i in range(n_samples):
        gender = np.random.choice(['male', 'female'], p=[0.5, 0.5])
        if gender == 'male':
            first_name = np.random.choice(male_names)
        else:
            first_name = np.random.choice(female_names)
        last_name = np.random.choice(last_names)
        name = f"{first_name} {last_name}"
        company = np.random.choice(companies)
        age = np.random.randint(21, 66)
        
        data.append({
            'code': i,
            'company': company,
            'name': name,
            'gender': gender,
            'age': age
        })
    
    user_df = pd.DataFrame(data)
    user_df.to_csv("data/users.csv", index=False)
    print(f"   ✓ Created data/users.csv with {len(user_df)} records")
else:
    print("\n📊 Loading users.csv...")
    user_df = pd.read_csv("data/users.csv")
    print(f"   ✓ Loaded {len(user_df)} records")

# Step 2: Filter data (only male and female, exclude 'none')
print("\n🔍 Filtering data...")
user_df_filtered = user_df[(user_df['gender'] == 'male') | (user_df['gender'] == 'female')].copy()
print(f"   ✓ Filtered to {len(user_df_filtered)} records (male/female only)")

# Step 3: Encode gender
print("\n🔄 Encoding target variable...")
label_encoder_gender = LabelEncoder()
user_df_filtered['gender_encoded'] = label_encoder_gender.fit_transform(user_df_filtered['gender'])
print(f"   ✓ Gender encoding: {dict(zip(label_encoder_gender.classes_, label_encoder_gender.transform(label_encoder_gender.classes_)))}")

# Step 4: Initialize SentenceTransformer
print("\n🤖 Loading SentenceTransformer model...")
print("   (This may take a few minutes on first run - downloading model)")
try:
    sentence_model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
    print("   ✓ SentenceTransformer loaded")
except Exception as e:
    print(f"   ❌ Error loading SentenceTransformer: {e}")
    print("   Installing sentence-transformers...")
    import subprocess
    subprocess.check_call(["pip", "install", "sentence-transformers", "--quiet"])
    sentence_model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
    print("   ✓ SentenceTransformer loaded")

# Step 5: Create text embeddings for names
print("\n📝 Creating text embeddings for names...")
text_columns = ['name']
n_components = 23  # As per the notebook

# Create embeddings
for column in text_columns:
    print(f"   Processing {column}...")
    embeddings = sentence_model.encode(user_df_filtered[column].tolist(), show_progress_bar=True)
    user_df_filtered[column + '_embedding'] = embeddings.tolist()

# Step 6: Apply PCA to text embeddings
print("\n📊 Applying PCA to text embeddings...")
text_embeddings_pca = np.empty((len(user_df_filtered), n_components * len(text_columns)))

pca_models = {}
for i, column in enumerate(text_columns):
    embeddings = np.array(user_df_filtered[column + '_embedding'].tolist())
    pca = PCA(n_components=n_components)
    embeddings_pca = pca.fit_transform(embeddings)
    text_embeddings_pca[:, i * n_components:(i + 1) * n_components] = embeddings_pca
    pca_models[column] = pca
    print(f"   ✓ PCA for {column}: {embeddings.shape[1]} -> {n_components} components")

# Step 7: Encode company
print("\n🏢 Encoding company feature...")
label_encoder_company = LabelEncoder()
user_df_filtered['company_encoded'] = label_encoder_company.fit_transform(user_df_filtered['company'])
print(f"   ✓ Company encoding: {len(label_encoder_company.classes_)} companies")

# Step 8: Combine features
print("\n🔗 Combining features...")
numerical_features = ['code', 'company_encoded', 'age']
X_numerical = user_df_filtered[numerical_features].values
X = np.hstack((text_embeddings_pca, X_numerical))
y = user_df_filtered['gender_encoded'].values

print(f"   ✓ Feature matrix shape: {X.shape}")
print(f"   ✓ Target shape: {y.shape}")

# Step 9: Split data
print("\n✂️  Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✓ Train: {X_train.shape[0]} samples")
print(f"   ✓ Test: {X_test.shape[0]} samples")

# Step 10: Scale features
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   ✓ Features scaled")

# Step 11: Train Logistic Regression with GridSearch
print("\n🌲 Training Logistic Regression model (with hyperparameter tuning)...")
print("   This may take a few minutes...")

# Define parameter grid (simplified for faster training)
param_grid = {
    'C': [0.1, 1, 10],
    'penalty': ['l2'],
    'solver': ['lbfgs']
}

# Base model
base_lr = LogisticRegression(random_state=42, max_iter=1000)

# GridSearchCV (reduced CV folds for speed)
grid_search = GridSearchCV(
    base_lr,
    param_grid,
    cv=3,  # Reduced from 5 to 3
    scoring='accuracy',
    n_jobs=-1,
    verbose=0  # Reduced verbosity
)

grid_search.fit(X_train_scaled, y_train)

# Get best model
best_lr_model = grid_search.best_estimator_
print(f"   ✓ Best parameters: {grid_search.best_params_}")
print(f"   ✓ Best CV score: {grid_search.best_score_:.4f}")

# Step 12: Evaluate model
print("\n📈 Evaluating model...")
y_train_pred = best_lr_model.predict(X_train_scaled)
y_test_pred = best_lr_model.predict(X_test_scaled)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"   Train Accuracy: {train_accuracy:.4f}")
print(f"   Test Accuracy: {test_accuracy:.4f}")

print("\n📊 Classification Report:")
print(classification_report(y_test, y_test_pred, target_names=['female', 'male']))

# Step 13: Save models
print("\n💾 Saving model files...")

# Save PCA model (use the one from name column)
with open("pca.pkl", "wb") as f:
    joblib.dump(pca_models['name'], f)
print("   ✓ Saved: pca.pkl")

# Save scaler
with open("scaler.pkl", "wb") as f:
    joblib.dump(scaler, f)
print("   ✓ Saved: scaler.pkl")

# Save logistic regression model
with open("tuned_logistic_regression_model.pkl", "wb") as f:
    pickle.dump(best_lr_model, f)
print("   ✓ Saved: tuned_logistic_regression_model.pkl")

print("\n✅ Model training completed successfully!")
print("=" * 60)
print("\n📝 Model files created:")
print("   - scaler.pkl")
print("   - pca.pkl")
print("   - tuned_logistic_regression_model.pkl")
print("\n🚀 You can now run the Flask app:")
print("   python app.py")


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
import catboost as cb
import lightgbm as lgb
import pickle
import numpy as np

def load_data():
    # Path to the CSV file
    file_path = 'data/processed_ckd_dataset.csv'
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Assuming the last column is the target variable
    ind_col = [col for col in df.columns if col != 'class']
    dep_col = 'class'

    X = df[ind_col]
    y = df[dep_col]
    # Split the dataset into training and testing sets
    return train_test_split(X, y, test_size=0.3, random_state=0)


def train_models(X_train, X_test, y_train, y_test):
    models = {
        'KNN': KNeighborsClassifier(),
        'Random Forest Classifier': RandomForestClassifier(),
        'Decision Tree Classifier': DecisionTreeClassifier(),
        'Ada Boost Classifier': AdaBoostClassifier(),
        'XgBoost': xgb.XGBClassifier(eval_metric='mlogloss'),
        'Cat Boost': cb.CatBoostClassifier(verbose=0),  # verbose=0 to keep output clean
        'LGBM Classifier': lgb.LGBMClassifier()
    }

    param_grids = {
        'KNN': {
            'n_neighbors': [3, 5, 7, 10],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
        },
        'Random Forest Classifier': {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        },
        'Decision Tree Classifier': {
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        'Ada Boost Classifier': {
            'n_estimators': [50, 100, 150],
            'learning_rate': [0.01, 0.1, 1.0]
        },
        'XgBoost': {
            'n_estimators': [100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1]
        },
        'Cat Boost': {
            'iterations': [100, 200],
            'depth': [4, 6, 10],
            'learning_rate': [0.01, 0.1]
        },
        'LGBM Classifier': {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, 30],
            'learning_rate': [0.01, 0.1]
        }
    }


    results = {}

    for name, model in models.items():
        print(f"Training and tuning {name}...")
        search = RandomizedSearchCV(model, param_grids[name], n_iter=10, cv=5, scoring='accuracy', random_state=42, verbose=10)
        search.fit(X_train, y_train)
        best_model = search.best_estimator_
        y_pred = best_model.predict(X_test)
        
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred, average='macro'),
            'precision': precision_score(y_test, y_pred, average='macro'),
            'f1_score': f1_score(y_test, y_pred, average='macro'),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),  # Convert to list for JSON compatibility
            'best_model': best_model  # Store the best model for each algorithm
        }
    
    # Save the trained model as a pickle file
        with open(f"{name.replace(' ', '_')}.pkl", 'wb') as model_file:
            pickle.dump(best_model, model_file)

    return results

def get_model_performance():
    X_train, X_test, y_train, y_test = load_data()
    return train_models(X_train, X_test, y_train, y_test)

def load_model(model_name):
    """Load a trained model from a pickle file."""
    try:
        with open(f"{model_name.replace(' ', '_')}.pkl", 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"Model file {model_name} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

def predict_ckd(age, bloodPressure, specificGravity, albumin, sugar, bloodGlucoseRandom, bloodUrea, serumCreatinine, sodium, potassium, hgb, packedCellVolume, wbc, hypertension):
    # Load your trained model
    try:
        with open('Decision_Tree_Classifier.pkl', 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        return "Model file not found."
    except Exception as e:
        return f"An error occurred while loading the model: {e}"

    # Preprocess the inputs similarly as done during the model training
    input_features = np.array([
        float(age),
        float(bloodPressure), 
        float(specificGravity), 
        float(albumin),
        float(sugar),
        float(bloodGlucoseRandom), 
        float(bloodUrea), 
        float(serumCreatinine),
        float(sodium), 
        float(potassium),
        float(hgb),   
        float(packedCellVolume), 
        float(wbc),
        float(hypertension)
    ]).reshape(1, -1)

    # Make prediction
    try:
         result = model.predict(input_features)
         result_proba = model.predict_proba(input_features)
        
         if result[0] == 0 and result_proba[0][0] > 0.5:
            return 'CKD Detected'
         else:
            return 'CKD Not Detected'
    except Exception as e:
        return f"An error occurred during prediction: {e}"

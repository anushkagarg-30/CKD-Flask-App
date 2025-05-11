import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 26)

def preprocess_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Drop 'id' column
    df.drop('id', axis=1, inplace=True)

    # Renaming column names
    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    # Convert necessary columns to numerical type
    for col in ['packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Replace incorrect values directly by reassigning
    corrections = {
        'diabetes_mellitus': {'\tno': 'no', '\tyes': 'yes', ' yes': 'yes'},
        'coronary_artery_disease': {'\tno': 'no'},
        'class': {'ckd\t': 'ckd', 'notckd': 'not ckd'}
    }
    for col, mapping in corrections.items():
        df[col] = df[col].replace(mapping)

    # Map 'class' to numeric and convert to integer
    df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1}).astype(int)

    # Extracting categorical and numerical columns
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Imputation using random sampling and mode
    def random_value_imputation(feature):
        random_sample = df[feature].dropna().sample(df[feature].isna().sum(), random_state=42)
        random_sample.index = df[df[feature].isnull()].index
        df.loc[df[feature].isnull(), feature] = random_sample

    def impute_mode(feature):
        mode = df[feature].mode()[0]
        df[feature] = df[feature].fillna(mode)

    for col in num_cols:
        if df[col].isna().sum() > 0:
            random_value_imputation(col)

    for col in cat_cols:
        impute_mode(col)

    # Feature Encoding using LabelEncoder
    def encode_categorical_features(df, cat_cols):
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = le.fit_transform(df[col])

    encode_categorical_features(df, cat_cols)

    # Feature selection
    features_to_retain = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'blood_glucose_random',
                          'blood_urea', 'serum_creatinine', 'sodium', 'potassium', 'haemoglobin', 'packed_cell_volume',
                          'white_blood_cell_count', 'hypertension', 'class']
    df = df[features_to_retain]

    return df

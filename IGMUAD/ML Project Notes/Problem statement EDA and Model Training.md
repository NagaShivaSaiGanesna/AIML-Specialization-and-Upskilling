# End-to-End ML Project: EDA, Problem Statement & Model Training

## Introduction — The Strategy Behind This Session

Before writing a single line of modular production code, every professional data scientist does two things in a Jupyter notebook:

1. **Explores the data** (EDA) to understand what they are working with
2. **Prototypes the model** to know what works before engineering it properly

This session covers both. Once you understand what the notebook is doing, converting it to clean modular code becomes straightforward mapping — not guesswork.

---

## Section 1: The Project — Student Performance Indicator

### Problem Statement

> Predict a student's **math score** based on demographic and preparation features such as gender, ethnicity, parental education level, lunch type, and test preparation course completion.

This is a **regression problem** because the target variable (math score) is a continuous numerical value.

### Why This Dataset?

| Property | Detail |
|----------|--------|
| Rows | 1,000 students |
| Columns | 8 features |
| Feature types | Both categorical and numerical |
| Missing values | None |
| Target variable | `math_score` |

It is small enough to understand quickly, yet rich enough to demonstrate every real preprocessing technique — encoding, scaling, pipelines, and multi-model evaluation.

---

### Dataset Features

| Feature | Type | Example Values |
|---------|------|---------------|
| `gender` | Categorical | male, female |
| `race_ethnicity` | Categorical | group A, B, C, D, E |
| `parental_level_of_education` | Categorical | bachelor's degree, some college… |
| `lunch` | Categorical | standard, free/reduced |
| `test_preparation_course` | Categorical | none, completed |
| `math_score` | Numerical (target) | 0–100 |
| `reading_score` | Numerical | 0–100 |
| `writing_score` | Numerical | 0–100 |

---

## Section 2: The ML Project Lifecycle

Every project follows this sequence — understanding it lets you know exactly what comes next at every stage.

```
1. Understand Problem Statement
         ↓
2. Data Collection
         ↓
3. Data Checks (missing values, duplicates, types)
         ↓
4. Exploratory Data Analysis (EDA)
         ↓
5. Data Preprocessing (encoding, scaling)
         ↓
6. Model Training (multiple models)
         ↓
7. Model Evaluation (choose the best)
         ↓
8. Model Deployment (push to cloud)
```

---

## Section 3: EDA — Exploratory Data Analysis

EDA is always done in **Jupyter Notebook**, never in `.py` files. The goal is to generate *observations* and *insights* that justify every preprocessing decision you make later.

### Folder Structure for Notebooks

```
ml-project/
├── notebook/
│   ├── data/
│   │   └── student.csv
│   ├── EDA.ipynb           ← exploration and visualisation
│   └── ModelTraining.ipynb ← prototype training code
└── src/
    └── ...
```

### Step 1 — Basic Data Checks

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/student.csv")

# Shape
print(df.shape)           # (1000, 8)

# First look
df.head()

# Data types and non-null counts
df.info()

# Summary statistics for numerical columns
df.describe()
```

### Step 2 — Check for Missing Values

```python
df.isnull().sum()
```

**Observation:** This dataset has zero missing values. In real projects, missing values are handled with mean/median imputation for numerical features and mode imputation for categorical ones.

### Step 3 — Check for Duplicate Rows

```python
df.duplicated().sum()
```

To remove duplicates if they exist:

```python
df = df.drop_duplicates()
```

### Step 4 — Identify Feature Types Programmatically

Rather than hardcoding column names, detect types dynamically — this makes the code reusable on any dataset:

```python
# Numerical features: any column whose dtype is NOT object
numerical_features = [
    feature for feature in df.columns
    if df[feature].dtype != "O"
]

# Categorical features: any column whose dtype IS object
categorical_features = [
    feature for feature in df.columns
    if df[feature].dtype == "O"
]

print(f"Numerical features: {numerical_features}")
print(f"Categorical features: {categorical_features}")
```

**Result:**
- Numerical: `math_score`, `reading_score`, `writing_score`
- Categorical: `gender`, `race_ethnicity`, `parental_level_of_education`, `lunch`, `test_preparation_course`

### Step 5 — Feature Engineering: Creating New Target Variables

We engineer two new columns from the three existing scores, giving us the option to predict either:

```python
# Total score across all three subjects
df["total_score"] = df["math_score"] + df["reading_score"] + df["writing_score"]

# Average score (out of 100)
df["average_score"] = df["total_score"] / 3
```

This turns one prediction problem into two: predict `total_score` or predict `average_score`. For this project we will predict `math_score` directly.

### Step 6 — Key EDA Insights

Run these to generate observations for stakeholders:

```python
# Students who scored full marks in each subject
print("Full marks in maths:", df[df["math_score"] == 100]["math_score"].count())
print("Full marks in reading:", df[df["reading_score"] == 100]["reading_score"].count())
print("Full marks in writing:", df[df["writing_score"] == 100]["writing_score"].count())

# Students who barely passed (score <= 20)
print("Struggling students:", df[df["math_score"] <= 20]["math_score"].count())
```

**Key observations from visualisations:**
- Female students consistently score higher than male students on average
- Students with a standard lunch plan outperform those on free/reduced lunch
- Completing the test preparation course correlates with higher scores

---

## Section 4: Model Training Prototype

### Step 1 — Define Features and Target

```python
# Drop math_score to create X (independent features)
X = df.drop(columns=["math_score"], axis=1)

# Target variable
y = df["math_score"]
```

### Step 2 — Build a Preprocessing Pipeline

This is the most important step. We need to apply different transformations to different column types, and we need these to happen in the correct order every time — both during training *and* during prediction.

**For categorical features:** Apply One-Hot Encoding (converts categories to 0/1 columns), then Standard Scaling.

**For numerical features:** Apply Standard Scaling only.

```python
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Identify column groups dynamically
numeric_features = X.select_dtypes(exclude="object").columns
categorical_features = X.select_dtypes(include="object").columns

# Build sub-pipelines for each type
numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("encoder", OneHotEncoder()),
    ("scaler", StandardScaler(with_mean=False))  # sparse-safe
])

# Combine into a single ColumnTransformer
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])
```

**Why Pipeline over doing steps manually?**

| Manual Steps | Pipeline |
|-------------|----------|
| Easy to apply steps out of order | Steps always execute in sequence |
| Fit and transform called separately | Single `fit_transform()` call |
| Risk of data leakage | Prevents leakage automatically |
| Cannot be saved as one object | Saved and loaded as one unit |

### Step 3 — Apply Preprocessing and Split Data

```python
from sklearn.model_selection import train_test_split

# Apply the preprocessor to X
X_transformed = preprocessor.fit_transform(X)

print(X_transformed.shape)  # (1000, 19) — OHE expanded the columns

# Train/test split — 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X_transformed, y, test_size=0.2, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")   # 800
print(f"Testing samples:  {X_test.shape[0]}")    # 200
```

### Step 4 — Define Evaluation Metrics

For a regression problem, the standard metrics are:

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model(y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    mse  = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_true, y_pred)
    return mae, rmse, r2
```

**What each metric tells you:**

| Metric | Full Name | Interpretation |
|--------|-----------|----------------|
| MAE | Mean Absolute Error | Average size of errors in original units |
| RMSE | Root Mean Squared Error | Penalises large errors more heavily than MAE |
| R² | R-Squared | % of variance explained — closer to 1.0 is better |

### Step 5 — Train and Compare Multiple Models

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

models = {
    "Linear Regression":    LinearRegression(),
    "Ridge":                Ridge(),
    "Lasso":                Lasso(),
    "Decision Tree":        DecisionTreeRegressor(),
    "Random Forest":        RandomForestRegressor(),
    "AdaBoost":             AdaBoostRegressor(),
    "SVR":                  SVR(),
    "KNN":                  KNeighborsRegressor(),
    "XGBoost":              XGBRegressor(),
    "CatBoost":             CatBoostRegressor(verbose=0),
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae, rmse, r2 = evaluate_model(y_test, y_pred)
    results[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}
    print(f"{name:25s} → R²: {r2:.4f}  RMSE: {rmse:.4f}")
```

**Prototype results (approximate):**

| Model | R² Score |
|-------|---------|
| Linear Regression | ~0.88 |
| Ridge | ~0.88 |
| CatBoost | ~0.85 |
| Random Forest | ~0.85 |
| AdaBoost | ~0.83 |

**Winner: Linear Regression / Ridge** — highest R², simplest model. Always prefer simpler models when performance is equal.

---

## Section 5: Mapping Notebook Code → Modular Code

This is the key insight of this session. Every block of notebook code has a home in the modular project structure:

| Notebook Code | Where It Goes in `src/` |
|---------------|------------------------|
| `pd.read_csv(...)` | `components/data_ingestion.py` |
| `train_test_split(...)` | `components/data_ingestion.py` |
| `ColumnTransformer`, `Pipeline` | `components/data_transformation.py` |
| `model.fit(...)`, `model.predict(...)` | `components/model_trainer.py` |
| `evaluate_model(...)` | `utils.py` |
| Best model selection logic | `utils.py` |
| Saving model to disk/cloud | `utils.py` |

```
notebook/ModelTraining.ipynb
         │
         │  "Where does this code live?"
         │
         ├── read CSV ──────────────────► data_ingestion.py
         ├── train_test_split ──────────► data_ingestion.py
         ├── ColumnTransformer ─────────► data_transformation.py
         ├── model.fit / predict ───────► model_trainer.py
         ├── evaluate_model() ──────────► utils.py
         └── best model selection ──────► utils.py
```

---

## Section 6: Committing the Notebook Work

```bash
git add .
git commit -m "Add EDA notebook, model training prototype, and dataset"
git push -u origin main
```

---

## What Comes Next

In the next session we take everything from the notebook and rewrite it as clean, production-grade modular code:

- `data_ingestion.py` — reads the CSV, splits into train/test, saves artifacts
- `data_transformation.py` — builds and applies the `ColumnTransformer` pipeline
- `model_trainer.py` — trains all models, selects the best, saves the model pickle
- `utils.py` — houses `evaluate_model` and any other shared helpers

The notebook was the **thinking** phase. The modular code is the **production** phase. Both are necessary and neither replaces the other.
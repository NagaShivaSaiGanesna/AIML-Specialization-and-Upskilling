import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Set page configuration
st.set_page_config(page_title="Iris Species Classifier", layout="wide")

# 1. Load Data with Caching
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    target_names = iris.target_names
    return df, iris.target, target_names

df, target, target_names = load_data()

# 2. Train the Model
# We train the model once and cache it as a resource
@st.cache_resource
def train_model(data, target):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(data, target)
    return model

model = train_model(df, target)

# 3. Sidebar - User Input Parameters
st.sidebar.header("User Input Parameters")

def user_input_features():
    sepal_length = st.sidebar.slider('Sepal length', 
                                    float(df.iloc[:, 0].min()), 
                                    float(df.iloc[:, 0].max()), 
                                    float(df.iloc[:, 0].mean()))
    sepal_width = st.sidebar.slider('Sepal width', 
                                   float(df.iloc[:, 1].min()), 
                                   float(df.iloc[:, 1].max()), 
                                   float(df.iloc[:, 1].mean()))
    petal_length = st.sidebar.slider('Petal length', 
                                    float(df.iloc[:, 2].min()), 
                                    float(df.iloc[:, 2].max()), 
                                    float(df.iloc[:, 2].mean()))
    petal_width = st.sidebar.slider('Petal width', 
                                   float(df.iloc[:, 3].min()), 
                                   float(df.iloc[:, 3].max()), 
                                   float(df.iloc[:, 3].mean()))
    
    data = {'sepal length (cm)': sepal_length,
            'sepal width (cm)': sepal_width,
            'petal length (cm)': petal_length,
            'petal width (cm)': petal_width}
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# 4. Main Panel
st.title("Iris Species Prediction App")
st.write("""
This app predicts the **Iris flower** type based on user inputs via the sidebar!
""")

# Display the user input parameters
st.subheader('User Input parameters')
st.write(input_df)

# 5. Prediction Logic
prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)

# Display results
st.subheader('Prediction')
st.write(f"The predicted species is: **{target_names[prediction][0]}**")

st.subheader('Prediction Probability')
proba_df = pd.DataFrame(prediction_proba, columns=target_names)
st.write(proba_df)

# Instructional Info

st.info("Adjust the sliders in the sidebar to see the predicted species change in real-time.")
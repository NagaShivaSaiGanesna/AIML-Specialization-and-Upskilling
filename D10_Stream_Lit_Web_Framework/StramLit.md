# Introduction to Streamlit for Data Science

**Streamlit** is a game-changing, open-source Python framework designed specifically for data scientists and machine learning engineers. It allows you to transform Python scripts into interactive, beautiful web applications in minutes, without requiring any knowledge of **HTML**, **CSS**, or **JavaScript**.

With the rise of Generative AI and Large Language Models (LLMs), Streamlit has become the industry standard for rapidly prototyping AI-powered chatbots and interactive data dashboards.

---

## 1. Getting Started: Installation and Execution

To use Streamlit, you must first install it within your Python environment. It is best practice to manage this via a `requirements.txt` file.

### Installation

1. Add `streamlit` to your `requirements.txt`.
2. Run the installation command:
```bash
pip install -r requirements.txt

```



### Running the App

Unlike standard Python scripts, you do not use `python app.py`. Instead, you use the Streamlit CLI:

```bash
streamlit run app.py

```

By default, the app will run locally on **port 8501** (e.g., `http://localhost:8501`).

---

## 2. Core Components: Displaying Content

Streamlit provides high-level functions called **components** that handle the frontend rendering automatically.

### Basic Text Components

| Function | HTML Equivalent | Purpose |
| --- | --- | --- |
| `st.title()` | `<h1>` | The main headline of your app. |
| `st.header()` | `<h2>` | Section headings. |
| `st.write()` | `<p>` / Mixed | The "Swiss Army Knife"—displays text, dataframes, or charts. |

### Working with Data

Streamlit integrates natively with **Pandas** and **NumPy**. You can display interactive tables with a single line:

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"Col1": [1, 2], "Col2": [3, 4]})
st.write("Here is my data:", df)

```

---

## 3. Interactive Widgets: Capturing User Input

Widgets are what make a Streamlit app interactive. When a user interacts with a widget, Streamlit reruns the script from top to bottom, updating the view with the new data.

### Common Widgets

* **Text Input:** Capture strings (e.g., names, queries).
```python
name = st.text_input("Enter your name")

```


* **Sliders:** Select a value from a range.
```python
age = st.slider("Select your age", 0, 100, 25)

```


* **Selectbox:** Create a dropdown menu.
```python
option = st.selectbox("Choose a language", ["Python", "Java", "C++"])

```


* **File Uploader:** Allow users to upload datasets (CSV, Excel, etc.).
```python
file = st.file_uploader("Upload a CSV", type="csv")

```



---

## 4. Visualizing Data: Charts and Graphs

Streamlit simplifies plotting by providing built-in chart types that are interactive by default (zoom, pan, save).

### Line Charts

To create a line chart, you simply pass a Pandas DataFrame or a NumPy array:

```python
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.line_chart(chart_data)

```

---

## 5. Development Workflow: The "Hot Reload"

One of Streamlit's most powerful features is **Fast Development**.

1. You write your Python code and save the file.
2. Streamlit detects the change and displays an **"Always rerun"** option in the browser.
3. Your app updates instantly without you needing to manually restart the server.

---

## Summary Checklist

* [ ] **Streamlit** is Python-only; no frontend experience is required.
* [ ] Use **`st.write()`** for general output and **`st.title()`** for headings.
* [ ] **Widgets** (sliders, inputs) store user values directly into Python variables.
* [ ] The app reruns automatically on every interaction, ensuring the UI is always in sync with your logic.



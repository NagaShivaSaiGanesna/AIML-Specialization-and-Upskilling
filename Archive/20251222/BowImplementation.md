Here is a structured summary of the practical session on implementing **Bag of Words (BoW)** using Python and the `sklearn` library.

### **High-Level Overview**

The process involves reading the data, extensive pre-processing (cleaning), and finally converting the text into vectors using `CountVectorizer`.

---

### **1. Data Loading & Inspection**

* **Dataset:** Contains SMS messages labeled as `ham` (normal) or `spam`.
* **Loading:** Used `pandas.read_csv` with a custom separator (`sep='\t'`) because the file is tab-separated.
* **Columns Assigned:** `label` (Target) and `message` (Input Text).

### **2. Data Pre-processing (Cleaning)**

Before creating vectors, the raw text was cleaned using a loop over the entire dataset (Corpus).

* **Step A: Regular Expressions (Regex):**
* Used `re.sub('[^a-zA-Z]', ' ', message)` to remove all special characters (punctuation, numbers, etc.), keeping only alphabets (A-Z, a-z).


* **Step B: Lowercasing:**
* Converted all text to lowercase to ensure consistency.


* **Step C: Stopword Removal & Stemming:**
* Iterated through words to remove English **Stopwords** (e.g., *the, is, in*).
* Applied **Porter Stemmer** to the remaining words to reduce them to their root form (e.g., *going*  *go*).
* *Assignment:* The speaker suggested trying **Lemmatization** here instead of Stemming for potentially better accuracy.



### **3. Implementing Bag of Words**

The core conversion was done using Scikit-Learn's `CountVectorizer`.

```python
from sklearn.feature_extraction.text import CountVectorizer

# Initialize
cv = CountVectorizer(max_features=2500, binary=True)

# Transform
X = cv.fit_transform(corpus).toarray()

```

#### **Key Parameters Explained:**

* **`max_features`:**
* Limits the vocabulary to the top  most frequent words (e.g., 2500).
* **Why?** To avoid creating massive vectors filled with rare words that don't add value.


* **`binary`:**
* If `True`: Creates a **Binary Bag of Words** (Values are only 0 or 1).
* If `False` (Default): Creates a **Frequency Bag of Words** (Values represent word counts, e.g., 2, 3).



### **4. Result**

* **Output Shape:** `(5572, 2500)`
* **5572:** Number of SMS messages (rows).
* **2500:** The fixed size of the vector (columns/features) determined by `max_features`.


* **Outcome:** The text data is now successfully converted into a numerical array (`X`) ready for machine learning model training.

### **Next Steps**

The speaker mentioned that the next video will explain **N-grams (`ngram_range`)**, another parameter in `CountVectorizer` that helps capture context by grouping words together.
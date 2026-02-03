
### **Bag of Words (BoW)**

**Introduction**
Bag of Words is the second technique discussed for converting text into numerical vectors, following One Hot Encoding. It is widely used for text classification tasks such as Sentiment Analysis (e.g., classifying positive vs. negative reviews) or Spam Detection (Spam vs. Ham). Unlike One Hot Encoding, which generates vectors for individual words, BoW creates a single fixed-length vector representation for an entire sentence or document.

### **Implementation Process**

The process begins with **Text Pre-processing**. Before generating vectors, the raw text must be cleaned to ensure consistency and remove noise. Two critical steps in this phase:

* **Lowercasing:** All text is converted to lowercase. This is essential to handle case sensitivity; for example, ensuring "Boy" (uppercase) and "boy" (lowercase) are treated as the same word rather than distinct features.
* **Stopword Removal:** Common grammatical words (like *he, she, is, a, and*) are removed. These words appear frequently but contribute very little semantic meaning to classification tasks.

**Vocabulary Creation**
Once the sentences are cleaned (e.g., "He is a good boy" becomes "good boy"), the algorithm constructs a vocabulary. This involves identifying every unique word across the entire dataset and calculating its frequency.

* **Frequency Sorting:** Words are typically sorted in descending order of frequency (most frequent first).
* **Feature Selection:** In large datasets, you can limit the vocabulary size (e.g., top 1,000 words) to prioritize the most impactful features and ignore rare words.

### **Vector Generation Logic**

The sorted vocabulary becomes the **features** (columns) of the vector. The algorithm then scans each sentence to check for the presence of these vocabulary words.

*Example Scenario:*
Using the vocabulary `[good, boy, girl]`, the sentences are converted as follows:

* **Sentence 1:** "He is a good boy"  *Cleaned:* "good boy"
* **Vector:** `[1, 1, 0]` (Contains 'good' and 'boy', but no 'girl').


* **Sentence 2:** "She is a good girl"  *Cleaned:* "good girl"
* **Vector:** `[1, 0, 1]` (Contains 'good' and 'girl', but no 'boy').


* **Sentence 3:** "Boy and girl are good"  *Cleaned:* "boy girl good"
* **Vector:** `[1, 1, 1]` (Contains all three words).



### **Types of Bag of Words**

The transcript distinguishes between two specific variations of this technique, which determine how the values inside the vector are calculated:

* **Binary Bag of Words:**
This approach only checks for the **existence** of a word. The value is strictly **1** (present) or **0** (absent). Even if a word appears multiple times in a sentence, the value remains 1.
* **Frequency-Based (Normal) Bag of Words:**
This approach counts the **occurrences** of the word. If a word appears twice in a sentence (e.g., "Good good girl"), the vector value for "good" will be **2**. This allows the model to weigh repeated words more heavily.
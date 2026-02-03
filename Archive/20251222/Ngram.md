
### **Introduction to N-grams**

The video introduces **N-grams** as a vital technique to improve text representation models like Bag of Words. The primary goal of N-grams is to capture the **context** and ordering of words, which is often lost when looking at words individually. Without N-grams, models can struggle to distinguish between sentences that use similar words but have completely opposite meanings.

### **The Problem with Unigrams (Single Words)**

The speaker uses a specific example to demonstrate why looking at one word at a time (Unigrams) fails:

* **Sentence 1:** "The food is good"
* **Sentence 2:** "The food is not good"
* **The Issue:** These sentences share almost the exact same vocabulary. In a standard Bag of Words model, their vectors look nearly identical (e.g., `1,0,1` vs `1,1,1`).
* **Result:** The machine learning model sees them as mathematically similar, even though "good" and "not good" are opposites.

### **How N-grams Solve This**

N-grams solve this by creating features from **sequences of adjacent words** rather than just single words. By grouping words together, the model can learn that "not good" is a single meaningful unit that is distinct from just "good." This creates vectors that are much more distinct from one another, allowing the model to understand sentiment and negation effectively.

### **Types of N-grams & Implementation**

In libraries like Scikit-Learn, this is controlled using the `ngram_range` parameter. The speaker explains three common configurations:

* **Unigram `(1, 1)`:** Uses only single words (e.g., "food", "good"). No context is captured.
* **Bigram `(1, 2)`:** Uses both single words and pairs of consecutive words.
* *Features:* "food", "good", "food good", "not good".


* **Trigram `(1, 3)`:** Uses single words, pairs, and triplets of words.
* *Features:* "food", "not", "food not", "not good", "food not good".

* **Bi Tri Gram  `(2, 3)`:**  : "food not", "not good", "food not good".


By using Bigrams or Trigrams, the feature space grows, but the vectors become far more descriptive, enabling the model to clearly distinguish "food good" from "food not good."

### **What are Word Embeddings?**

Word Embedding is a fundamental concept in NLP used to represent words for text analysis. It involves converting words into **real-valued vectors** in such a way that the vectors encode the meaning of the word.

* **Core Principle:** Words that are similar in meaning should be positioned closer to each other in the vector space, while dissimilar words should be far apart.

**Example from Transcript:**

* **Similar Words:** If you convert "Happy" and "Excited" into vectors and plot them on a 2D graph (using dimensionality reduction like PCA), they will appear very close to each other.
* **Opposite Words:** If you add the word "Angry" to the same graph, it will appear far away from "Happy" and "Excited," mathematically representing the opposite meaning.

---

### **Categories of Word Embedding Techniques**

The speaker divides all word embedding techniques into two major categories:

#### **1. Count or Frequency-Based Methods**

These are the techniques covered in previous videos. While they successfully convert text to vectors, they suffer from limitations like sparsity and lack of semantic meaning.

* **One Hot Encoding**
* **Bag of Words (BoW)**
* **TF-IDF (Term Frequency-Inverse Document Frequency)**

#### **2. Deep Learning Trained Models (Prediction-Based)**

These are more advanced methods that solve the disadvantages of frequency-based models (like high dimensionality and sparsity) and provide much better accuracy.

* **Word2Vec:** The most prominent technique in this category. It creates efficient vector representations where semantic relationships are preserved.

---

### **Types of Word2Vec Models**

The speaker introduces **Word2Vec** as the focus of upcoming videos and categorizes it into two distinct architectures based on how the underlying neural network is trained:

1. **CBOW (Continuous Bag of Words):** Predicts a target word based on context words.
2. **Skip-Gram:** Predicts context words based on a target word.


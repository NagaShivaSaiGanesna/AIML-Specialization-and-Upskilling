Here is the summary of the transcript regarding the **Skip-Gram** architecture for Word2Vec.

### **1. Core Concept: Skip-Gram vs. CBOW**

The fundamental difference between Skip-Gram and the previously discussed CBOW (Continuous Bag of Words) is the **direction of prediction**.

* **CBOW:** Takes multiple *Context Words* (Input)  Predicts the single *Target Word* (Output).
* *"I see 'The', 'quick', 'fox'. The missing middle word is likely..."*


* **Skip-Gram:** Takes a single *Target Word* (Input)  Predicts multiple *Context Words* (Output).
* *"I see the word 'fox'. The words likely to be near it are..."*



### **2. Architecture Changes**

Using the same example sentence: *"iNeuron company is related to data science"*, the input and output data structure is flipped compared to CBOW.

* **Input Layer:** Receives the **Center Word** (e.g., "is").
* It accepts just **1 word** at a time (represented as a One-Hot encoded vector).


* **Hidden Layer:** Compresses the input into the embedding dimension (e.g., 300 neurons).
* *Correction Note:* The speaker again conflates "Window Size" with "Hidden Layer Size." As noted before, the Hidden Layer size is a design choice (like 100 or 300) and is not strictly tied to the window size (5).


* **Output Layer:** Predicts **multiple words** (the surrounding context).
* If the window size is 5, the model tries to predict the 2 words before and 2 words after the input word.



### **3. Training Process**

* **Neural Network:** It uses a fully connected ANN.
* **Forward Propagation:** The input (center word) passes through the hidden layer to the output layer.
* **Loss Calculation:** The model uses **Softmax** to generate probabilities. It compares these predictions with the actual context words found in the text.
* **Backpropagation:** The weights are updated to minimize the loss, refining the word vectors in the hidden layer.

### **4. When to Use Which?**

The speaker provides a research-backed rule of thumb for choosing between the two architectures:

| Model | Best For |
| --- | --- |
| **CBOW** | **Small Datasets.** It is faster to train and has better accuracy on frequent words. |
| **Skip-Gram** | **Huge Datasets.** It works better with infrequent words and generally produces higher quality vectors for large corpora. |

### **5. Improving the Model**

To get better accuracy from Word2Vec (either architecture), the speaker suggests:

1. **Increase Training Data:** More text leads to better semantic understanding.
2. **Increase Vector Dimension:** (The speaker calls this "Window Size" but refers to dimension). Using a larger hidden layer (e.g., 300 instead of 50) allows the model to capture more subtle relationships, though it requires more data to train effectively.

### **6. Google's Pre-Trained Model**

The speaker mentions Google's famous Word2Vec model as a benchmark:

* **Training Data:** 3 Billion words (from Google News).
* **Vector Dimension:** 300 dimensions.
* **Capability:** Can represent complex relationships (e.g., "Cricket") with high precision without needing to train from scratch.

### **Next Steps**

The next video will move to **practical implementation**, where they will use the `Gensim` library to load pre-trained models and train new ones from scratch.
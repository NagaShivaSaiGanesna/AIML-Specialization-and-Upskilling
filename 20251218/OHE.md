# OHE
Following text pre-processing steps like stemming, lemmatization, and stop word removal, the next critical step in NLP is converting text into vectors.
# Method - 
One Hot Encoding:
Vocabulary Creation: The first step is to identify all unique words (vocabulary) across the entire corpus (all documents combined).
Vector Representation: Each word is represented by a binary vector with a dimension equal to the vocabulary size . If a specific word is present at a certain index in the vocabulary, it is marked as 1, and all other positions are marked as 0.
Example:
Documents:
    D1: "the food is good"
    D2: "the food is bad"
    D3: "pizza is amazing"
Unique Vocabulary (Size 7): ['the', 'food', 'is', 'good', 'bad', 'pizza', 'amazing'].
Encoding D1 ("the food is good"):
    "the": [1, 0, 0, 0, 0, 0, 0]
    "food": [0, 1, 0, 0, 0, 0, 0]
    "is": [0, 0, 1, 0, 0, 0, 0]
    "good": [0, 0, 0, 1, 0, 0, 0]
Result: The document D1 is represented as a matrix with the shape 4x7 (4 words x 7 vocabulary size).

Conclusion: The video concludes by noting that while simple, $\One \Hot \Encoding \is \rarely \used \in \advanced \NLP \due \to \disadvantages$ 

# Advantages

Ease of Implementation:
It is very simple to implement in Python using standard libraries.
Scikit-learn: OneHotEncoder class.
Pandas: pd.get_dummies() function.
Intuitive: The concept is straightforward—representing words as binary vectors based on a vocabulary.

# Disadvantages (The Major Limitations)
1. Sparsity (Sparse Matrix)
 Problem: OHE creates vectors filled mostly with zeros and only a single one.

 Consequence: When you have a large vocabulary (e.g., 50,000 words), each vector becomes massive (length 50k) but contains almost no information (mostly zeros).

 Impact on ML: This leads to Overfitting, where the model learns noise in the training data and fails to generalize to new data.
 
2. Variable Input Size (No Fixed Size)
Problem: Machine Learning algorithms require inputs of a fixed size (e.g., every sentence must generate a matrix of the same dimensions).
Example:
Sentence 1 (4 words): Generates a $4 \times 7$ matrix.
Sentence 2 (3 words): Generates a $3 \times 7$ matrix.

Consequence: You cannot feed these directly into standard ML models because the dimensions mismatch.

3. No Semantic Meaning CapturedProblem: OHE treats every word as equally distinct from every other word. It cannot capture relationships or similarities.The Vector Space 

Example:If you plot Food, Pizza, and Burger in 3D space:
Food: $(1, 0, 0)
$Pizza: $(0, 1, 0)
$Burger: $(0, 0, 1)

$The distance between Food and Pizza is identical to the distance between Food and Burger. 
The model does not learn that Pizza and Burger are similar types of Food.

4. Out of Vocabulary (OOV) Issue
Problem: The model can only handle words present in the training vocabulary.
Scenario: If you train on a dataset, and the test data contains a new word (e.g., "Burger" was not in training), the model has no way to represent it.
Consequence: The system fails or ignores new words entirely during testing/deployment.
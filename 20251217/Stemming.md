# Stemming
 a text pre-processing technique used to reduce words to their root form (word stem) by removing affixes, suffixes, or prefixes. The primary goal is to simplify input features for machine learning models (like sentiment analysis or spam classification) by treating variations of a word (e.g., "eating," "eats," "eaten") as a single entity.

# 1. Porter Stemmer
 Description: The most basic stemming technique.
 Function: Cuts off suffixes to find the root.
 Outcome: Works for simple cases (eating ---> eat), but often produces non-words or changes meaning.Examples of Failure:history ---> histori (Meaning lost)congratulations ---> congratul (Non-word)

# 2. RegexpStemmer (Regular Expression Stemmer)
 Description: A class that uses custom Regular Expressions (Regex) to identify and remove morphological affixes.
 Function: You define a pattern (e.g., ing$), and if the word matches, that part is removed.
 Usage: Highly customizable but requires precise regex patterns to avoid over-clipping words.

# 3. Snowball Stemmer
 Description: An improved, more aggressive, and accurate version of the Porter Stemmer.
 Features: Supports multiple languages (English, French, German, etc.).
 Comparison: It handles complex suffixes better than Porter.
 Porter: fairly ---> fairli
 Snowball: fairly ---> fair (Correct root)
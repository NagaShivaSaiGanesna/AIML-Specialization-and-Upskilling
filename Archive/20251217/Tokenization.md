# Methods

Sentence Tokenization (sent_tokenize)
Function: Converts a paragraph into a list of individual sentences.
Logic: It identifies sentence boundaries based on punctuation marks like periods (.) and exclamation points (!).

Word Tokenization (word_tokenize)
Function: Splits paragraphs into individual words.
Logic: It treats punctuation (commas, full stops) as separate individual tokens. It is the most commonly used method.

WordPunct Tokenization (WordPunctTokenizer)
Function: Splits text based strictly on punctuation.
Key Difference: Unlike standard word tokenization, this will split apostrophes (e.g., "Krishna's" becomes ['Krishna', "'", 's']).

Treebank Word Tokenization (TreebankWordTokenizer)
Function: A standard tokenizer used in the Penn Treebank project.
Key Difference: It handles full stops differently than word_tokenize. It often keeps the full stop attached to the previous word (unless it is the very last word of the text), whereas standard tokenization separates it.
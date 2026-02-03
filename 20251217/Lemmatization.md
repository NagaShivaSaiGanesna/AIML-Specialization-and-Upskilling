# Lemmatization 
 is a superior alternative to Stemming. 
 While Stemming chops off word endings to find a "stem" (often resulting in non-words like histori), Lemmatization uses a $dictionary-based$ approach (WordNet corpus) to reduce words to their Lemma (a valid, meaningful root word).

 # WordNetLemmatizerLibrary: 
  Uses nltk.stem.WordNetLemmatizer.
  Mechanism: It doesn't just cut suffixes; it looks up the word in the WordNet database to return the correct grammatical root.
  Stemming: History ---> Histori (Meaningless)
  Lemmatization: History ---> History (Meaningful)

Feature,        Stemming (Porter/Snowball),                    Lemmatization (WordNet)
Output,         Word Stem (often a non-word).,                 Lemma (a valid dictionary word).
Method,         Rule-based (Algorithmic cutting).,             Dictionary-based (Lookup).
Speed,          Faster (Simple string operations).,            Slower (Requires corpus lookup).
Use Cases,      Spam Classification,                           Chatbots, Q&A Systems, Text Summarization  
                Sentiment Analysis (where speed matters).      (where grammatical accuracy matters)
                
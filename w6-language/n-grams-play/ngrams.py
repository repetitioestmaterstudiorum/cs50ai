from collections import Counter

import nltk
# nltk.download('punkt') # needs one uncommented run
import os
import sys


def main():
    """Calculate top term frequencies for a corpus of documents."""

    if len(sys.argv) < 3:
        sys.exit("Usage: python ngrams.py n corpus no_stopwords?(boolean)")
    print("Loading data...")

    no_stopwords = False
    if len(sys.argv) > 3 and sys.argv[3] == 'True':
        no_stopwords = True
    

    n = int(sys.argv[1])
    corpus = load_dir_data(sys.argv[2], no_stopwords)

    # Compute n-grams
    ngrams = Counter(nltk.ngrams(corpus, n))

    # Print most common n-grams
    for ngram, freq in ngrams.most_common(10):
        print(f"{freq}: {ngram}")


def load_dir_data(directory, no_stopwords=False):
    contents = []
    stopwords = nltk.corpus.stopwords.words('english') if no_stopwords else []
    # Read all files and extract words
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            contents.extend([
                word.lower() for word in
                nltk.word_tokenize(f.read())
                if any(c.isalpha() for c in word)
                and word.lower() not in stopwords
            ])
    return contents


if __name__ == "__main__":
    main()

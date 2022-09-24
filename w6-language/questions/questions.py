import nltk
nltk.download('stopwords') # execute at least once
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    DIAG = False

    cwd = os.getcwd()
    dir_absolute_path = os.path.join(cwd, directory)
    DIAG and print(f"Reading txt files from directory {dir_absolute_path} ...")
    dir_contents = dict()

    for dir_element in os.scandir(dir_absolute_path):
        if dir_element.is_file and dir_element.name.endswith('.txt'):
            with open(dir_element.path) as file:
                dir_contents[dir_element.name] = file.read()
        else:
            print(f"! Skipped element {dir_element.name}")

    return dir_contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    words = list()

    for word in nltk.word_tokenize(document):
        w = word.lower()

        if w in punctuation or w in stopwords:
            continue
        else:
            words.append(w)    

    """
    Remarks: it might make sense to filter out urls from the text as well. However, since the exercise data texts *should* include just one url per document, it might not be very important.
    However, there seem to be lots of occurences of "==" and "===" in the text because of the way the Wikipedia articles were prepared, as well as "``" and "''". These could be filtered out as well (e.g. by extending the list of punctuation symbols).
    """

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_documents = len(documents)
    idfs = dict()

    """
    More readable but less efficient solution:
        unique_words = set(word for words in documents.values() for word in words)
        for u_word in unique_words:
            word_occurrence_count = sum(1 for d_words in documents.values() if u_word in d_words)
            idf = math.log(total_documents / word_occurrence_count)
            idfs[u_word] = idf
    """

    for doc_words in documents.values():
        for doc_word in doc_words:
            if doc_word not in idfs:
                word_occurrence_count = sum(1 for d_words in documents.values() if doc_word in d_words)
                idf = math.log(total_documents / word_occurrence_count)
                idfs[doc_word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    DIAG = False
    DIAG and print(f"query: {query}, len(files): {len(files)}, len(idfs): {len(idfs)}, n: {n}")

    files_ranking = dict()

    for word in query:
        idf = idfs[word]
        for doc_name, doc_words in files.items():
            tf = sum(1 for d_word in doc_words if d_word == word) or 0
            tf_idf = tf * idf

            DIAG and print(f"word: {word}, tf: {tf}, tf_idf: {tf_idf}")
            
            files_ranking[doc_name] = files_ranking.get(doc_name, 0) + tf_idf

    DIAG and print('files_ranking', files_ranking)

    return [filename for filename in dict(sorted(files_ranking.items(), key=lambda x: x[1], reverse=True))][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    DIAG = False
    DIAG and print(f"query: {query}, len(sentences): {len(sentences)}, len(idfs): {len(idfs)}, n: {n}")

    sentence_ranking = dict()

    for word in query:
        idf = idfs.get(word, None)
        DIAG and print(f"idf for {word}: {idf}")
        if not idf: 
            continue

        for sentence, sentence_words in sentences.items():
            if word in sentence_words:
                sentence_ranking[sentence] = {
                    'matching_words_measure': sentence_ranking.get(sentence, {}).get('matching_words_measure', 0) + idf, # i.e. idf sum of all of the query words that are in that sentence
                    'query_term_density': sentence_ranking.get(sentence, {}).get('query_term_density', 0) + (sum(1 for sentence_word in sentence_words if word == sentence_word) / len(sentence_words)) # i.e. how many times the query words appear in that sentence
                }

    best_n_sentences = sorted(sentence_ranking, key=lambda k: (sentence_ranking[k]['matching_words_measure'], sentence_ranking[k]['query_term_density']), reverse=True)[:n]

    if DIAG:
        print(f"best_n_sentences: {best_n_sentences}")
        print(f"sentence_ranking for best {n} sentence(s):")
        for sentence in best_n_sentences:
            print(sentence_ranking[sentence])

    return best_n_sentences


if __name__ == "__main__":
    main()

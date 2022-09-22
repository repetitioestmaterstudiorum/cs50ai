import nltk
import sys

TERMINALS = """
Adj -> "red" | "enigmatical" | "country" | "dreadful" | "little" | "moist"
Adv ->  "here" | "never" | "down"
Conj -> "and" | "until"
Det -> "a" | "the" | "my" | "an" | "his"
N -> "holmes" | "pipe" | "we" | "thursday" | "day" | "armchair" | "he" | "companion" | "smile" | "himself" | "she" | "word" | "door" | "i" | "walk" | "home" | "mess" | "paint" | "palm" | "hand"
P -> "before" | "in" | "to" | "at" | "on" | "of"
V -> "sat" | "lit" | "arrived" | "chuckled" | "smiled" | "said" | "were" | "had" | "came"
"""

NONTERMINALS = """
S -> NP VP
S -> NP VP NP
S -> NP VP PP
S -> NP VP PP Conj VP
S -> NP VP Conj VP NP
S -> NP VP NP PP Conj VP PP
S -> NP VP NP Conj NP VP PP Adv
S -> VP NP PP PP
NP -> N | Det N | Det N P N | Det V N | Det Adj N | Det Adj Adj Adj N
VP -> V | N V | Adv V | V Adv | V N
PP -> P N | P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # example output: ['holmes', 'lit', 'a', 'pipe']
    return list(word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word))


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    return [subtree for subtree in tree.subtrees() if subtree.label() == 'NP']


if __name__ == "__main__":
    main()

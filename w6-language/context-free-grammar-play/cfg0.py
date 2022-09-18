import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP

    NP -> D N | N
    VP -> V | V NP

    D -> "the" | "a"
    N -> "she" | "city" | "car"
    V -> "saw" | "walked"
""")

parser = nltk.ChartParser(grammar)

words = input("Sentence: ").split()
try:
    for tree in parser.parse(words):
        tree.pretty_print()
except ValueError:
    print("No parse tree possible.")

# e.g. she saw a car
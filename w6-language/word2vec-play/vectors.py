from scipy.spatial.distance import cosine

import numpy as np

with open("words.txt") as f:
    words = dict()
    for i in range(50000):
        row = next(f).split()
        word = row[0]
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector


def distance(w1, w2):
    return cosine(w1, w2)


def closest_words(embedding):
    distances = {
        w: distance(embedding, words[w])
        for w in words
    }
    return sorted(distances, key=lambda w: distances[w])[:10]


def closest_word(embedding):
    return closest_words(embedding)[0]

print("distance(words['book'], words['audiobook']):", distance(words['book'], words['audiobook'])) # 0.2902111051633657
print("distance(words['table'], words['giraffe']):", distance(words['table'], words['giraffe'])) # 0.7642318135027607
print("closest_words(words['ape'])[:10]:", closest_words(words['ape'])[:10]) # ['ape', 'monkey', 'chimp', 'apes', 'creature', 'beast', 'gorilla', 'chimpanzee', 'lizard', 'pig']
print("closest_word(words['king'] - words['man'] + words['woman']):", closest_word(words['king'] - words['man'] + words['woman'])) # queen
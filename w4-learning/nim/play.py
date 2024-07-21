import sys
from nim import train, play

DEFAULT_ROUNDS = 500

rounds = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROUNDS

ai = train(rounds)

play(ai)

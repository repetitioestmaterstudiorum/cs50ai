from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # game propositions
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # puzzle proposition 
    Or(
        # telling the truth
        And(AKnight, AKnave),
        # lying
        AKnave
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # game propositions
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # puzzle propositions
    Or(
        # A is telling the truth
        And(AKnight, AKnave, BKnave),
        # A is lying
        And(AKnave, BKnight)
    ),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # game propositions
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # puzzle propositions
    Or(
        # A is telling the truth
        And(AKnight, BKnight), 
        # A is lying
        And(AKnave, Not(BKnave)),
    ),
    Or(
        # B is telling the truth
        And(BKnight, AKnave),
        # B is lying
        And(BKnave, Not(BKnight))
    ), 
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # game propositions
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # puzzle propositions
    Or(
        # A is telling the truth
        AKnight,
        # A is lying
        Not(AKnave),
    ),
    Or(
        # B is telling the truth
        And(AKnave, CKnave, BKnight),
        # B is lying
        And(Not(AKnave), Not(CKnave), BKnave)
    ),
    Or(
        # C is telling the truth
        And(AKnight, CKnight),
        # C is lying
        And(AKnave, CKnave)
    ),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

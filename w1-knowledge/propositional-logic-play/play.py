from logic import *
import termcolor

# ---

dark = Symbol("It is dark outside")
night = Symbol("It is the night")
evening = Symbol("It is the evening")
day = Symbol("It is the day")
summer = Symbol("It is summer")
winter = Symbol("It is winter")

symbols = [dark, night, evening, summer, winter]

knowledge_base = And(
    dark,
    Implication(night, dark),
    Implication(And(evening, winter), dark),
    Or(summer, winter),
    Not(And(summer, winter)),
)

def what_is_true(knowledge_base):
    print('What we know for sure:')
    for symbol in symbols:
        if model_check(knowledge_base, symbol):
            print(f"- {symbol}")

def check_knowledge(knowledge_base):
    print('Knowledge base complete state:')
    for symbol in symbols:
        if model_check(knowledge_base, symbol):
            termcolor.cprint(f"- {symbol}: YES", "green")
        elif not model_check(knowledge_base, Not(symbol)):
            print(f"- {symbol}: MAYBE")

if __name__ == "__main__":
    print()
    what_is_true(knowledge_base)
    print()
    check_knowledge(knowledge_base)
    print()

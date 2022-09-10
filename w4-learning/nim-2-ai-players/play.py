from nim import train, play

training_and_playing_rounds = 50

training_rounds = 5000
playing_rounds = 500

ai_alpha = 0.5 # alpha has little influence
ai_epsilon = 0.1 # big influence

ai2_alpha = 0.5
ai2_epsilon = 0.3

"""
It seems like whoever starts the game 2nd has a ~87% chance of winning, with "default settings" (alpha 0.5, epsilon 0.1)!
Therefore, here, each AI takes turn in starting in each "training and playing round".
"""

print(f"Training and playing rounds: {training_and_playing_rounds}")
print(f"Training rounds per round: {training_rounds}")
print(f"Playing rounds per round: {playing_rounds}\n")

ai_won_rounds = 0
ai2_won_rounds = 0

for i in range(training_and_playing_rounds):
    print(f"Overall round: {i + 1}/{training_and_playing_rounds}")

    ai = train(training_rounds, ai_alpha, ai_epsilon, 'ai')
    ai2 = train(training_rounds, ai2_alpha, ai2_epsilon, 'ai2')

    ai_won = 0
    ai2_won = 0

    for round in range(playing_rounds):
        winner = play(ai, ai2, i % 2)
        if winner == 'ai':
            ai_won += 1
        elif winner == 'ai2':
            ai2_won += 1

    round_winner = 'neihter!'
    if ai_won > ai2_won:
        ai_won_rounds += 1
        round_winner = 'AI'
    elif ai2_won > ai_won:
        ai2_won_rounds += 1
        round_winner = 'AI 2'

    print(f"Training and playing round winner: {round_winner}\n")

overall_winner = 'neither!'
if ai_won_rounds > ai2_won_rounds:
    overall_winner = 'AI'
elif ai2_won_rounds > ai_won_rounds:
    overall_winner = 'AI 2'

print('WINNER: <<', overall_winner, '>>')
print('AI   won:', f"{100 / training_and_playing_rounds * ai_won_rounds:.0f}% with settings: {ai_alpha} alpha, {ai_epsilon} epsilon ({ai_won_rounds}/{training_and_playing_rounds})")
print('AI 2 won:', f"{100 / training_and_playing_rounds * ai2_won_rounds:.0f}% with settings: {ai2_alpha} alpha, {ai2_epsilon} epsilon ({ai2_won_rounds}/{training_and_playing_rounds})")

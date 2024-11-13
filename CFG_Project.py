import random
from typing import Any
import requests
import pandas as pd

my_score = 0
challenger_score = 0

play_game = True
while play_game:

    def randomise_pokemon():
        pick_pokemon = random.randint(1, 151)
        url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pick_pokemon)
        response = requests.get(url)
        pokemon = response.json()

        global my_score
        global challenger_score

        return {
            'name': pokemon['name'],
            'h': pokemon['height'],
            'i': pokemon['id'],
            'be': pokemon['base_experience'],
            'w': pokemon['weight'],
        }

    my_pokemon = randomise_pokemon()
    print('You were given {}'.format(my_pokemon['name']))
    stat_choice = input('Which stat do you want to play? Enter h for height, i for id, be for base experience or w for weight. Pick now!')

    challenger_pokemon = randomise_pokemon()
    print('Your opponent chose {}'.format(challenger_pokemon['name']))

    my_stat = my_pokemon[stat_choice]
    challenger_stat = challenger_pokemon[stat_choice]

    if my_stat > challenger_stat:
        my_score = my_score +1
        print('Your value is ' + str(my_stat))
        print('Your opponents value is ' + str(challenger_stat))
        print('You Win!')
        print("Your points: " + str(my_score))
        print("Opponent points: " + str(challenger_score))
    elif my_stat < challenger_stat:
        challenger_score = challenger_score +1
        print('Your value is ' + str(my_stat))
        print('Your opponents value is ' + str(challenger_stat))
        print('You Lose!')
        print("Your points: " + str(my_score))
        print("Opponent points: " + str(challenger_score))
    else:
        print('Draw!')

    play_again = input('Do you want to play again? (Y/N): ')

    if play_again.upper() != 'Y':
        play_game = False

data = {
    'Your Stat': my_stat,
    'Your Score' : my_score,
    'Opponent Stat': challenger_stat,
    'Opponent Score': challenger_score,
}
df = pd.DataFrame(data)
df.to_csv('score.csv')
from model.TrainerClass import Trainer
from model.EnemyTrainerClass import EnemyTrainer

def new_game(game):
    #TODO need to display pokemon and add pokemon clicked on: game.trainer.add_pokemon(pokemon) , take pokelist buttons for pokemon
    # Player and AI object are created here. It's for deck-building/random encounter feature
    game.trainer = Trainer("Player")
    game.enemy = EnemyTrainer("Rival")
    
    #adds default pokemon in pokemon list
    #extract json
    # for pkmn in pokedb:
    #   if pkmn["ingame"]:
    #     game.enemy.pokemon.append(pkmn)

    #starter choose
    game.button_pokemon1.draw(game.screen)
    game.button_pokemon2.draw(game.screen)
    game.button_pokemon3.draw(game.screen)

    game.image_pokemon1.draw(game.screen, hitbox=game.button_pokemon1)
    game.image_pokemon2.draw(game.screen, hitbox=game.button_pokemon2)
    game.image_pokemon3.draw(game.screen, hitbox=game.button_pokemon3)

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, "Choose a pokemon (for free)" ,hitbox=game.button_battle_message)

def load_game(game):
    # TODO Player and AI object are created here. It's for deck-building/random encounter feature
    game.trainer = Trainer("Player")
    game.enemy = EnemyTrainer("Rival")

    # TODO saveslot/ load different files (trainer name = filename)
    game.trainer.load_pokedex(game.MOOV_TEMPLATE)
    game.game_state = "game_menu"

    for pokemon in game.trainer.pokedex:
        print(pokemon.name)

from random import choice

from model.TrainerClass import Trainer


class EnemyTrainer(Trainer):
    def __init__(self, name):
        super().__init__(name)
        self.pokemon = [] # List of possible pokemon enemy can choose from 


    def add_pokemon_to_list(self, pokemon):
        """To add a pokemon from the template to pokemon list."""
        self.pokemon.append(self.convert_pokemon_to_obj(pokemon))
        self.update_json()

    def remove_pokemon_to_list(self, pokemon):
        """To remove a pokemon from the pokemon list."""
        self.pokemon.remove(self.convert_pokemon_to_obj(pokemon)) 
        self.update_json()
        
    def choose_pokemon(self):
        """Choose a pokemon from the pokemon_list and add it to battle"""
        pokemon = choice(self.pokemon)
        self.pokedex.append(pokemon)

    def remove_pokemon(self):
        """To remove defeated pokemon from our pokedex. pokemon is an object"""
        self.pokedex.remove(self.pokedex[0])

# Add "if hp <= 0" and "if not already_owned" before this when you call it
    def give_pokemon(self, trainer):
        """Copy itself to trainer pokedex and get removed."""
        gift_success = False
        if not trainer.already_owned(self.pokedex[0]):
            trainer.add_pokemon(self.pokedex[0])
            gift_success = True
        self.remove_pokemon()
        return gift_success

    def update_json(self):
        """Update the json from the pokedex list"""
        self.save_json(self.pokemon, "pokemon")

    def load_pokedex(self):
        """When loading a save, add all saved pokemon on trainer object"""
        pokelist = self.load_json("pokemon")
        for pokemon in pokelist:
            self.pokemon.append(self.convert_pokemon_to_obj(pokemon))




"""

# Pokemon pool and list will contain Dict (from there, it'll create object for pokedex)
POKEMON_DB = [{"name": "Bulbosaur", "stats": [1,2,3]}, {"name": "Squirtle", "stats": [3,2,1]}, {"name": "Charizard", "stats": [2,1,3]}]
pokemon_list = [{"name": "Squirtle", "stats": [3,2,1]}]


"""


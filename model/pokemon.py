from random import randint, uniform
from model.moov import Moov
from model.multiplier import type_multiplier
class Pokemon(): 
    '''Class to create a pokemon'''

    def __init__(self,name,type,attack,defence,moov1,moov2,moov_list,level = 5,life = 100):
        '''Initialize the pokemon'''
        self.name = name
        self.sprite = {
            "front": f"media/Pokemons-assets/front/{self.name}_front.png",
            "back": f"media/Pokemons-assets/back/{self.name}_back.png"
        }
        self.type = type
        self.level = level
        self.life = life
        self.attack = attack
        self.defence = defence

        self.moov = [self.create_moov(moov1, moov_list), self.create_moov(moov2, moov_list)]
    
    def get_pokemon(self):
        return f"Name: {self.name}, Type: {self.type}, Level: {self.level}, Attack: {self.attack}, Defence: {self.defence}, Moov: {self.moov1},' ',{self.moov2}; Life: {self.life}"
    
    def create_moov(self, moov_name, moov_list):
        for moov in moov_list:
            if moov["name"] == moov_name:
                return Moov(name=moov["name"], type=moov["type"], accuracy=moov["accuracy"])

    def level_up(self):
        '''Level up the pokemon'''
        self.level += 1
        self.attack += 5
        self.defence += 5
        return f"{self.name} is now level {self.level}"
    
    def evolve(self,new_name,new_type,new_sprite):
        '''Evolve the pokemon'''
        temp_str = self.name
        self.name = new_name
        self.type = new_type
        self.sprite = new_sprite
        return f"{temp_str} has evolved into {new_name}!"
    
    def attack_damage(self, opponent, moov_type):
        '''Calculate the damage of an attack'''
        multi = type_multiplier[(moov_type, opponent.type)]
        damage = round((self.attack * self.level * 0.2 - opponent.defence * opponent.level * 0.05) * multi * uniform(0.8, 1.2))
        return damage
        # return f"{self.name} has inflicted {damage} damage to {opponent.name}!"

    def has_missed(self, moov):
        '''Calculate if the move missed with a random number (0-100).
        
        Gen 1 miss included! (which is 1/100 and not 1/256)'''
        random_nb = randint(0,100)
        accuracy = moov.accuracy
        if accuracy < random_nb: #Gen 1 miss if randint=100 when acc = 100!! (intentional)
            return True
        else:
            return False
        # return f"{self.moov1} has an accuracy of {self.accuracy_mouv1} and {self.moov2} has an accuracy of {self.accuracy_mouv2}"

    def apply_damage(self, game, damage):
        if game.battle.opponent == game.battle.enemy_name:
            game.battle.enemy_current_hp -= damage
            if game.battle.enemy_current_hp < 0:
                game.battle.enemy_current_hp = 0
        else:
            game.battle.trainer_current_hp -= damage
            if game.battle.trainer_current_hp < 0:
                game.battle.trainer_current_hp = 0
        return True
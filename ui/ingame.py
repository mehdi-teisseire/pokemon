from pygame import time, mouse, image, Rect, Surface, MOUSEBUTTONDOWN, SRCALPHA



def display_ingame(game):
    display_background(game)
    display_battle_interface(game)

    match game.ingame_state:
        case "choose_pkmn":
            choose_pokemon_battle(game)
        case "attacking":
            if game.battle.chosen_moov:
                display_attacking_text(game)
            else:
                if game.battle.turn == game.battle.enemy_name:
                    display_enemy_choosing_move(game)
                else:
                    display_attack_choice(game)
        case "mooving":
            if not game.battle.miss_check:
                game.battle.pokemon_missed = game.battle.turn_pkmn.has_missed(game.battle.chosen_moov)
                game.battle.miss_check = True
            if game.battle.pokemon_missed:
                display_moov_missed_text(game)
            else:
                if not game.battle.damage:
                    game.battle.damage = game.battle.turn_pkmn.attack_damage(game.battle.opponent_pkmn, game.battle.chosen_moov.type)
                display_moov_animation(game)
        case "damage":
            if not game.battle.applied_damage:
                game.battle.applied_damage = game.battle.turn_pkmn.apply_damage(game, game.battle.damage)
            display_damage_text(game, game.battle.damage)
        case "turn_finish":
            game.battle.finish_turn(game)
        case "pokemon_ko":
            display_end_results(game)
        case _:
            print("Error selecting an ingame state")

def choose_pokemon_battle(game):
    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, f"Choose a pokemon to send in battle!" ,hitbox=game.button_battle_message)

    background = Surface((game.screen_size[0], 460), SRCALPHA)
    background.fill((0,0,0, 128))
    game.screen.blit(background, (0,0))

    game.sprite_positions = display_pokemon_pokedex(game, game.trainer.pokedex)

def display_pokemon_pokedex(game, pokedex_data):
    """Display all Pokemon sprites in a grid."""
    x, y = 80, 150
    spacing = 70
    sprite_positions = []
    
    for pokemon in pokedex_data:
        sprite = image.load(pokemon.sprite["front"])
        game.screen.blit(sprite, (x, y))
        sprite_positions.append((Rect(x, y, 200, 200), pokemon))
        
        x += spacing
        if x > game.screen.get_width() - spacing:
            x = 80
            y += spacing
            
    return sprite_positions

def display_background(game):
    game.background.draw(game.screen, size=game.screen_size, image_path="media/ui-elements/MDPokemonBattle_Notextbox.png")
    game.healthbox.draw(game.screen, (700,25), (470, 115), image_path="media/ui-elements/MDPokemonBattle_Healthbox.png")
    game.button_quit.draw(game.screen)
    game.button_quit_image.draw(game.screen,hitbox=game.button_quit,image_path="media/ui-elements/cross.svg")

def display_battle_interface(game):
    game.hitbox_trainer_pkmn.draw(game.screen)
    game.hitbox_enemy_pkmn.draw(game.screen)
    game.trainer_pokemon.draw(game.screen, image_path=f"media/Pokemons-assets/back/{game.battle.trainer_pokemon.name}_back.png", hitbox=game.hitbox_trainer_pkmn)
    game.enemy_pokemon.draw(game.screen, image_path=f"media/Pokemons-assets/front/{game.battle.enemy_pokemon.name}_front.png", hitbox=game.hitbox_enemy_pkmn)
    

    game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.name}", (70,50)) 
    game.ingame_text.draw(game.screen, f"{game.battle.enemy_pokemon.name}", (740,50)) 
    
    game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.level}", (350,55)) 
    game.ingame_text.draw(game.screen, f"{game.battle.enemy_pokemon.level}", (1040,55)) 

    game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.current_health}/{game.trainer.pokedex[0].life}", (50,85)) 
    game.ingame_text.draw(game.screen, f"{game.battle.enemy_pokemon.current_health}/{game.enemy.pokedex[0].life}", (720,85)) 

    game.health_bar.draw(game.screen, (227, 92), (1.87* game.battle.trainer_pokemon.current_health * 100 / game.trainer.pokedex[0].life, 15))
    game.health_bar.draw(game.screen, (908, 90), (1.98* game.battle.enemy_pokemon.current_health * 100 / game.enemy.pokedex[0].life, 17))

# To allow the player to choose an attack
def display_attack_choice(game):
    """Show the moov buttons and allow to choose an attack"""
    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)

    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_moov1.draw(game.screen, game.battle.turn_pkmn.moov[0].name) 
    game.button_moov2.draw(game.screen, game.battle.turn_pkmn.moov[1].name)
    game.button_change_pkmn.draw(game.screen, "pokemons")

    game.background_button_moov.draw(game.screen, hitbox=game.button_moov1)
    game.background_button_moov.draw(game.screen, hitbox=game.button_moov2)
    game.background_button_moov.draw(game.screen, hitbox=game.button_change_pkmn)
    
    game.text_button_moov.draw(game.screen, game.battle.turn_pkmn.moov[0].name, hitbox=game.button_moov1)    
    game.text_button_moov.draw(game.screen, game.battle.turn_pkmn.moov[1].name, hitbox=game.button_moov2)
    game.text_button_moov.draw(game.screen, "Pokemons", hitbox=game.button_change_pkmn)  
    
def display_attacking_text(game):
    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, f"{game.battle.turn}'s {game.battle.turn_pkmn.name} uses {game.battle.chosen_moov.name}!!" ,hitbox=game.button_battle_message)
    
    custom_wait(game, "mooving", 1000)

def display_moov_animation(game):
    if game.battle.turn == game.battle.trainer_name:
        game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")
        game.hitbox_trainer_pkmn.coord = (game.hitbox_trainer_pkmn.coord[0]+3, game.hitbox_trainer_pkmn.coord[1])
    else:
        game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_mooving.png")
        game.hitbox_enemy_pkmn.coord = (game.hitbox_enemy_pkmn.coord[0]-3, game.hitbox_enemy_pkmn.coord[1])

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, "" ,hitbox=game.button_battle_message)
    if time.get_ticks() >= game.delay:
        game.delay = time.get_ticks() + 2000
        game.ingame_state = "damage"

        reset_animation(game)

def reset_animation(game):
    game.hitbox_trainer_pkmn.coord = (100, 250)
    game.hitbox_enemy_pkmn.coord = (750,170)

def display_damage_text(game, damage):
    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, f"{game.battle.turn}'s {game.battle.turn_pkmn.name} has inflicted {damage} damage to {game.battle.opponent_pkmn.name}!" ,hitbox=game.button_battle_message)
    
    custom_wait(game, "turn_finish", 0)

def display_moov_missed_text(game):
    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, f"{game.battle.chosen_moov.name} has missed!!" ,hitbox=game.button_battle_message)
    
    custom_wait(game, "turn_finish", 0)

def display_enemy_choosing_move(game):
    """Display a message to let AI play without interferences"""
    game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

    game.button_battle_message.draw(game.screen)
    game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
    game.text_battle_message.draw(game.screen, f"{game.battle.enemy_name} is picking a move!" ,hitbox=game.button_battle_message)
   
    if time.get_ticks() >= game.delay:
        game.delay = time.get_ticks() + 1500
        game.ingame_state = "attacking"
        game.battle.chosen_moov = game.battle.ia_choose_moov(game)

def display_end_results(game):
    if not game.battle.won:
        game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

        game.button_battle_message.draw(game.screen)
        game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
        game.text_battle_message.draw(game.screen, f"Too bad, {game.battle.trainer_name}'s {game.battle.trainer_pokemon.name} had been defeated by {game.battle.enemy_name}'s {game.battle.enemy_pokemon.name}!!" ,hitbox=game.button_battle_message)
        game.hitbox_trainer_pkmn.coord = (game.hitbox_trainer_pkmn.coord[0], game.hitbox_trainer_pkmn.coord[1]+50)
        
    else:
        game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_stand.png")

        game.button_battle_message.draw(game.screen)
        game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
        game.text_battle_message.draw(game.screen, f"Good job, {game.battle.trainer_name}'s {game.battle.trainer_pokemon.name} had defeated {game.battle.enemy_name}'s {game.battle.enemy_pokemon.name}!!" ,hitbox=game.button_battle_message)
        game.hitbox_enemy_pkmn.coord = (game.hitbox_enemy_pkmn.coord[0], game.hitbox_enemy_pkmn.coord[1]+50)

    if time.get_ticks() >= game.delay:
        game.delay = time.get_ticks() + 5000
        if not game.battle.won:
            game.enemy.remove_pokemon()
            game.trainer.remove_pokemon(game.battle.trainer_pokemon)
                
        else:
            game.battle.gave_pokemon = game.enemy.give_pokemon(game.trainer)
        
        if len(game.trainer.pokedex) < 1:
            game.game_state = "intro"
            game.mixer.music.stop()
            game.mixer.music.load('media/audio/bgm_menu.mp3')
            game.mixer.music.play(-1)
            game.battle_start = False
            game.battle.ingame_state = "attacking"
            reset_animation(game)
        else:
            game.game_state = "battle_end"
            game.mixer.music.stop()
            game.mixer.music.load('media/audio/bgm_battle_end.mp3')
            game.mixer.music.play(-1)
            game.battle_start = False
            game.battle.ingame_state = "attacking"
            game.battle.turn_pkmn.level_up()
            reset_animation(game)


def custom_wait(game, state, wait_time = 1000):
    if time.get_ticks() >= game.delay:
        game.delay = time.get_ticks() + wait_time
        game.ingame_state = state

def display_battle_end(game):    
    if game.battle.won:
        game.background.draw(game.screen, size=game.screen_size, image_path="media/ui-elements/MDPokemonBattle_Notextbox.png")
        game.hitbox_trainer_pkmn.draw(game.screen)
        game.trainer_pokemon.draw(game.screen, image_path=f"media/Pokemons-assets/back/{game.battle.trainer_pokemon.name}_back.png", hitbox=game.hitbox_trainer_pkmn)

        game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.name}", (70,50)) 
        game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.level}", (350,55)) 
        game.ingame_text.draw(game.screen, f"{game.battle.trainer_pokemon.current_health}/{game.trainer.pokedex[0].life}", (50,85)) 
        game.health_bar.draw(game.screen, (227, 92), (1.87* game.battle.trainer_pokemon.current_health * 100 / game.trainer.pokedex[0].life, 15))

        if game.battle.gave_pokemon:
            game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_sad.png")
            
            game.button_battle_message.draw(game.screen)
            game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
            game.text_battle_message.draw(game.screen, f"{game.battle.enemy_name} gave you a {game.battle.enemy_pokemon.name}!! So cool!" ,hitbox=game.button_battle_message)
           
   
        else:
            game.rival.draw(game.screen, (1050,150), (85,150), "media/ui-elements/Rival_sad.png")
            
            game.button_battle_message.draw(game.screen)
            game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
            game.text_battle_message.draw(game.screen, f"{game.battle.enemy_name} gave you a {game.battle.enemy_pokemon.name}!! Unfortunately, you already had one..." ,hitbox=game.button_battle_message)
   
    else:
        game.background.draw(game.screen, size=game.screen_size, image_path="media/ui-elements/dead_screen.jpg")
        game.button_battle_message.draw(game.screen)
        game.background_battle_message.draw(game.screen, hitbox=game.button_battle_message)
        game.text_battle_message.draw(game.screen, f"{game.battle.trainer_name}'s {game.battle.trainer_pokemon.name} is dead forever..." ,hitbox=game.button_battle_message)
   
    if time.get_ticks() >= game.delay:
       # game.battle.turn_pkmn.level_up()
        display_evolve(game)
        game.delay = time.get_ticks() + 50000
        game.save_json(game.trainer.pokedex, 'pokedex')
        game.mixer.music.stop()
        game.mixer.music.load('media/audio/bgm_menu.mp3')
        game.mixer.music.play(-1)
        if not game.trainer.pokedex:
            game.game_state = "intro"
        else:
            for pokemon in game.trainer.pokedex:
                pokemon.current_health = pokemon.life
            game.game_state = "game_menu"


def display_evolve(game):
    if game.trainer.pokedex[0].evolve_data:
        if game.trainer.pokedex[0].level == game.trainer.pokedex[0].evolve_data["level"]:
                game.trainer.pokedex[0].evolve(game.trainer.pokedex[0].evolve_data["name"], game.trainer.pokedex[0].evolve_data["type"])
   

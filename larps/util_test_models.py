from .models import *
from .config import *

def create_player(player_info):
    user = User(username=player_info["username"], first_name=player_info["first_name"], last_name=player_info["last_name"])
    user.save()
    player = Player(user=user, gender=player_info["gender"], chest=player_info["chest"], waist=player_info["waist"])
    player.save()
    return player

def create_group(group_name):
    larp = Larp(name = larp_name())
    larp.save()
    group = Group(larp=larp, name=group_name)
    group.save()
    return group

def create_character_assigment(group, player_info, character_name):
    run = 1
    player = create_player(player_info)
    character = Character(name=character_name, group=group)
    character.save()
    assigment = CharacterAssigment(user=player.user, character=character, run=run)
    assigment.save()
    return assigment

def create_characters_assigments(group, example_players, example_characters):
    assigments = []
    for n in range(0, 2):
        player_info = example_players[n]
        character_name = example_characters[n]
        a = create_character_assigment(group, player_info, character_name)
        assigments.append(a)
    return assigments

def create_uniform(group_name):
    larp = Larp(name=larp_name())
    larp.save()
    group = Group(name=group_name, larp=larp)
    group.save()
    uniform = Uniform(group=group, name=group_name)
    uniform.save()
    return uniform

def create_uniform_size(size_information):
    uniform = create_uniform(group_name="")
    size = UniformSize(uniform=uniform)
    size.set_values(size_information)
    size.save()
    return size

def create_uniform_with_sizes(example_sizes):
    uniform = create_uniform(group_name="")
    for size_information in example_sizes:
        size = UniformSize(uniform=uniform)
        size.set_values(size_information)
        size.save()
    return uniform

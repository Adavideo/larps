from larps.models import *
from larps.config import *


def create_user(player_info):
    user_search = User.objects.filter(username=player_info["username"])
    if user_search:
        return user_search[0]
    user = User(username=player_info["username"], first_name=player_info["first_name"], last_name=player_info["last_name"])
    user.save()
    return user

def get_diet(diet_name):
    diet = None
    diet_search = DietaryRestriction.objects.filter(name=diet_name)
    if diet_search:
        diet = diet_search[0]
    return diet

def create_player(player_info):
    user = create_user(player_info)
    player_search = Player.objects.filter(user=user)
    if player_search:
        return player_search[0]
    diet = get_diet(player_info["diet"])
    player = Player(user=user, gender=player_info["gender"], chest=player_info["chest"], waist=player_info["waist"], dietary_restrictions=diet)
    player.save()
    return player

def create_diets(diets):
    for diet_name in diets:
        new_diet = DietaryRestriction(name=diet_name)
        new_diet.save()

def create_group(group_name):
    group_search = Group.objects.filter(name=group_name)
    if group_search:
        return group_search[0]
    larp = Larp(name = larp_name())
    larp.save()
    group = Group(larp=larp, name=group_name)
    group.save()
    return group

def create_character(character_name, group=None, group_name=""):
    character_search = Character.objects.filter(name=character_name)
    if character_search:
        return character_search[0]
    if not group and group_name:
        group = Group(name=group_name)
    character = Character(name=character_name, group=group)
    character.save()
    return character

def contains_profile_info(player_info):
    return player_info["gender"] or player_info["chest"] or player_info["waist"]

def create_character_assigment(group, player_info, character_name, run=1):
    if contains_profile_info(player_info):
        player = create_player(player_info)
        user=player.user
    else:
        user = create_user(player_info)
        user.save()
    character = create_character(character_name, group)
    assigment = CharacterAssigment(user=user, character=character, run=run)
    assigment.save()
    return assigment

def create_characters_assigments(group, players, characters, run=1):
    assigments = []
    if len(players) > len(characters):
        n = len(characters)
    else:
        n = len(players)
    for i in range(0, n):
        player_info = players[i]
        character_name = characters[i]
        assigment = create_character_assigment(group=group, player_info=player_info, character_name=character_name, run=run)
        assigment.save()
        assigments.append(assigment)
    return assigments

def create_uniform(group_name="", group=None):
    if not group:
        group = create_group(group_name)
    uniform = Uniform(group=group, name=group_name)
    uniform.save()
    return uniform

def create_uniform_size(size_information, group_name=""):
    uniform = create_uniform(group_name)
    size = UniformSize(uniform=uniform)
    size.set_values(size_information)
    size.save()
    return size

def create_uniform_with_sizes(sizes, group_name="", group=None):
    uniform = create_uniform(group_name=group_name, group=group)
    for size_information in sizes:
        size = UniformSize(uniform=uniform)
        size.set_values(size_information)
        size.save()
    return uniform

def create_uniform_with_players_and_sizes(sizes, players_info, characters_names, group_name="", run=1):
    group = create_group(group_name=group_name)
    uniform = create_uniform_with_sizes(sizes, group_name=group_name)
    assigments = create_characters_assigments(group, players_info, characters_names, run)
    return uniform

def create_uniform_with_player_in_several_runs(sizes, players_info, characters_names, player_in_several_runs, group_name="", runs=2):
    uniform = create_uniform_with_players_and_sizes(sizes, players_info, characters_names, group_name=group_name, run=1)
    for i in range(2,runs+1):
        create_character_assigment(uniform.group, player_in_several_runs, characters_names[1], run=i)
    return uniform

def create_group_with_diet_info(larp, players_info, characters_names, group_name=""):
    group = Group(larp=larp, name=group_name)
    group.save()
    players_info1 = [ players_info[0], players_info[1] ]
    players_info2 = [ players_info[2], players_info[3] ]
    characters_names1 = [ characters_names[0], characters_names[1] ]
    characters_names2 = [ characters_names[2], characters_names[3] ]
    create_characters_assigments(group, players_info1, characters_names1, run=1)
    create_characters_assigments(group, players_info2, characters_names1, run=2)


def create_larp_with_diet_info(players_info, characters_names, group_name="", larp_name=""):
    larp = Larp(name=larp_name)
    larp.save()
    create_group_with_diet_info(larp, players_info, characters_names, group_name)
    return larp

def test_character_diets(test, original_list, returned_info):
    for info in original_list:
        name = info["first_name"] + " " + info["last_name"]
        if name == returned_info["player"]:
            original_info = info
    test.assertEqual(returned_info["diet"].name, original_info["diet"])

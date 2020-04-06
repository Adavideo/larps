from larps.models import DietaryRestriction, Larp, Group
from .examples import example_diets, example_players_with_diets1, example_players_with_diets2
from .examples import example_players_incomplete, example_characters1, example_characters2
from .util_test import create_characters_assigments

# Initialize for food testing

def create_diets(diets=example_diets):
    for diet_name in diets:
        new_diet = DietaryRestriction(name=diet_name)
        new_diet.save()

def create_group_with_diet_info(larp, players_info, characters_names, diet_info="", group_name=""):
    group = Group(larp=larp, name=group_name)
    group.save()
    players_info1 = [ players_info[0], players_info[1] ]
    players_info2 = [ players_info[2], players_info[3] ]
    if diet_info:
        diet_info1 = [ diet_info[0], diet_info[1] ]
        diet_info2 = [ diet_info[2], diet_info[3] ]
    else:
        diet_info1 = ""
        diet_info2 = ""
    create_characters_assigments(group, players_info1, characters_names, run=1, diet_info=diet_info1)
    create_characters_assigments(group, players_info2, characters_names, run=2, diet_info=diet_info2)

def create_larp_with_diet_info(players_info=example_players_with_diets1, characters_names=example_characters1, diet_info="", group_name="", larp_name=""):
    create_diets()
    larp = Larp(name=larp_name)
    larp.save()
    create_group_with_diet_info(larp, players_info, characters_names, diet_info=diet_info, group_name=group_name)
    return larp

def create_all_1_group():
    larp = create_larp_with_diet_info(example_players_with_diets1, example_characters1, group_name="group1")
    return larp

def create_all_2_groups():
    larp = create_all_1_group()
    create_group_with_diet_info(larp, example_players_with_diets2, example_characters2, group_name="group2")
    return larp

def create_all_without_profiles():
    larp = Larp(name="")
    larp.save()
    group = Group(larp=larp, name="")
    group.save()
    create_characters_assigments(group=group, players=example_players_incomplete)
    return larp


# OTHER util functions

def test_character_diets(test, original_list, returned_info):
    for info in original_list:
        name = info["first_name"] + " " + info["last_name"]
        if name == returned_info["player"]:
            original_info = info
    test.assertEqual(returned_info["diet"], original_info["diet"])

from django.test import TestCase
from larps.models import Group, Larp, DietaryRestriction
from .util_test import create_diets, create_characters_assigments
from larps.food import *


example_players_with_diets1 = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75, "diet":"" },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78, "diet":"Vegan" },
    { "username": "Manolo_Garcia", "first_name": "Manolo", "last_name": "Garcia", "gender":"male", "chest":100, "waist":90, "diet":"" },
    { "username": "Paco_Garcia", "first_name": "Paco", "last_name": "Garcia", "gender":"male", "chest":102, "waist":86, "diet":"Vegan" },
]

example_players_with_diets2 = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"Vegetarian" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"" },
    { "username": "Juan_Perez", "first_name": "Juan", "last_name": "Perez", "gender":"male", "chest":100, "waist":90, "diet":"" },
    { "username": "Carlos_Hernandez", "first_name": "Carlos", "last_name": "Hernandez", "gender":"male", "chest":102, "waist":86, "diet":"Vegan" },
]

example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"" },
]

diets = [ "", "Vegetarian", "Vegan" ]

example_characters = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker", "Peter Parker", "Leopold Fitz" ]


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
    create_diets(diets)
    larp = Larp(name=larp_name)
    larp.save()
    create_group_with_diet_info(larp, players_info, characters_names, group_name)
    return larp

def test_character_diets(test, original_list, returned_info):
    for info in original_list:
        name = info["first_name"] + " " + info["last_name"]
        if name == returned_info["player"]:
            original_info = info
    test.assertEqual(returned_info["diet"], original_info["diet"])

def create_all_1_group():
    larp = create_larp_with_diet_info(example_players_with_diets1, example_characters, group_name="group1", larp_name="")
    return larp

def create_all_2_groups():
    larp = create_all_1_group()
    create_group_with_diet_info(larp, example_players_with_diets2, example_characters, group_name="group2")
    return larp

def create_all_without_profiles():
    larp = Larp(name="")
    larp.save()
    group = Group(larp=larp, name="")
    group.save()
    create_characters_assigments(group, example_players_incomplete, example_characters, run=1)
    return larp


class FoodTests(TestCase):

    def test_get_runs_number(self):
        larp = create_all_1_group()
        assigments = larp.get_character_assigments()
        runs_number = get_runs_number(assigments)
        self.assertIs(runs_number, 2)

    def test_get_empty_run_list_one_run(self):
        number_of_runs = 1
        run_list = get_empty_run_list(number_of_runs)
        self.assertIs(len(run_list), 1)
        self.assertEqual(run_list, [ [] ])

    def test_get_empty_run_list_two_runs(self):
        number_of_runs = 2
        run_list = get_empty_run_list(number_of_runs)
        self.assertIs(len(run_list), 2)
        self.assertEqual(run_list, [ [], [] ])

    def test_get_players_diets(self):
        # Initialize
        larp = create_all_1_group()
        assigments = larp.get_character_assigments()
        number_of_runs = get_runs_number(assigments)
        # Obtain results
        players_diets_all_runs = get_players_diets(assigments, number_of_runs)
        # Validate
        self.assertEqual(len(players_diets_all_runs), number_of_runs)
        for players_diets in players_diets_all_runs:
            self.assertEqual(len(players_diets), 2)
            for player_diet in players_diets:
                test_character_diets(test=self, original_list=example_players_with_diets1,returned_info=player_diet)

    def test_get_players_diets_without_profiles(self):
        # Initialize
        larp = create_all_without_profiles()
        assigments = larp.get_character_assigments()
        number_of_runs = 1
        # Obtain results
        players_diets_all_runs = get_players_diets(assigments, number_of_runs)
        # Validate
        self.assertEqual(len(players_diets_all_runs), 1)
        for player_diet in players_diets_all_runs[0]:
            self.assertEqual(player_diet["diet"], "Not provided yet")

    def test_get_food_empty(self):
        larp = Larp(name="")
        food = larp.get_food()
        self.assertEqual(food, {'players_diets': [], 'diets_amounts': []})

    def test_get_food_1_group(self):
        # Initialize
        larp = create_all_1_group()
        # Obtain results
        result = larp.get_food()
        players_diets_all_runs = result["players_diets"]
        diets_amounts_all_runs = result["diets_amounts"]
        # Validate
        self.assertIs(len(players_diets_all_runs), 2)
        self.assertIs(len(diets_amounts_all_runs), 2)

    def test_get_food_2_groups(self):
        # Initialize
        larp = create_all_2_groups()
        # Obtain results
        result = larp.get_food()
        players_diets_all_runs = result["players_diets"]
        diets_amounts_all_runs = result["diets_amounts"]
        # Validate
        self.assertIs(len(players_diets_all_runs), 2)
        self.assertIs(len(diets_amounts_all_runs), 2)

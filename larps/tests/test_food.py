from django.test import TestCase
from larps.models import Group, Larp, DietaryRestriction, Player
from .util_test import create_diets, create_characters_assigments
from larps.food import *


example_players_with_diets1 = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75, "diet":"none", "comments":"" },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78, "diet":"Vegan", "comments":"" },
    { "username": "Manolo_Garcia", "first_name": "Manolo", "last_name": "Garcia", "gender":"male", "chest":100, "waist":90, "diet":"none", "comments":"" },
    { "username": "Paco_Garcia", "first_name": "Paco", "last_name": "Garcia", "gender":"male", "chest":102, "waist":86, "diet":"Vegan", "comments":"" },
]

example_players_with_diets2 = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"female", "chest":0, "waist":0, "diet":"Vegetarian", "comments":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"female", "chest":0, "waist":0, "diet":"none", "comments":"" },
    { "username": "Juan_Perez", "first_name": "Juan", "last_name": "Perez", "gender":"male", "chest":100, "waist":90, "diet":"none", "comments":"" },
    { "username": "Carlos_Hernandez", "first_name": "Carlos", "last_name": "Hernandez", "gender":"male", "chest":102, "waist":86, "diet":"Vegan", "comments":"" },
]

example_player_food_info = [
    { "diet":"Vegetarian", "comments":"", 'allergies': "", 'food_allergies' : "", 'food_intolerances': "" },
    { "diet":"none", "comments":"", 'allergies': "polen", 'food_allergies' : "", 'food_intolerances': "lactose" },
    { "diet":"none", "comments":"", 'allergies': "", 'food_allergies' : "peanuts", 'food_intolerances': "" },
    { "diet":"Vegan", "comments":"", 'allergies': "", 'food_allergies' : "pineaple", 'food_intolerances': "lactose" },
]

example_comments = [
    "",
    "intolerant to: lactose",
    "allergies: peanuts",
    "allergies: pineaple, intolerant to: lactose"
]

example_diets_counts = [
    { "none" : 2, "Vegetarian": 1, "Vegan": 1 },
    { "none" : 2, "Vegetarian": 0, "Vegan": 2 },
]

example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"", "comments":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"", "comments":"" },
]

diets = [ "Vegetarian", "Vegan", "none" ]

example_characters1 = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker" ]
example_characters2 = [ "Peter Parker", "Leopold Fitz", "Tony Stark", "Gemma Simmons" ]

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

def create_larp_with_diet_info(players_info, characters_names, diet_info="", group_name="", larp_name=""):
    create_diets(diets)
    larp = Larp(name=larp_name)
    larp.save()
    create_group_with_diet_info(larp, players_info, characters_names, diet_info=diet_info, group_name=group_name)
    return larp

def test_character_diets(test, original_list, returned_info):
    for info in original_list:
        name = info["first_name"] + " " + info["last_name"]
        if name == returned_info["player"]:
            original_info = info
    test.assertEqual(returned_info["diet"], original_info["diet"])

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
    create_characters_assigments(group, example_players_incomplete, example_characters1, run=1)
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

    def test_get_players_diets_with_comments(self):
        # Initialize
        larp = create_larp_with_diet_info(example_players_with_diets1, example_characters1, diet_info=example_player_food_info)
        # Obtain results
        result = larp.get_food()
        diets_all_runs = result["players_diets"]
        # Validate
        count = 0
        for run in diets_all_runs:
            for player_diet in run:
                self.assertEqual(player_diet["comments"], example_comments[count])
                count += 1


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

    def test_get_diets_amounts_no_diets(self):
        # Initialize
        larp = create_all_without_profiles()
        assigments = larp.get_character_assigments()
        number_of_runs = 1
        # Obtain results
        assigments = larp.get_character_assigments()
        number_of_runs = get_runs_number(assigments)
        players_diets = get_players_diets(assigments, number_of_runs)
        diets_types = DietaryRestriction.objects.all()
        all_runs_diets = get_diets_amounts(players_diets, number_of_runs, diets_types)
        # Validate
        self.assertIs(len(all_runs_diets), 1)
        for run_diets in all_runs_diets:
            self.assertEqual(run_diets, [])

    def test_get_diets_amounts_empty(self):
        # Initialize
        create_diets(diets)
        larp = create_all_without_profiles()
        assigments = larp.get_character_assigments()
        number_of_runs = 1
        # Obtain results
        assigments = larp.get_character_assigments()
        number_of_runs = get_runs_number(assigments)
        players_diets = get_players_diets(assigments, number_of_runs)
        diets_types = DietaryRestriction.objects.all()
        all_runs_diets = get_diets_amounts(players_diets, number_of_runs, diets_types)
        # Validate
        self.assertIs(len(all_runs_diets), 1)
        for run_diets in all_runs_diets:
            for diet in run_diets:
                diet_name = diet["diet_name"]
                self.assertIs(diet["amount"], 0)

    def test_get_diets_amounts(self):
        # Initialize
        larp = create_all_2_groups()
        # Obtain results
        assigments = larp.get_character_assigments()
        number_of_runs = get_runs_number(assigments)
        players_diets = get_players_diets(assigments, number_of_runs)
        diets_types = DietaryRestriction.objects.all()
        all_runs_diets = get_diets_amounts(players_diets, number_of_runs, diets_types)
        # Validate
        self.assertIs(len(all_runs_diets), 2)
        run = 0
        for run_diets in all_runs_diets:
            for diet in run_diets:
                diet_name = diet["diet_name"]
                example_amount = example_diets_counts[run][diet_name]
                self.assertIs(diet["amount"], example_amount)
            run += 1

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

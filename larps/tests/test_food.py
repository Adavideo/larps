from django.test import TestCase
from larps.food import get_runs_number, get_players_diets, get_empty_run_list, get_diets_amounts
from .util_test import create_characters_assigments
from .util_test_food import *
from .examples import example_player_food_info, example_diets_counts, example_comments


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
        larp = create_larp_with_diet_info(diet_info=example_player_food_info)
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
        create_diets()
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

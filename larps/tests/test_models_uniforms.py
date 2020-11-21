from django.test import TestCase
from django.contrib.auth.models import User
from .util_test import create_player
from .util_test_uniforms import *
from .examples import example_sizes, example_players_complete, example_sizes_info, empty_size_info


class UniformModelTests(TestCase):

    def test_create_uniform(self):
        uniform = create_uniform(group_name=example_groups[0])
        self.assertEqual(uniform.group.name, example_groups[0])
        self.assertEqual(uniform.name, example_groups[0])

    def test_create_uniform_with_full_info(self):
        uniform = create_uniform(group_name=example_groups[0])
        color = "Red"
        uniform.color = color
        self.assertEqual(uniform.group.name, example_groups[0])
        self.assertEqual(uniform.name, example_groups[0])

    def test_create_uniform_size_with_no_info(self):
        uniform = create_uniform(group_name=example_groups[0])
        size = UniformSize(uniform=uniform)
        self.assertEqual(size.uniform.name, example_groups[0])

    def test_create_uniform_size_with_info(self):
        size_information = example_sizes[0]
        size = create_uniform_size(size_information)
        self.assertEqual(size.gender, size_information["gender"])
        self.assertEqual(size.american_size, size_information["american_size"])
        self.assertEqual(size.european_size, size_information["european_size"])
        self.assertEqual(size.chest_min, int(size_information["chest_min"]))
        self.assertEqual(size.chest_max, int(size_information["chest_max"]))
        self.assertEqual(size.waist_min, int(size_information["waist_min"]))
        self.assertEqual(size.waist_max, int(size_information["waist_max"]))
        self.assertEqual(str(size), "female. S/38 chest(86,90) waist(70,74)")

    def test_create_uniform_size_with_empty_info(self):
        size_information = empty_size_info
        size = create_uniform_size(size_information)
        self.assertEqual(size.gender, size_information["gender"])
        self.assertEqual(size.american_size, size_information["american_size"])
        self.assertEqual(size.european_size, size_information["european_size"])
        self.assertEqual(size.chest_min, 0)
        self.assertEqual(size.chest_max, 0)
        self.assertEqual(size.waist_min, 0)
        self.assertEqual(size.waist_max, 0)
        self.assertEqual(str(size), " chest(0,0) waist(0,0)")

    def test_recommend_sizes_perfect_fit(self):
        player_info = example_players_complete[0]
        player = create_player(player_info=player_info)
        uniform = create_uniform_with_sizes(example_sizes)
        sizes = uniform.recommend_sizes(player)
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].gender,"female")
        self.assertEqual(sizes[0].american_size,"M")
        self.assertEqual(sizes[0].european_size,"40")
        self.assertEqual(str(sizes[0]), "female. M/40 chest(90,94) waist(74,78)")

    def test_recommend_sizes_valid_fit(self):
        uniform = create_uniform_with_sizes(example_sizes)
        player_info = example_players_complete[0]
        player = create_player(player_info=player_info)
        sizes = uniform.recommend_sizes(player=player)
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].american_size,"M")
        self.assertEqual(sizes[0].european_size,"40")
        self.assertEqual(str(sizes[0]), "female. M/40 chest(90,94) waist(74,78)")

    def test_perfect_fit_true(self):
        chest = 90
        waist = 75
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.perfect_fit(chest, waist), True)

    def test_perfect_fit_false(self):
        chest = 90
        waist = 75
        size = create_uniform_size(example_sizes[0])
        self.assertIs(size.perfect_fit(chest, waist), False)

    def test_waist_fit_true(self):
        waist = 75
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.waist_fit(waist), True)

    def test_waist_fit_false(self):
        waist = 75
        size = create_uniform_size(example_sizes[0])
        self.assertIs(size.waist_fit(waist), False)

    def test_chest_fit_true(self):
        chest = 90
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.chest_fit(chest), True)

    def test_chest_fit_false(self):
        chest = 89
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.chest_fit(chest), False)

    def test_chest_minimum_fit_true(self):
        chest = 89
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.chest_minimum_fit(chest), True)

    def test_chest_minimum_fit_size_too_small(self):
        chest = 91
        size = create_uniform_size(example_sizes[0])
        self.assertIs(size.chest_minimum_fit(chest), False)

    def test_waist_minimum_fit_true(self):
        waist = 74
        size = create_uniform_size(example_sizes[1])
        self.assertIs(size.waist_minimum_fit(waist), True)

    def test_waist_minimum_fit_size_too_small(self):
        waist = 80
        size = create_uniform_size(example_sizes[0])
        self.assertIs(size.waist_minimum_fit(waist), False)

    def test_get_sizes_with_quantities_empty(self):
        players = []
        uniform = Uniform(name="")
        sizes_with_quantities = uniform.get_sizes_with_quantities(players)
        self.assertEqual(sizes_with_quantities, [])

    def test_get_sizes_with_quantities_no_players(self):
        players = []
        uniform = create_uniform_with_sizes(example_sizes)
        sizes_with_quantities = uniform.get_sizes_with_quantities(players)
        self.assertEqual(len(sizes_with_quantities), len(example_sizes))
        for i in range(0,len(example_sizes)):
            self.assertEqual(sizes_with_quantities[i]["name"], example_sizes[i]["american_size"]+" / "+example_sizes[i]["european_size"])
            self.assertEqual(sizes_with_quantities[i]["quantity"], 0)
            self.assertEqual(str(sizes_with_quantities[i]["info"]), example_sizes_info[i])

    def test_get_sizes_with_quantities(self):
        uniform = create_uniform_with_players_and_sizes(sizes=example_sizes, group_name="Pilots")
        players_with_sizes = uniform.get_players_with_recommended_sizes()
        sizes_with_quantities = uniform.get_sizes_with_quantities(players_with_sizes)
        self.assertEqual(len(sizes_with_quantities), len(example_sizes))
        for i in range(0,len(example_sizes)):
            self.assertEqual(sizes_with_quantities[i]["name"], example_sizes[i]["american_size"]+" / "+example_sizes[i]["european_size"])
            self.assertEqual(str(sizes_with_quantities[i]["info"]), example_sizes_info[i])
        self.assertEqual(sizes_with_quantities[0]["quantity"], 0)
        self.assertEqual(sizes_with_quantities[1]["quantity"], 1)
        self.assertEqual(sizes_with_quantities[2]["quantity"], 1)
        self.assertEqual(sizes_with_quantities[3]["quantity"], 0)
        self.assertEqual(sizes_with_quantities[4]["quantity"], 0)
        self.assertEqual(sizes_with_quantities[5]["quantity"], 2)

    def test_update_quantities_no_valid_sizes(self):
        uniform = create_uniform("")
        players_with_sizes = uniform.get_players_with_recommended_sizes()
        sizes_with_quantities = uniform.initialize_sizes_with_quantities()
        uniform.update_quantities(sizes_with_quantities, players_with_sizes)

    def test_get_players_with_recommended_sizes(self):
        uniform = create_uniform_with_players_and_sizes(sizes=example_sizes, players_info=example_players_complete, group_name="Mechanics")
        players_with_sizes = uniform.get_players_with_recommended_sizes()
        self.assertEqual(len(players_with_sizes), len(example_players_complete))

    def test_get_players_with_recommended_sizes_a_player_in_several_runs(self):
        player_repeated = example_players_complete[1]
        uniform = create_uniform_with_player_in_several_runs(sizes=example_sizes, players_info=example_players_complete,
                                                            characters_names=example_characters, player_in_several_runs=player_repeated,
                                                            group_name=example_groups[0], runs=3)
        players_with_sizes = uniform.get_players_with_recommended_sizes()
        # Ensure that the player in several runs does not appear repeated in the list that this function returns.
        self.assertEqual(len(players_with_sizes), len(example_players_complete))
        player_returned = players_with_sizes[1]
        self.assertEqual(player_returned["info"].user.username, player_repeated["username"])
        # Ensure that only returns one size for the repeated player
        self.assertEqual(len(player_returned["sizes"]), 1)
        # Ensure that it returns the correct size for the repeated player
        self.assertEqual(str(player_returned["sizes"][0]), "female. M/42 chest(94,98) waist(78,82)")

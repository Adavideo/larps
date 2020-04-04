from django.test import TestCase
from django.contrib.auth.models import User

from larps.models import *
from larps.config import larp_name
from .util_test import *

example_characters = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker", "Peter Parker", "Leopold Fitz" ]
example_groups = [ "Scientists", "Doctors", "Mecanics" ]

example_players_complete = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75, "diet":"" },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78, "diet":"" },
    { "username": "Manolo_Garcia", "first_name": "Manolo", "last_name": "Garcia", "gender":"male", "chest":100, "waist":90, "diet":"" },
    { "username": "Paco_Garcia", "first_name": "Paco", "last_name": "Garcia", "gender":"male", "chest":102, "waist":86, "diet":"" },
]

example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"" },
]


example_sizes = [
         {  "gender":"female", "american_size":"S", "european_size":"38", "chest_min":"86", "chest_max":"90", "waist_min":"70", "waist_max":"74" },
         {  "gender":"female", "american_size":"M", "european_size":"40", "chest_min":"90", "chest_max":"94", "waist_min":"74", "waist_max":"78" },
         {  "gender":"female", "american_size":"M", "european_size":"42", "chest_min":"94", "chest_max":"98", "waist_min":"78", "waist_max":"82" },
         {  "gender":"male", "american_size":"M", "european_size":"46", "chest_min":"90", "chest_max":"94", "waist_min":"78", "waist_max":"82" },
         {  "gender":"male", "american_size":"M", "european_size":"48", "chest_min":"94", "chest_max":"98", "waist_min":"82", "waist_max":"86" },
         {  "gender":"male", "american_size":"L", "european_size":"50", "chest_min":"98", "chest_max":"102", "waist_min":"86", "waist_max":"90" },
     ]

example_sizes_info = [
    "female. S/38 chest(86,90) waist(70,74)",
    "female. M/40 chest(90,94) waist(74,78)",
    "female. M/42 chest(94,98) waist(78,82)",
    "male. M/46 chest(90,94) waist(78,82)",
    "male. M/48 chest(94,98) waist(82,86)",
    "male. L/50 chest(98,102) waist(86,90)"
]

empty_size_info = { "gender":"", "american_size":"", "european_size":"", "chest_min":"", "chest_max":"", "waist_min":"", "waist_max" :"" }


# PLAYER PROFILES

class PlayerModelTests(TestCase):

    def test_create_player_profile(self):
        """
        create_player_profile() creates a Player object asociated to a test User account.
        """
        player_info = example_players_complete[0]
        player = create_player(player_info)
        self.assertEqual(player.user.username, player_info["username"])
        self.assertEqual(str(player), player_info["first_name"] + " " + player_info["last_name"])
        self.assertEqual(player.gender, player_info["gender"])

    def test_create_player_profile_with_no_dietary_information(self):
        """
        create_player_profile_with_dietary_information() creates a Player object asociated to a test User account
        and adds medical and dietary information.
        """
        test_user = User(username="ana")
        diet = DietaryRestriction(name="None")
        test_player = Player(user=test_user, dietary_restrictions = diet)
        self.assertEqual(test_player.dietary_restrictions.name, "None")
        self.assertIs(test_player.dietary_restrictions, diet)
        self.assertIs(test_player.comments,"no")

    def test_create_player_profile_with_dietary_information(self):
        """
        create_player_profile_with_dietary_information() creates a Player object asociated to a test User account
        and adds medical and dietary information.
        """
        test_user = User(username="ana")
        diet = DietaryRestriction(name="Vegan")
        test_player = Player(user=test_user, dietary_restrictions = diet)
        self.assertEqual(test_player.dietary_restrictions.name, "Vegan")
        self.assertIs(test_player.dietary_restrictions, diet)

    def test_create_player_profile_with_alternative_dietary_information(self):
        """
        create_player_profile_with_dietary_information() creates a Player object asociated to a test User account
        and adds medical and dietary information.
        """
        test_user = User(username="ana")
        diet = DietaryRestriction(name="Other")
        test_player = Player(user=test_user, dietary_restrictions = diet)
        test_player.comments = "I'm a pescatarian"
        self.assertEqual(test_player.dietary_restrictions.name, "Other")
        self.assertIs(test_player.dietary_restrictions, diet)
        self.assertEqual(test_player.comments, "I'm a pescatarian")

    def test_create_player_profile_with_size_information(self):
        """
        create_player_profile_with_size_information() creates a Player object asociated to a test User account
        and adds information about the size of the player.
        """
        test_user = User(username="ana")
        test_player = Player(user=test_user, shoulder= 40, height = 160, chest = 90, waist = 90)
        self.assertIs(test_player.shoulder, 40)
        self.assertIs(test_player.height, 160)
        self.assertIs(test_player.chest, 90)
        self.assertIs(test_player.waist, 90)


# LARPS AND CHARACTERS

class GroupModelTests(TestCase):

    def test_create_group(self):
        """
        create_group creates a Group associated with a Larp.
        """
        group_name = example_groups[0]
        group = create_group(group_name)
        self.assertEqual(group.name, group_name)
        self.assertEqual(group.larp.name, larp_name())

    def test_create_empty_group(self):
        """
        create_empty_group creates agroup associated with a Larp.
        """
        empty_group = create_group("")
        self.assertEqual(empty_group.larp.name, larp_name())
        self.assertEqual(str(empty_group), larp_name()+" - no group")

    def test_create_characters_assigments(self):
        group = create_group(example_groups[1])
        create_characters_assigments(group=group, players=example_players_complete, characters=example_characters)
        for i in range(0,len(example_players_complete)):
            # Testing user creation
            player_info = example_players_complete[i]
            user_search = User.objects.filter(username=player_info["username"])
            self.assertEqual(len(user_search), 1)
            user = user_search[0]
            self.assertEqual(user.username, player_info["username"])
            # Testins player profile creation
            player_profiles = Player.objects.filter(user=user)
            self.assertEqual(len(player_profiles), 1)
            self.assertEqual(player_profiles[0].gender, player_info["gender"])
            # Testing character creation
            character_name = example_characters[i]
            character_search = Character.objects.filter(name=character_name)
            self.assertEqual(len(character_search), 1)
            character = character_search[0]
            self.assertEqual(character.name, character_name)
            self.assertEqual(character.group, group)
            # Testing character assigment
            assigments = CharacterAssigment.objects.filter(character=character, user=user)
            self.assertEqual(len(assigments), 1)


    def test_get_player_profiles_empty(self):
        """
        create_get_player_profiles_empty returns an empty array
        """
        group = create_group(example_groups[0])
        player_profiles = group.get_player_profiles()
        self.assertEqual(player_profiles, [])
        all_profiles = Player.objects.all()
        self.assertEqual(str(all_profiles), "<QuerySet []>" )

    def test_get_character_assigments(self):
        group = create_group(example_groups[0])
        create_characters_assigments(group, players=example_players_complete, characters=example_characters)
        #assigments = CharacterAssigment.objects.all()
        assigments_group = group.get_character_assigments()
        self.assertEqual(len(assigments_group), len(example_players_complete))
        for i in range(0,len(example_players_complete)):
            self.assertEqual(assigments_group[i].user.username, example_players_complete[i]["username"])
            self.assertEqual(assigments_group[i].character.name, example_characters[i])

    def test_get_player_profiles_users_with_no_profile(self):
        """
        create_get_player_profiles returns empty profiles associated with the users assigned to this group.
        """
        group = create_group(example_groups[1])
        create_characters_assigments(group=group, players=example_players_incomplete, characters=example_characters)
        player_profiles = group.get_player_profiles()
        self.assertEqual(str(player_profiles), "[<Player: Maria Gonzalez>, <Player: Andrea Hernandez>]")
        self.assertEqual(player_profiles[0].user.username, example_players_incomplete[0]["username"])
        self.assertEqual(player_profiles[0].chest, 0)
        self.assertEqual(player_profiles[0].waist, 0)
        self.assertEqual(player_profiles[1].user.username, example_players_incomplete[1]["username"])
        self.assertEqual(player_profiles[1].chest, 0)
        self.assertEqual(player_profiles[1].waist, 0)

    def test_get_player_profiles_with_correct_examples(self):
        """
        create_get_player_profiles returns the profiles of the players assigned to this group.
        """
        group = create_group(example_groups[2])
        create_characters_assigments(group, players=example_players_complete, characters=example_characters[2:4])
        player_profiles = group.get_player_profiles()
        self.assertEqual(str(player_profiles), "[<Player: Ana Garcia>, <Player: Pepa Perez>]")
        self.assertEqual(player_profiles[0].user.username, example_players_complete[0]["username"])
        self.assertEqual(player_profiles[0].chest, example_players_complete[0]["chest"])
        self.assertEqual(player_profiles[0].waist, example_players_complete[0]["waist"])
        self.assertEqual(player_profiles[1].user.username, example_players_complete[1]["username"])
        self.assertEqual(player_profiles[1].chest, example_players_complete[1]["chest"])
        self.assertEqual(player_profiles[1].waist, example_players_complete[1]["waist"])

    def test_get_player_profiles_player_in_2_runs(self):
        player_repeated = example_players_complete[1]
        uniform = create_uniform_with_player_in_several_runs(sizes=example_sizes, players_info=example_players_complete,
                                                            characters_names=example_characters, player_in_several_runs=player_repeated,
                                                            group_name=example_groups[0], runs=2)
        profiles = uniform.group.get_player_profiles()
        self.assertEqual(len(profiles), len(example_players_complete))


class CharacterModelTests(TestCase):

    def test_create_character(self):
        """
        create_character creates a character for a larp.
        """
        group = create_group(example_groups[1])
        character = Character(group = group, name=example_characters[0])
        self.assertEqual(character.name, example_characters[0])
        self.assertIs(character.group, group)
        self.assertEqual(character.group.name, example_groups[1])
        self.assertEqual(character.group.larp.name, larp_name())

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run.
        """
        user = User(username="ana", first_name="Ana", last_name="Garcia")
        group = create_group(example_groups[1])
        character = Character(group = group, name=example_characters[0])
        character_assigment = CharacterAssigment(run=1, character=character, user=user)
        self.assertIs(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.character.name, example_characters[0])
        self.assertIs(character_assigment.character.group.name, example_groups[1])
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie assigned to Ana Garcia")

    def test_create_character_assigment_without_user(self):
        """
        create_character_assigment assigns a character to a larp run but without an asigned user.
        This is useful when you have a new character that has no player assigned yet.
        """
        larp = Larp(name = larp_name())
        group = Group(larp=larp, name="Doctors")
        character = Character(group = group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=character)
        self.assertIs(character_assigment.character.group.larp, larp)
        self.assertEqual(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.character, character)
        self.assertEqual(character_assigment.character.name, example_characters[0])
        self.assertIs(character_assigment.character.group, group)
        self.assertEqual(character_assigment.character.group.name, example_groups[1])
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie")

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run for a character without a group.
        """
        user = User(username="ana", first_name="Ana", last_name="Garcia")
        larp = Larp(name = larp_name())
        empty_group = Group(name="", larp = larp)
        character = Character(group = empty_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=character, user=user)
        self.assertIs(character_assigment.character.name, "Marie Curie")
        self.assertIs(character_assigment.character.group.larp, larp)
        self.assertEqual(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie assigned to Ana Garcia")


# BOOKINGS

class BookingsModelTests(TestCase):

    def test_create_bookings(self):
        """
        create_bookings()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        self.assertIs(test_bookings.user.username, "ana")
        self.assertEqual(str(test_bookings), "Blue Flame run 1 - Ana Garcia")

    def test_bookings_weapon(self):
        """
        bookings_weapon()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        test_bookings.weapon = True
        self.assertIs(test_bookings.weapon, True)

    def test_bookings_bus(self):
        """
        bookings_bus()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        bus_option1 = BusStop(name="Madrid_1")
        test_bookings.bus = bus_option1
        self.assertIs(test_bookings.bus.name, "Madrid_1")

    def test_bookings_accomodations(self):
        """
        bookings_accomodations()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        accomodation1 = Accomodation(name="In game")
        test_bookings.accomodation = accomodation1
        test_bookings.sleeping_bag = False
        self.assertIs(test_bookings.accomodation.name, "In game")
        self.assertIs(test_bookings.sleeping_bag, False)

    def test_bookings_comments(self):
        """
        bookings_comments()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        test_bookings.comments = "Hi"
        self.assertIs(test_bookings.comments,"Hi")

    def test_bookings_no_comments(self):
        """
        bookings_no_comments()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_bookings = Bookings(user=test_user, larp=test_larp, run=1)
        self.assertIs(test_bookings.comments,"no")


# UNIFORMS

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
        self.assertEqual(str(size), "chest(0,0) waist(0,0)")

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
        uniform = create_uniform_with_players_and_sizes(sizes=example_sizes, players_info=example_players_complete, characters_names=example_characters, group_name="Pilots")
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
        uniform = create_uniform_with_players_and_sizes(sizes=example_sizes, players_info=example_players_complete, characters_names=example_characters, group_name="Mechanics")
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


class DietaryRestrictionModelTests(TestCase):
    diets = [ "", "Vegetarian", "Vegan" ]

    def test_create_dietary_restrictions(self):
        create_diets(self.diets)
        all_diets= DietaryRestriction.objects.all()
        self.assertIs(len(all_diets),3)

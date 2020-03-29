from django.test import TestCase
from django.contrib.auth.models import User

from larps.models import *
from larps.config import larp_name
from .util_test_models import *

example_characters = [ "Marie Curie", "Ada Lovelace" ]
example_groups = [ "Scientists", "Doctors", "Mecanics" ]
example_players = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75 },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78 }
]

# PLAYER PROFILES

class PlayerModelTests(TestCase):

    def test_create_player_profile(self):
        """
        create_player_profile() creates a Player object asociated to a test User account.
        """
        player_info = example_players[0]
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
        group_name = example_groups[1]
        group = create_group(group_name)
        self.assertEqual(group.name, group_name)
        self.assertEqual(group.larp.name, larp_name())

    def test_create_empty_group(self):
        """
        create_empty_group creates agroup associated with a Larp.
        """
        larp = Larp(name = larp_name())
        empty_group = Group(larp=larp, name="")
        self.assertEqual(empty_group.larp.name, larp_name())
        self.assertIs(empty_group.larp, larp)
        self.assertEqual(str(empty_group), larp_name()+" - no group")

    def test_get_player_profiles_empty(self):
        """
        create_get_player_profiles returns the profiles of the players assigned to this group.
        """
        group = create_group(group_name=example_groups[1])
        player_profiles = group.get_player_profiles()
        self.assertEqual(player_profiles, [])

    def test_get_player_profiles_with_correct_examples(self):
        """
        create_get_player_profiles returns the profiles of the players assigned to this group.
        """
        group = create_group(example_groups[1])
        create_characters_assigments(group, example_players, example_characters)
        player_profiles = group.get_player_profiles()
        self.assertEqual(player_profiles[0].user.username, example_players[0]["username"])
        self.assertEqual(player_profiles[0].chest, example_players[0]["chest"])
        self.assertEqual(player_profiles[0].waist, example_players[0]["waist"])
        self.assertEqual(player_profiles[1].user.username, example_players[1]["username"])
        self.assertEqual(player_profiles[1].chest, example_players[1]["chest"])
        self.assertEqual(player_profiles[1].waist, example_players[1]["waist"])



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
    example_sizes = [
             {  "gender":"female", "american_size":"S", "european_size":"38", "chest_min":"86", "chest_max":"90", "waist_min":"70", "waist_max":"74" },
             {  "gender":"female", "american_size":"M", "european_size":"40", "chest_min":"90", "chest_max":"94", "waist_min":"74", "waist_max":"78" },
             {  "gender":"female", "american_size":"M", "european_size":"42", "chest_min":"94", "chest_max":"98", "waist_min":"78", "waist_max":"82" },
             {  "gender":"male", "american_size":"M", "european_size":"46", "chest_min":"90", "chest_max":"94", "waist_min":"78", "waist_max":"82" },
             {  "gender":"male", "american_size":"M", "european_size":"48", "chest_min":"94", "chest_max":"98", "waist_min":"82", "waist_max":"86" },
             {  "gender":"male", "american_size":"L", "european_size":"50", "chest_min":"98", "chest_max":"102", "waist_min":"86", "waist_max":"90" },
         ]

    empty_size_info = { "gender":"", "american_size":"", "european_size":"", "chest_min":"", "chest_max":"", "waist_min":"", "waist_max" :"" }
    group_name = "Pilots"

    def test_create_uniform(self):
        uniform = create_uniform(group_name=self.group_name)
        self.assertEqual(uniform.group.name, self.group_name)
        self.assertEqual(uniform.name, self.group_name)

    def test_create_uniform_with_full_info(self):
        uniform = create_uniform(group_name=self.group_name)
        color = "Red"
        uniform.color = color
        self.assertEqual(uniform.group.name, self.group_name)
        self.assertEqual(uniform.name, self.group_name)

    def test_create_uniform_size_with_no_info(self):
        uniform = create_uniform(group_name=self.group_name)
        size = UniformSize(uniform=uniform)
        self.assertEqual(size.uniform.name, self.group_name)

    def test_create_uniform_size_with_info(self):
        size_information = self.example_sizes[0]
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
        size_information = self.empty_size_info
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
        player_info = example_players[0]
        player = create_player(player_info=player_info)
        uniform = create_uniform_with_sizes(self.example_sizes)
        sizes = uniform.recommend_sizes(player)
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].gender,"female")
        self.assertEqual(sizes[0].american_size,"M")
        self.assertEqual(sizes[0].european_size,"40")
        self.assertEqual(str(sizes[0]), "female. M/40 chest(90,94) waist(74,78)")

    def test_recommend_sizes_valid_fit(self):
        uniform = create_uniform_with_sizes(self.example_sizes)
        player_info = example_players[0]
        player = create_player(player_info=player_info)
        sizes = uniform.recommend_sizes(player=player)
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].american_size,"M")
        self.assertEqual(sizes[0].european_size,"40")
        self.assertEqual(str(sizes[0]), "female. M/40 chest(90,94) waist(74,78)")

    def test_perfect_fit_true(self):
        chest = 90
        waist = 75
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.perfect_fit(chest, waist), True)

    def test_perfect_fit_false(self):
        chest = 90
        waist = 75
        size = create_uniform_size(self.example_sizes[0])
        self.assertIs(size.perfect_fit(chest, waist), False)

    def test_waist_fit_true(self):
        waist = 75
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.waist_fit(waist), True)

    def test_waist_fit_false(self):
        waist = 75
        size = create_uniform_size(self.example_sizes[0])
        self.assertIs(size.waist_fit(waist), False)

    def test_chest_fit_true(self):
        chest = 90
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.chest_fit(chest), True)

    def test_chest_fit_false(self):
        chest = 89
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.chest_fit(chest), False)

    def test_chest_minimum_fit_true(self):
        chest = 89
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.chest_minimum_fit(chest), True)

    def test_chest_minimum_fit_size_too_small(self):
        chest = 91
        size = create_uniform_size(self.example_sizes[0])
        self.assertIs(size.chest_minimum_fit(chest), False)

    def test_waist_minimum_fit_true(self):
        waist = 74
        size = create_uniform_size(self.example_sizes[1])
        self.assertIs(size.waist_minimum_fit(waist), True)

    def test_waist_minimum_fit_size_too_small(self):
        waist = 80
        size = create_uniform_size(self.example_sizes[0])
        self.assertIs(size.waist_minimum_fit(waist), False)

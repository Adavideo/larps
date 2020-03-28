from django.test import TestCase
from django.contrib.auth.models import User

from .models import *


# PLAYER PROFILES

class PlayerModelTests(TestCase):

    def test_create_player_profile(self):
        """
        create_player_profile() creates a Player object asociated to a test User account.
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_player = Player(user=test_user)
        self.assertEqual(test_player.user.username, "ana")
        self.assertEqual(str(test_player), "Ana Garcia")

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
        test_larp = Larp(name = "Blue Flame")
        test_group = Group(larp=test_larp, name="Doctors")
        self.assertEqual(test_group.name, "Doctors")
        self.assertEqual(test_group.larp.name, "Blue Flame")
        self.assertIs(test_group.larp, test_larp)

    def test_create_empty_group(self):
        """
        create_empty_group creates agroup associated with a Larp.
        """
        test_larp = Larp(name = "Blue Flame")
        empty_group = Group(larp=test_larp, name="")
        self.assertEqual(empty_group.larp.name, "Blue Flame")
        self.assertIs(empty_group.larp, test_larp)
        self.assertEqual(str(empty_group), "Blue Flame - no group")


class CharacterModelTests(TestCase):

    def test_create_character(self):
        """
        create_character creates a character for a larp.
        """
        test_larp = Larp(name = "Blue Flame")
        test_group = Group(larp=test_larp, name="Doctors")
        test_character = Character(group = test_group, name="Marie Curie")
        self.assertEqual(test_character.name, "Marie Curie")
        self.assertIs(test_character.group, test_group)
        self.assertEqual(test_character.group.name, "Doctors")
        self.assertIs(test_character.group.larp, test_larp)
        self.assertEqual(test_character.group.larp.name, "Blue Flame")

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run.
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_group = Group(larp=test_larp, name="Doctors")
        test_character = Character(group = test_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=test_character, user=test_user)
        self.assertIs(character_assigment.character.group.larp.name, "Blue Flame")
        self.assertIs(character_assigment.character.name, "Marie Curie")
        self.assertIs(character_assigment.character.group.name, "Doctors")
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), "Blue Flame run 1 - Marie Curie assigned to Ana Garcia")

    def test_create_character_assigment_without_user(self):
        """
        create_character_assigment assigns a character to a larp run but without an asigned user.
        This is useful when you have a new character that has no player assigned yet.
        """
        test_larp = Larp(name = "Blue Flame")
        test_group = Group(larp=test_larp, name="Doctors")
        test_character = Character(group = test_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=test_character)
        self.assertIs(character_assigment.character.group.larp, test_larp)
        self.assertEqual(character_assigment.character.group.larp.name, "Blue Flame")
        self.assertIs(character_assigment.character, test_character)
        self.assertEqual(character_assigment.character.name, "Marie Curie")
        self.assertIs(character_assigment.character.group, test_group)
        self.assertEqual(character_assigment.character.group.name, "Doctors")
        self.assertEqual(str(character_assigment), "Blue Flame run 1 - Marie Curie")

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run for a character without a group.
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        empty_group = Group(name="", larp = test_larp)
        test_character = Character(group = empty_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=test_character, user=test_user)
        self.assertIs(character_assigment.character.name, "Marie Curie")
        self.assertIs(character_assigment.character.group.larp, test_larp)
        self.assertEqual(character_assigment.character.group.larp.name, "Blue Flame")
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), "Blue Flame run 1 - Marie Curie assigned to Ana Garcia")


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
             {  "gender":"female", "american_size":"M", "european_size":"42", "chest_min":"94", "chest_max":"94", "waist_min":"78", "waist_max":"82" },
         ]
    empty_size_info = { "gender":"", "american_size":"", "european_size":"", "chest_min":"", "chest_max":"", "waist_min":"", "waist_max" :"" }
    group_name = "Pilots"

    def create_uniform(self):
        larp = Larp(name="larp name")
        larp.save()
        group = Group(name=self.group_name, larp=larp)
        group.save()
        uniform = Uniform(group=group, name=self.group_name)
        uniform.save()
        return uniform

    def create_uniform_size(self, size_information):
        uniform = self.create_uniform()
        size = UniformSize(uniform=uniform)
        size.set_values(size_information)
        size.save()
        return size

    def create_uniform_with_sizes(self):
        uniform = self.create_uniform()
        for size_information in self.example_sizes:
            size = UniformSize(uniform=uniform)
            size.set_values(size_information)
            size.save()
        return uniform


    def test_create_uniform(self):
        uniform = self.create_uniform()
        self.assertEqual(uniform.group.name, self.group_name)
        self.assertEqual(uniform.name, self.group_name)

    def test_create_uniform_with_full_info(self):
        uniform = self.create_uniform()
        color = "Red"
        uniform.color = color
        self.assertEqual(uniform.group.name, self.group_name)
        self.assertEqual(uniform.name, self.group_name)

    def test_create_uniform_size_with_no_info(self):
        uniform = self.create_uniform()
        size = UniformSize(uniform=uniform)
        self.assertEqual(size.uniform.name, self.group_name)

    def test_create_uniform_size_with_info(self):
        size_information = self.example_sizes[0]
        size = self.create_uniform_size(size_information)
        self.assertEqual(size.uniform.name, self.group_name)
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
        size = self.create_uniform_size(size_information)
        self.assertEqual(size.gender, size_information["gender"])
        self.assertEqual(size.american_size, size_information["american_size"])
        self.assertEqual(size.european_size, size_information["european_size"])
        self.assertEqual(size.chest_min, 0)
        self.assertEqual(size.chest_max, 0)
        self.assertEqual(size.waist_min, 0)
        self.assertEqual(size.waist_max, 0)
        #self.assertEqual(str(size), "")

    def test_recommend_sizes(self):
        chest = 90
        waist = 75
        uniform = self.create_uniform_with_sizes()
        sizes = uniform.recommend_sizes(chest, waist)
        self.assertEqual(sizes[0].american_size,"M")

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Player, Larp, Group, Character, CharacterAssigment, Bookings, DietaryRestriction


class PlayerModelTests(TestCase):


    # PLAYER PROFILES

    def test_create_player_profile(self):
        """
        create_player_profile() creates a Player object asociated to a test User account.
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_player = Player(user=test_user)
        self.assertEqual(test_player.user.username, "ana")
        self.assertEqual(str(test_player), "Ana Garcia")

    def test_create_player_profile_with_dietary_information(self):
        """
        create_player_profile_with_dietary_information() creates a Player object asociated to a test User account
        and adds medical and dietary information.
        """
        test_user = User(username="ana")
        diet = DietaryRestriction(name="none")
        test_player = Player(user=test_user, dietary_restrictions = diet)
        self.assertEqual(test_player.dietary_restrictions.name, "none")
        self.assertIs(test_player.dietary_restrictions, diet)

    def test_create_player_profile_with_size_information(self):
        """
        create_player_profile_with_size_information() creates a Player object asociated to a test User account
        and adds information about the size of the player.
        """
        test_user = User(username="ana")
        test_player = Player(user=test_user, height = 160, chest = 90, waist = 90)
        self.assertIs(test_player.height, 160)
        self.assertIs(test_player.chest, 90)
        self.assertIs(test_player.waist, 90)


    # LARPS AND CHARACTERS

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

    def test_create_bookings(self):
        """
        create_bookings()
        """
        test_user = User(username="ana", first_name="Ana", last_name="Garcia")
        test_larp = Larp(name = "Blue Flame")
        test_group = Group(larp=test_larp, name="Doctors")
        test_character = Character(group = test_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=test_character, user=test_user)
        test_bookings = Bookings(character_assigment=character_assigment)
        self.assertIs(test_bookings.character_assigment.character.name, "Marie Curie")
        self.assertIs(test_bookings.character_assigment.user.username, "ana")
        self.assertIs(test_bookings.character_assigment.character.group.name, "Doctors")
        self.assertEqual(str(test_bookings), "Blue Flame run 1 - Marie Curie assigned to Ana Garcia")

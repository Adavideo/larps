from django.test import TestCase
from django.contrib.auth.models import User
from .models import Player, Larp, Group, Character, CharacterAssigment, Bookings, DietaryRestriction, BusStop, Accomodation
from .csv_importer import *


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


# CSV IMPORT

class CSVTests(TestCase):

    # Tests for create users

    def test_create_user_correct(self):
        player_name = "Ana Perez"
        new_user = create_user(player_name)
        self.assertEqual(new_user.username, "Ana_Perez")
        self.assertEqual(new_user.first_name, "Ana")
        self.assertEqual(new_user.last_name, "Perez")

    def test_create_user_one_name(self):
        player_name = "Ana"
        new_user = create_user(player_name)
        self.assertEqual(new_user.username, "Ana")
        self.assertEqual(new_user.first_name, "Ana")
        self.assertEqual(new_user.last_name, "")

    def test_create_user_empty(self):
        player_name = ""
        new_user = create_user(player_name)
        self.assertEqual(new_user, None)

    def test_create_user_blank_space(self):
        player_name = " "
        new_user = create_user(player_name)
        self.assertEqual(new_user, None)

    # Tests for create characters

    def test_create_character_complete_information(self):
        larp_name = "Blue Flame"
        character_name = "Athena"
        group = "Scientists"
        race = "Terrans"
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, "Blue Flame")

    def test_create_character_no_race(self):
        larp_name = "Blue Flame"
        character_name = "Athena"
        group = "Scientists"
        race = ""
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.race.name, "")

    def test_create_character_no_group(self):
        larp_name = "Blue Flame"
        character_name = "Athena"
        group = ""
        race = "Terrans"
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group.name, "")
        self.assertEqual(new_character.group.larp.name, "Blue Flame")

    def test_create_character_no_information(self):
        larp_name = "Blue Flame"
        character_name = ""
        group = ""
        race = ""
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character, None)

    def test_create_character_only_group_information(self):
        larp_name = "Blue Flame"
        character_name = ""
        group = "Scientists"
        race = ""
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, "Blue Flame")

    def test_create_character_only_race_information(self):
        larp_name = "Blue Flame"
        character_name = ""
        group = ""
        race = "Terrans"
        new_character = create_character(larp_name, character_name, group, race)
        self.assertEqual(new_character.race.name, "Terrans")
        self.assertEqual(new_character.group.name, "")
        self.assertEqual(new_character.group.larp.name, "Blue Flame")


    # Test for processing lines

    def test_process_csv_line_correct(self):
        column = ['1', 'Werner Mikolasch', 'Ono', 'agriculture teacher', 'Rhea', 'lieutenant']
        result = process_csv_line(column)
        self.assertEqual(result, 'Character Ono assigned to Werner Mikolasch')

    def test_process_csv_line_no_user(self):
        column = ['1', '', 'Fuertes', 'artist teacher', 'Kepler', 'lieutenant']
        result = process_csv_line(column)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_user_blank_space(self):
        column = ['1', ' ', 'Fuertes', 'artist teacher', 'Kepler', 'lieutenant']
        result = process_csv_line(column)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_correct_user_but_no_character(self):
        column = ['2', 'Samuel Bascomb', '', '', '', '']
        result = process_csv_line(column)
        self.assertEqual(result, 'Created user Samuel Bascomb. Character invalid')

    def test_process_csv_line_no_user_and_no_character(self):
        column = ['2', '', '', '', '', '']
        result = process_csv_line(column)
        self.assertEqual(result, 'User invalid. Character invalid')


    # Test for processing datasets

    def test_process_data_without_errors(self):
        """
        process_data() checks that the data from the csv file is processed correctly
        """
        data = """run,player,character,group,planet,rank
1,Werner Mikolasch,Ono,agriculture teacher,Rhea,lieutenant
2,Fabio,Fuertes,artist teacher,Kepler,lieutenant"""
        result = process_data(data)
        self.assertEqual(result, ['Character Ono assigned to Werner Mikolasch', 'Character Fuertes assigned to Fabio '])


    def test_process_data_with_invalid_users(self):
        """
        process_data_with_invalid_users() checks that no users are created when the player name is empty or a blank space
        """
        data = """run,player,character,group,planet,rank
    1,,Fuertes,artist teacher,Kepler,lieutenant
    2, ,Ono,agriculture teacher,Rhea,lieutenant"""
        result = process_data(data)
        self.assertEqual(result, ['User invalid', 'User invalid'])


    def test_process_data_with_wrong_character(self):
        data = """run,player,character,group,planet,rank
2,Samuel Bascomb,,,,"""
        result = process_data(data)
        self.assertEqual(result, ['Created user Samuel Bascomb. Character invalid'])

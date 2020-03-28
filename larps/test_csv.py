from django.test import TestCase
from django.contrib.auth.models import User

from .models import *
from .csv_importer import create_user, create_character, assign_character_to_user, process_csv_line, process_data
from .config import larp_name, csv_file_types


# CSV IMPORT

class CSVCharactersTests(TestCase):
    csv_type = csv_file_types()[0][0]
    larp_name = larp_name()

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
        character_name = "Athena"
        group = "Scientists"
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, self.larp_name)

    def test_create_character_no_race(self):
        character_name = "Athena"
        group = "Scientists"
        race = ""
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.race.name, "")

    def test_create_character_no_group(self):
        character_name = "Athena"
        group = ""
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group.name, "")
        self.assertEqual(new_character.group.larp.name, self.larp_name)

    def test_create_character_no_information(self):
        character_name = ""
        group = ""
        race = ""
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character, None)

    def test_create_character_only_group_information(self):
        character_name = ""
        group = "Scientists"
        race = ""
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, self.larp_name)

    def test_create_character_only_race_information(self):
        character_name = ""
        group = ""
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race)
        self.assertEqual(new_character.race.name, "Terrans")
        self.assertEqual(new_character.group.name, "")
        self.assertEqual(new_character.group.larp.name, self.larp_name)


    # Test assign characters to users

    def test_assign_character_to_user(self):
        run = 2
        user = User(username="Ana", first_name="Ana")
        user.save()
        character = Character(name="Ono")
        character.save()
        result = assign_character_to_user(user, character, run)
        self.assertEqual(result, "Character Ono assigned to Ana ")


    # Test for processing lines

    def test_process_csv_line_correct(self):
        column = ['1', 'Werner Mikolasch', 'Ono', 'agriculture teacher', 'Rhea', 'lieutenant']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'Character Ono assigned to Werner Mikolasch')

    def test_process_csv_line_no_user(self):
        column = ['1', '', 'Fuertes', 'artist teacher', 'Kepler', 'lieutenant']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_user_blank_space(self):
        column = ['1', ' ', 'Fuertes', 'artist teacher', 'Kepler', 'lieutenant']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_correct_user_but_no_character(self):
        column = ['2', 'Samuel Bascomb', '', '', '', '']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'Created user Samuel Bascomb. Character invalid')

    def test_process_csv_line_no_user_and_no_character(self):
        column = ['2', '', '', '', '', '']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid. Character invalid')


    # Test for processing datasets

    def test_process_data_without_errors(self):
        """
        process_data() checks that the data from the csv file is processed correctly
        """
        data = """run,player,character,group,planet,rank
1,Werner Mikolasch,Ono,agriculture teacher,Rhea,lieutenant
2,Fabio,Fuertes,artist teacher,Kepler,lieutenant"""
        result = process_data(data, self.csv_type)
        self.assertEqual(result, ['Character Ono assigned to Werner Mikolasch', 'Character Fuertes assigned to Fabio '])


    def test_process_data_with_invalid_users(self):
        """
        process_data_with_invalid_users() checks that no users are created when the player name is empty or a blank space
        """
        data = """run,player,character,group,planet,rank
    1,,Fuertes,artist teacher,Kepler,lieutenant
    2, ,Ono,agriculture teacher,Rhea,lieutenant"""
        result = process_data(data, self.csv_type)
        self.assertEqual(result, ['User invalid', 'User invalid'])


    def test_process_data_with_wrong_character(self):
        data = """run,player,character,group,planet,rank
2,Samuel Bascomb,,,,"""
        result = process_data(data, self.csv_type)
        self.assertEqual(result, ['Created user Samuel Bascomb. Character invalid'])

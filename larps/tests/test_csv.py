from django.test import TestCase
from django.contrib.auth.models import User
from config import csv_file_types, uniforms_header, characters_header
from larps.models import Character
from larps.csv_importer import *
from .examples import *


# CSV IMPORT CHARACTERS

class CSVCharactersTests(TestCase):
    csv_type = csv_file_types()[0][0]
    larp_name = "Mission Together"

    # Tests for create users

    def test_create_user_correct(self):
        player_name = "Ana Perez"
        new_user = create_user(player_name, example_email)
        self.assertEqual(new_user.username, "Ana_Perez")
        self.assertEqual(new_user.first_name, "Ana")
        self.assertEqual(new_user.last_name, "Perez")

    def test_create_user_one_name(self):
        player_name = "Ana"
        new_user = create_user(player_name, example_email)
        self.assertEqual(new_user.username, "Ana")
        self.assertEqual(new_user.first_name, "Ana")
        self.assertEqual(new_user.last_name, "")

    def test_create_user_empty(self):
        player_name = ""
        new_user = create_user(player_name, example_email)
        self.assertEqual(new_user, None)

    def test_create_user_blank_space(self):
        player_name = " "
        new_user = create_user(player_name, example_email)
        self.assertEqual(new_user, None)

    # Tests for create characters

    def test_create_character_complete_information(self):
        character_name = "Athena"
        group = "Scientists"
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race,
            example_character['rank'], example_character['type'], example_character['concept'],
            example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, self.larp_name)

    def test_create_character_no_race(self):
        character_name = "Athena"
        group = "Scientists"
        race = ""
        # larp_name, character_name, group, race, rank, type, concept, sheet, weapon
        new_character = create_character(self.larp_name, character_name, group, race,
            example_character['rank'], example_character['type'], example_character['concept'],
            example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.race.name, "")

    def test_create_character_no_group(self):
        character_name = "Athena"
        group = ""
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race,
            example_character['rank'], example_character['type'], example_character['concept'],
            example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character.name, "Athena")
        self.assertEqual(new_character.group, None)

    def test_create_character_no_information(self):
        character_name = ""
        group = ""
        race = ""
        new_character = create_character(self.larp_name, character_name, group, race,
            example_character['rank'], example_character['type'], example_character['concept'],
            example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character, None)

    def test_create_character_only_group_information(self):
        character_name = ""
        group = "Scientists"
        race = ""
        new_character = create_character(self.larp_name, character_name, group, race,
        example_character['rank'], example_character['type'], example_character['concept'],
        example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character.group.name, "Scientists")
        self.assertEqual(new_character.group.larp.name, self.larp_name)

    def test_create_character_only_race_information(self):
        character_name = ""
        group = ""
        race = "Terrans"
        new_character = create_character(self.larp_name, character_name, group, race,
        example_character['rank'], example_character['type'], example_character['concept'],
        example_character['sheet'], example_character['weapon'])
        self.assertEqual(new_character.race.name, "Terrans")
        self.assertEqual(new_character.group, None)


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
        column = ['Mission Together', '1', 'test1@email.com', 'Werner Mikolasch', 'Ono',
             example_character['group'], example_character['race'], example_character['rank'],
             example_character['type'], example_character['concept'], example_character['sheet'],
             example_character['weapon']]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'Character Ono assigned to Werner Mikolasch')
        character = Character.objects.all()[0]
        self.assertEqual(character.race.name, example_character['race'])
        self.assertEqual(character.rank, example_character['rank'])
        self.assertEqual(character.type.name, example_character['type'])
        self.assertEqual(character.concept, example_character['concept'])
        self.assertEqual(character.sheet, example_character['sheet'])
        self.assertEqual(character.weapon, example_character['weapon'])

    def test_process_csv_line_no_user(self):
        column = ['Mission Together', '1', 'test1@email.com', '', 'Fuertes',
            example_character['group'], example_character['race'], example_character['rank'],
            example_character['type'], example_character['concept'], example_character['sheet'],
            example_character['weapon']]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_user_blank_space(self):
        column = ['Mission Together', '1', 'test1@email.com', '', 'Fuertes',
            example_character['group'], example_character['race'], example_character['rank'],
            example_character['type'], example_character['concept'], example_character['sheet'],
            example_character['weapon']]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid')

    def test_process_csv_line_correct_user_but_no_character(self):
        column = ['Mission Together', '2', 'test1@email.com', 'Samuel Bascomb', '','','', '','','','','']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'Created user Samuel Bascomb. Character invalid')

    def test_process_csv_line_no_user_and_no_character(self):
        column = ['Mission Together', '2', 'test1@email.com','', '','','', '','','','','']
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, 'User invalid. Character invalid')


    # Test for processing datasets

    def test_process_data_without_errors(self):
        """
        process_data() checks that the data from the csv file is processed correctly
        """
        result = process_data(characters_csv_example)
        self.assertEqual(result, ['Character Ono assigned to Werner Mikolasch', 'Character Fuertes assigned to Fabio '])


    def test_process_data_with_invalid_users(self):
        """
        process_data_with_invalid_users() checks that no users are created when the player name is empty or a blank space
        """
        data = """larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon
        Mission Together;1;;;Fuertes;artist teacher;Kepler;lieutenant;player;https://docs.google.com/document/d/1sICrVe/edit?usp=sharing;this is a test;
        Mission Together;2;;;Ono;agriculture teacher;Rhea;lieutenant;secret NPC;https://docs.google.com/document/d/ynZA/edit?usp=sharing;this is a test;Your character owns a weapon, we will provide it"""

        result = process_data(data)
        self.assertEqual(result, ['User invalid', 'User invalid'])


    def test_process_data_with_wrong_character(self):
        data = """larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon
        Mission Together;2;;Samuel Bascomb;;;;;;;;"""
        result = process_data(data)
        self.assertEqual(result, ['Created user Samuel Bascomb. Character invalid'])



# CSV IMPORT UNIFORMS

class CSVUniformsTests(TestCase):
    csv_type = csv_file_types()[1][0]

    def test_process_csv_line_correct(self):
        column = correct_size_examples[3]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, "Pilots - group not assigned - female. L/44 chest(98,102) waist(82,86)")

    def test_process_csv_line_not_esential_info_missing(self):
        column = incorrect_size_examples[0]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, "Pilots - group not assigned - female. L/44 chest(98,102) waist(82,86)")

    def test_process_csv_line_no_group(self):
        column = incorrect_size_examples[1]
        result = process_csv_line(column, self.csv_type)
        expected_result = " - group not assigned - female. L/44 chest(98,102) waist(82,86)"
        self.assertEqual(result, expected_result)

    def test_process_csv_line_group_blank_space(self):
        column = incorrect_size_examples[2]
        result = process_csv_line(column, self.csv_type)
        self.assertEqual(result, " - group not assigned - female. L/44 chest(98,102) waist(82,86)")


class CSVFileTypesTests(TestCase):
    character_file_type = csv_file_types()[0][0]
    uniform_file_type = csv_file_types()[1][0]

    def test_incorrect_header(self):
        header = ""
        result = get_file_type(header)
        self.assertEqual(result, "incorrect")

    def test_correct_header_characters(self):
        result = get_file_type(characters_header)
        self.assertEqual(result, self.character_file_type)

    def test_correct_header_uniforms(self):
        result = get_file_type(uniforms_header)
        self.assertEqual(result, self.uniform_file_type)

    def test_correct_data_set_characters(self):
        result = process_data(characters_csv_example)
        self.assertEqual(result, ["Character Ono assigned to Werner Mikolasch",
                                "Character Fuertes assigned to Fabio "])

    def test_correct_uniforms(self):
        result = process_data(uniforms_csv_example)
        self.assertEqual(result, ["Pilots - group not assigned - female. S/38 chest(86,90) waist(70,74)",
                                "Pilots - group not assigned - female. M/40 chest(90,94) waist(74,78)"])

    def test_incorrect_data_set(self):
        result = process_data(incorrect_csv)
        self.assertEqual(result, ["Incorrect file type"])

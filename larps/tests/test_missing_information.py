from django.test import TestCase
from larps.models import Larp, Player, Bookings
from .util_test import create_group, create_characters_assigments, create_character_assigment, create_diets, set_bookings

example_characters = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker", "Peter Parker", "Leopold Fitz" ]
example_groups = [ "Scientists", "Doctors", "Mecanics" ]

example_players_complete = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75, "diet":"none" },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78, "diet":"none" },
    { "username": "Manolo_Garcia", "first_name": "Manolo", "last_name": "Garcia", "gender":"male", "chest":100, "waist":90, "diet":"Vegetarian" },
    { "username": "Paco_Garcia", "first_name": "Paco", "last_name": "Garcia", "gender":"male", "chest":102, "waist":86, "diet":"none" },
]
example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"" },
]
example_diets = [ "Vegetarian", "Vegan", "none" ]

example_bookings = [
    { "weapon": False, "bus": None, "accomodation": None, "sleeping_bag": False },
    { "weapon": False, "bus": "Madrid", "accomodation": "on site", "sleeping_bag": True },
]


class MissingInformationTests(TestCase):


    def test_get_missing_information_empty(self):
        # Initialize
        larp = Larp(name="")
        # Get information
        missing_info = larp.get_missing_information()
        # Validate
        self.assertIs(len(missing_info), 0)


    def test_get_missing_information_empty_one_run(self):
        # Initialize
        group = create_group()
        larp = group.larp
        create_diets(example_diets)
        player_info = example_players_incomplete[0]
        assigment = create_character_assigment(group, player_info, example_characters[0], run=1)
        # Get information
        missing_info = larp.get_missing_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        self.assertIs(len(missing_info[0]), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"].username, player_info["username"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["profile"].gender, "")
        self.assertEqual(missing_player_info["profile"].allergies, "")
        self.assertEqual(missing_player_info["profile"].dietary_restrictions, None)
        self.assertEqual(missing_player_info["bookings"].weapon, None)
        self.assertEqual(missing_player_info["bookings"].bus, None)
        self.assertEqual(missing_player_info["bookings"].accomodation, None)
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, None)
        self.assertEqual(missing_player_info["run"], 1)

    def test_get_missing_information_with_profile_info(self):
        # Initialize
        group = create_group(example_groups[0])
        larp = group.larp
        create_diets(example_diets)
        players_info = example_players_complete
        create_characters_assigments(group, players=players_info, characters=example_characters)
        # Get information
        missing_info = larp.get_missing_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        players_run1 = missing_info[0]
        self.assertEqual(len(players_run1), len(players_info))
        count = 0
        for missing_player_info in players_run1:
            self.assertEqual(missing_player_info["user"].username, players_info[count]["username"])
            self.assertEqual(missing_player_info["profile"].user.username, players_info[count]["username"])
            self.assertEqual(missing_player_info["profile"].gender, players_info[count]["gender"])
            self.assertEqual(missing_player_info["profile"].allergies, "")
            self.assertEqual(missing_player_info["profile"].dietary_restrictions.name, players_info[count]["diet"] )
            self.assertEqual(missing_player_info["bookings"].weapon, None)
            self.assertEqual(missing_player_info["bookings"].bus, None)
            self.assertEqual(missing_player_info["bookings"].accomodation, None)
            self.assertEqual(missing_player_info["bookings"].sleeping_bag, None)
            self.assertEqual(missing_player_info["run"], 1)
            count += 1

    def test_get_missing_information_with_some_booking_info(self):
        # Initialize
        group = create_group(example_groups[0])
        larp = group.larp
        player_info = example_players_complete[0]
        bookings_info = example_bookings[0]
        assigment = create_character_assigment(group, player_info, example_characters[0])
        set_bookings(assigment, bookings_info)
        # Get information
        missing_info = larp.get_missing_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"].username, player_info["username"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["bookings"].weapon, False)
        self.assertEqual(missing_player_info["bookings"].bus, None)
        self.assertEqual(missing_player_info["bookings"].accomodation, None)
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, False)
        

    def test_get_missing_information_with_all_booking_info(self):
        # Initialize
        group = create_group(example_groups[0])
        larp = group.larp
        player_info = example_players_complete[0]
        bookings_info = example_bookings[1]
        assigment = create_character_assigment(group, player_info, example_characters[0])
        set_bookings(assigment, bookings_info)
        # Get information
        missing_info = larp.get_missing_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"].username, player_info["username"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["bookings"].weapon, False)
        self.assertEqual(missing_player_info["bookings"].bus.name, bookings_info["bus"])
        self.assertEqual(missing_player_info["bookings"].accomodation.name, bookings_info["accomodation"])
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, True)

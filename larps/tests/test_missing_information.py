from django.test import TestCase
from larps.models import Larp, Bookings
from .util_test import create_group, create_characters_assigments, create_character_assigment, set_bookings
from .examples import example_players_complete, example_players_incomplete, example_bookings


class MissingInformationTests(TestCase):


    def test_get_players_information_empty(self):
        # Initialize
        larp = Larp(name="")
        # Get information
        missing_info = larp.get_players_information()
        # Validate
        self.assertIs(len(missing_info), 0)


    def test_get_players_information_empty_one_run(self):
        # Initialize
        group = create_group()
        larp = group.larp
        player_info = example_players_incomplete[0]
        assigment = create_character_assigment(group, player_info, run=1)
        # Get information
        missing_info = larp.get_players_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        self.assertIs(len(missing_info[0]), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"], player_info["first_name"]+" "+player_info["last_name"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["profile"].gender, "")
        self.assertEqual(missing_player_info["bookings"].bus, None)
        self.assertEqual(missing_player_info["bookings"].accomodation, None)
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, None)
        self.assertEqual(missing_player_info["run"], 1)


    def test_get_players_information_with_profile_info(self):
        # Initialize
        group = create_group()
        larp = group.larp
        players_info = example_players_complete
        create_characters_assigments(group, players=players_info)
        # Get information
        missing_info = larp.get_players_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        players_run1 = missing_info[0]
        self.assertEqual(len(players_run1), len(players_info))
        count = 0
        for missing_player_info in players_run1:
            self.assertEqual(missing_player_info["user"], players_info[count]["first_name"]+" "+players_info[count]["last_name"])
            self.assertEqual(missing_player_info["profile"].user.username, players_info[count]["username"])
            self.assertEqual(missing_player_info["profile"].gender, players_info[count]["gender"])
            self.assertEqual(missing_player_info["bookings"].bus, None)
            self.assertEqual(missing_player_info["bookings"].accomodation, None)
            self.assertEqual(missing_player_info["bookings"].sleeping_bag, None)
            self.assertEqual(missing_player_info["run"], 1)
            count += 1


    def test_get_missing_players_with_some_booking_info(self):
        # Initialize
        group = create_group()
        larp = group.larp
        player_info = example_players_complete[0]
        bookings_info = example_bookings[0]
        assigment = create_character_assigment(group, player_info)
        set_bookings(assigment, bookings_info)
        # Get information
        missing_info = larp.get_players_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"], player_info["first_name"]+" "+player_info["last_name"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["bookings"].bus, None)
        self.assertEqual(missing_player_info["bookings"].accomodation, None)
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, False)


    def test_get_players_information_with_all_booking_info(self):
        # Initialize
        group = create_group()
        larp = group.larp
        player_info = example_players_complete[0]
        bookings_info = example_bookings[1]
        assigment = create_character_assigment(group, player_info)
        set_bookings(assigment, bookings_info)
        # Get information
        missing_info = larp.get_players_information()
        # Validate
        self.assertIs(len(missing_info), 1)
        missing_player_info = missing_info[0][0]
        self.assertEqual(missing_player_info["user"], player_info["first_name"]+" "+player_info["last_name"])
        self.assertEqual(missing_player_info["profile"].user.username, player_info["username"])
        self.assertEqual(missing_player_info["bookings"].bus.name, bookings_info["bus"])
        self.assertEqual(missing_player_info["bookings"].accomodation.name, bookings_info["accomodation"])
        self.assertEqual(missing_player_info["bookings"].sleeping_bag, True)

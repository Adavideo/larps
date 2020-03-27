from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_login


class ViewsTests(TestCase):


    def test_login_page(self):
        test_login(self)


    # PLAYER PROFILE

    def test_player_profile_page(self):
        url = reverse('larps:player_profile')
        test_correct_page(self, url)


    # PLAYERS LIST

    def test_players_list_page(self):
        url = reverse('larps:players_list')
        test_correct_page(self, url)


    # CHARACTER PAGE

    def test_character_page(self):
        url = "/larps/character/1/"
        test_correct_page(self, url)


    # CHARACTERS LIST

    def test_characters_list_page(self):
        url = reverse('larps:characters_list')
        test_correct_page(self, url)


    # BOOKINGS PAGE

    def test_bookings_page(self):
        url = "/larps/bookings/1/"
        test_correct_page(self, url)


    # MANAGE BOOKINGS PAGE

    def test_manage_bookings_page(self):
        url = "/larps/bookings/larp_1/run_1/"
        test_correct_page(self, url)


    # BOOKINGS LIST

    def test_bookings_list_page(self):
        url = reverse('larps:bookings_list')
        test_correct_page(self, url)


    # PAGE FOR CSV FILE UPLOAD

    def test_csv_upload_page(self):
        url = reverse('larps:file_upload')
        test_correct_page(self, url)

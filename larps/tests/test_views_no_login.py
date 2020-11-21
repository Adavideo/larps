from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_page_no_login


class ViewsTestsNoLogin(TestCase):

    # HOME PAGE

    def test_home_page(self):
        """
            home_page() Test the home page is working
        """
        url = reverse('larps:home')
        test_correct_page(self, url)


    # PLAYER PROFILE

    def test_player_profile_page_no_login(self):
        """
            player_profile_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:player_profile')
        test_page_no_login(self, url)


    # CHARACTER PAGE

    def test_character_page_no_login(self):
        """
            character_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/character/1/"
        test_page_no_login(self, url)


    # CHARACTERS LIST

    def test_characters_list_page_no_login(self):
        """
            characters_list_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:characters_list')
        test_page_no_login(self, url)


    # BOOKINGS PAGE

    def test_bookings_page_no_login(self):
        """
            bookings_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/bookings/1/"
        test_page_no_login(self, url)


    # MANAGE BOOKINGS PAGE

    def test_manage_bookings_page_no_login(self):
        """
            bookings_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/bookings/larp_1/run_1/"
        test_page_no_login(self, url)


    # BOOKINGS LIST

    def test_bookings_list_page_no_login(self):
        """
            bookings_list_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:bookings_list')
        test_page_no_login(self, url)


    # PAGE FOR CSV FILE UPLOAD

    def test_csv_upload_page_no_login(self):
        """
            csv_upload_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:file_upload')
        test_page_no_login(self, url)

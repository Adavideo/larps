from django.test import TestCase
from django.urls import reverse


class ViewsTests(TestCase):

    login_url = "/accounts/login/?next="


    # HOME PAGE

    def test_home_page(self):
        """
            home_page() Test the home page is working
        """
        url = reverse('larps:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not only Larps")


    # PLAYER PROFILE

    def test_player_profile_page_no_login(self):
        """
            player_profile_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:player_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # PLAYERS LIST

    def test_players_list_page_no_login(self):
        """
            players_list_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:players_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # CHARACTER PAGE

    def test_character_page_no_login(self):
        """
            character_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/character/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # CHARACTERS LIST

    def test_characters_list_page_no_login(self):
        """
            characters_list_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:characters_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # BOOKINGS PAGE

    def test_bookings_page_no_login(self):
        """
            bookings_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/bookings/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # MANAGE BOOKINGS PAGE

    def test_manage_bookings_page_no_login(self):
        """
            bookings_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = "/larps/bookings/larp_1/run_1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # BOOKINGS LIST

    def test_bookings_list_page_no_login(self):
        """
            bookings_list_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:bookings_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)


    # PAGE FOR CSV FILE UPLOAD

    def test_csv_upload_page_no_login(self):
        """
            csv_upload_page_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:file_upload')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url + url)

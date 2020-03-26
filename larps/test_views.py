from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

from django.urls import reverse



class ViewsTests(TestCase):

    def test_home(self):
        """
            home() Test the home page is working
        """
        url = reverse('larps:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not only Larps")


    # PLAYER PROFILE

    def test_player_profile_no_login(self):
        """
            player_profile_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:player_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/larps/player_profile/")


    # PLAYERS LIST

    def test_players_list_no_login(self):
        """
            players_list_no_login() checks that it redirects to login when trying to access this page anonimously.
        """
        url = reverse('larps:players_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/larps/players")

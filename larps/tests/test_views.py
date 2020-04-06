from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_login
from larps.models import Bookings
from larps.views import generate_bookings
from .util_test import create_group, create_character_assigment


class ViewsTests(TestCase):

    def test_login_page(self):
        test_login(self)

    # PAGE FOR CSV FILE UPLOAD

    def test_csv_upload_page(self):
        url = reverse('larps:file_upload')
        # response = test_correct_page(self, url)
        # self.assertContains(response, "Import CSV files")


    # PAGE FOR UNIFORMS
    def test_uniforms_page(self):
        url = reverse("larps:uniforms")
        #response = test_correct_page(self, url)


    def test_generate_bookings(self):
        # initialize
        group = create_group()
        assigment = create_character_assigment(group)
        user = assigment.user
        # execute
        generate_bookings(user)
        # validate
        bookings_search = Bookings.objects.all()
        self.assertIs(len(bookings_search), 1)
        self.assertEqual(bookings_search[0].user.username, user.username)

from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_login


class ViewsTests(TestCase):


    def test_login_page(self):
        test_login(self)

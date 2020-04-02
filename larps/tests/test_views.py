from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_login
from larps.models import Uniform
from .util_test import *


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

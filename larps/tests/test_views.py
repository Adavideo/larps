from django.test import TestCase
from django.urls import reverse
from .util_test_views import test_correct_page, test_login
from larps.config import login_required_enabled


class ViewsTests(TestCase):

    def test_login_page(self):
        test_login(self)

    # PAGE FOR CSV FILE UPLOAD

    def test_csv_upload_page(self):
        url = reverse('larps:file_upload')
        if not login_required_enabled():
            response = test_correct_page(self, url)
            self.assertContains(response, "Import CSV files")


    # PAGE FOR UNIFORMS
    def test_uniforms_page(self):
        url = reverse("larps:uniforms")
        if not login_required_enabled():
            response = test_correct_page(self, url)

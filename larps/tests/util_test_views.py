from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

login_url = reverse('login')

# checks that it loads the page without problems
def test_correct_page(test, url):
    response = test.client.get(url)
    test.assertEqual(response.status_code, 200)
    test.assertContains(response, "Not only Larps")
    return response

def test_login(test):
    new_user = User(username="ana", first_name="ana", password="secret34")
    response = test.client.post(login_url, {'username': "ana", 'password': "secret34"})
    test.assertEqual(response.status_code, 200)
    test.assertContains(response, "Not only Larps")
    return response

# checks that it redirects to login when trying to access the page anonimously.
def test_page_no_login(test, url):
    response = test.client.get(url)
    test.assertEqual(response.status_code, 302)
    test.assertEqual(response.url, login_url +  "?next=" + url)
    return response

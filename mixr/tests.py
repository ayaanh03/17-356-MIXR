from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_home_page_exists(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def create_room_exists(self):
        response = self.client.get('/createRoom/', follow=True)
        self.assertEqual(response.status_code, 200)

    def join_room_exists(self):
        response = self.client.get('/joinRoom', follow=True)
        self.assertEqual(response.status_code, 200)

    def home_view_uses_correct_template(self):
        print("testing home uses correct template")
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def join_room_uses_correct_template(self):
        print("testing join private uses correct template")
        response = self.client.get('/joinRoom', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'joinPrivate.html')

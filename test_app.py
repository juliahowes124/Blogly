from unittest import TestCase

from app import app

from models import User, db

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BloglyTestCase(TestCase):
    """Test flask app of Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):

        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)

    def test_users_page(self):

        with self.client as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_create_user_page(self):

        with self.client as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)

    def test_create_user_post(self):

        with self.client as client:
            response = client.post('/users/new',  data={
                "first": "This is",
                "last": "a stupid test",
                "image": "http://joelburton.com/joel-burton.jpg"
            }, follow_redirects=True)
            html = response.get_data(as_text=True)
            user = User.query.filter(User.first_name == "This is", User.last_name == "a stupid test")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(user)
            self.assertIn('This is a stupid test', html)

    def test_user_page(self):

        with self.client as client:
            user_id = User.find_user_id("This is", "a stupid test")
            response = client.get(f"/users/{user_id}") 
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="btn btn-primary">Edit</button>', html)

    def test_user_edit_page(self):

        with self.client as client:
            user_id = User.find_user_id("This is", "a stupid test")
            response = client.get(f"/users/{user_id}/edit") 
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="btn btn-outline-primary">Cancel</button>', html)

    def test_edit_user_post(self):
        with self.client as client:
            user_id = User.find_user_id("This is", "a stupid test")
            response = client.post(f"/users/{user_id}/edit",  data={
                "first": "This is2",
                "last": "a stupid test2",
                "image": ""
            }, follow_redirects=True)
            html = response.get_data(as_text=True)
            user = User.query.filter(User.first_name == "This is2", User.last_name == "a stupid test2").first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user.last_name, "a stupid test2")
            self.assertIn('This is2 a stupid test2', html)

    def test_delete_user(self):

        with self.client as client:
            user_id = User.find_user_id("This is2", "a stupid test2")
            response = client.post(f"/users/{user_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)
            user = User.query.get(user_id)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(user)
            self.assertNotIn('This is2 a stupid test2', html)
            

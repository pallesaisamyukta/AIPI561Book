import sys
import os

# Ensure the app.py file can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import unittest

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Setup the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_endpoint(self):
        # Test the root endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello World")

    def test_test_endpoint(self):
        # Test the /test endpoint
        response = self.app.post('/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": "Hello from /test endpoint"})

    def test_summarize_endpoint(self):
        # Test the /summarize endpoint with a mock PDF path
        pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
        response = self.app.post('/summarize', json={'pdf_path': 'sample.pdf'})
        self.assertEqual(response.status_code, 200)
        # Check if the summary key exists in the response
        self.assertIn('summary', response.json)

if __name__ == '__main__':
    unittest.main()

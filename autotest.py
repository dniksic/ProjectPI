import unittest
from firebase_admin import credentials, initialize_app, db
from datetime import datetime

class TestDatabaseIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the Firebase app
        cred = credentials.Certificate("serviceAccountKey.json")
        initialize_app(cred, {
            'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/",
            'storageBucket': "evidencijaprepoznavanjemlica.appspot.com"
        })

    def setUp(self):
        # Set up the test data in the database
        self.student_id = '123456'
        ref = db.reference(f'Studenti/{self.student_id}')
        ref.set({
            'name': 'Test Student',
            'zadnja_evidencija_vrijeme': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ukupno_dolazaka': 0,
            'titula': 'Student',
            'godina': '3',
            'godina_upisa': '2021'
        })

    def tearDown(self):
        # Clean up the test data
        db.reference(f'Studenti/{self.student_id}').delete()

    def test_fetch_student_info(self):
        student_info = db.reference(f'Studenti/{self.student_id}').get()
        self.assertIsNotNone(student_info)
        self.assertIn('zadnja_evidencija_vrijeme', student_info)

    def test_update_student_info(self):
        ref = db.reference(f'Studenti/{self.student_id}')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ref.child('zadnja_evidencija_vrijeme').set(now)
        updated_info = db.reference(f'Studenti/{self.student_id}').get()
        self.assertEqual(updated_info['zadnja_evidencija_vrijeme'], now)

if __name__ == '__main__':
    unittest.main()

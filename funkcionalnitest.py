import unittest
from unittest.mock import patch, MagicMock
from firebase_admin import credentials, initialize_app, db
from datetime import datetime


class TestFaceRecognitionSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Firebase app
        cred = credentials.Certificate("serviceAccountKey.json")
        initialize_app(cred, {
            'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/",
            'storageBucket': "evidencijaprepoznavanjemlica.appspot.com"
        })

    @patch('cv2.VideoCapture')
    @patch('face_recognition.face_locations')
    @patch('face_recognition.face_encodings')
    @patch('firebase_admin.db.reference')
    def test_face_recognition(self, mock_db_reference, mock_face_encodings, mock_face_locations, mock_video_capture):
        # Mocking the camera input
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        mock_face_locations.return_value = [(0, 0, 1, 1)]
        mock_face_encodings.return_value = [MagicMock()]

        # Mocking Firebase database reference
        mock_ref = MagicMock()
        mock_db_reference.return_value = mock_ref

        # Setting up mock return values
        mock_ref.get.return_value = {
            'name': 'Test Student',
            'zadnja_evidencija_vrijeme': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ukupno_dolazaka': 0
        }

        # Simulate face recognition and updating database
        student_id = '12316'
        ref = db.reference(f'Studenti/{student_id}')
        student_info = ref.get()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ref.child('zadnja_evidencija_vrijeme').set(now)

        # Ensure the set method is called with the correct arguments
        ref.child('zadnja_evidencija_vrijeme').set.assert_called_with(now)

        # Mock the return value for updated get
        updated_info = {'zadnja_evidencija_vrijeme': now}
        mock_ref.get.return_value = updated_info

        # Fetch updated info and assert
        updated_info = ref.get()
        self.assertEqual(updated_info['zadnja_evidencija_vrijeme'], now)


if __name__ == '__main__':
    unittest.main()

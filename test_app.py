import tempfile
import unittest
from pathlib import Path

import app


class StudentEnquiryTests(unittest.TestCase):
    def setUp(self):
        temp_db = Path(tempfile.gettempdir()) / "sk_coaching_test_students.db"
        if temp_db.exists():
            temp_db.unlink()
        app.DB_PATH = temp_db
        app.init_db()
        self.client = app.app.test_client()

    def tearDown(self):
        db_path = Path(app.DB_PATH)
        if db_path.exists():
            db_path.unlink()

    def test_create_enquiry_success(self):
        payload = {
            "name": "Aarav",
            "class_name": "Class 8",
            "phone": "9876543210",
            "course": "Middle School",
        }

        response = self.client.post("/api/enquiry", json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("id", data)

    def test_create_enquiry_rejects_missing_data(self):
        response = self.client.post(
            "/api/enquiry",
            json={"name": "Aarav", "class_name": "Class 8"},
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])


if __name__ == "__main__":
    unittest.main()

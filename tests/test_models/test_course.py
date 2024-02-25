import unittest
import models
from models.course import Course
from models.document import Document

class TestCourse(unittest.TestCase):
    def setUp(self):
        self.course = Course(name="Computer Science", dept_id="DEP001")
        self.document = Document(title="Test Document", category="Test", course_id=self.course.id, stud_id="STU001", tags=["test", "document"])

    def test_init(self):
        self.assertEqual(self.course.name, "Computer Science")
        self.assertEqual(self.course.dept_id, "DEP001")

    def test_documents(self):
        models.storage.new(self.document)
        models.storage.save()
        self.assertIn(self.document, self.course.documents.values())

if __name__ == '__main__':
    unittest.main()
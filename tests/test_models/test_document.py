import unittest
import os
from models.document import Document
from models.student import Student

class TestDocument(unittest.TestCase):
    def setUp(self):
        self.student = Student(name="John Doe", email="johndoe@example.com", school_id="SCH001", dept_id="DEP001")
        self.document = Document(title="Test Document", category="Test", course_id="CSE101", stud_id=self.student.id, tags=["test", "document"])

    def test_init(self):
        self.assertEqual(self.document.title, "Test Document")
        self.assertEqual(self.document.category, "Test")
        self.assertEqual(self.document.course_id, "CSE101")
        self.assertEqual(self.document.stud_id, self.student.id)
        self.assertEqual(self.document.tags, ["test", "document"])

    def test_save(self):
        test_file = "test.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file.")
        self.document.save(test_file)
        self.assertTrue(os.path.exists(f'docs/{self.document.filename}'))
        os.remove(test_file)
        os.remove(f'docs/{self.document.filename}')

    def test_get_file(self):
        test_file = "test.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file.")
        self.document.save(test_file)
        self.assertEqual(self.document.get_file(), "Saved Successfully!")
        self.assertTrue(os.path.exists(f'return/{self.document.title}.txt'))
        os.remove(test_file)
        os.remove(f'docs/{self.document.filename}')
        os.remove(f'return/{self.document.title}.txt')

if __name__ == '__main__':
    unittest.main()
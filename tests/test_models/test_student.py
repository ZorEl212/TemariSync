import unittest
from models.student import Student
from models.document import Document
from models.department import Department
import models
class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(name="John Doe", email="johndoe@example.com", school_id="SCH001", dept_id="DEP001")
        self.document = Document(stud_id=self.student.id)
        self.department = Department(id=self.student.dept_id, name="Computer Science")

    def test_init(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "johndoe@example.com")
        self.assertEqual(self.student.school_id, "SCH001")
        self.assertEqual(self.student.dept_id, "DEP001")

    def test_documents(self):
        self.assertIn(self.document, self.student.documents.values())

    def test_department(self):
        self.assertEqual(self.student.department, "Computer Science")

if __name__ == '__main__':
    unittest.main()
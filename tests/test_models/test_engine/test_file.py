import unittest
from models.engine.file import FileStorage
from models import storage
from models.student import Student
from models.document import Document
from models.department import Department
from models.course import Course
import models
import os
class TestFileStorage(unittest.TestCase):
    @classmethod
    def setUp(cls):
        # Add test objects to the storage
        models.storage.new(Student(name="John", stud_id='1234/56', id='1234', email='john@example.com'))
        models.storage.new(Student(name="Jane", stud_id='7890/12', id='7890', email='jane@example.com'))
        models.storage.new(Department(name="Computer Science", id='3214'))
        models.storage.new(Course(name="Python Programming", id='4545'))
        models.storage.new(Document(name="Sample Document", id='8585'))
        models.storage.save()
        models.storage.reload()
        
    def tearDown(self):
       # storage.__objs = {}
        storage.save()
        if os.path.exists('file.json'):
            os.remove('file.json')
            storage.reload()

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_new(self):
        student = Student(name="Yeabsira", stud_id='3156/14', email='yabsirad212@gmail.com')
        key = f"{student.cls_name}.{student.id}"
        self.assertIn(key, models.storage.all())

    def test_FileStorage_instantiation_no_args(self):
        """Test FileStorage init with no args"""
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        """Test init with args = None"""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        """Test filee_path is a private string"""
        self.assertEqual(str, type(FileStorage._FileStorage__path))

    def testFileStorage_objects_is_private_dict(self):
        """Test objects is a private dictionary"""
        self.assertEqual(dict, type(FileStorage._FileStorage__objs))

    def test_storage_initializes(self):
        """Test if the class inits"""
        self.assertEqual(type(models.storage), FileStorage)

    def test_all_with_cls_argument(self):
        """Test all() method with cls argument"""
        # Test with cls argument as "Student"
        result = models.storage.all(cls="Student")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), storage.count(Student))
        self.assertTrue(all(isinstance(obj, Student) for obj in result.values()))

        # Test with cls argument as "Department"
        result = models.storage.all(cls="Department")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), storage.count(Department))
        self.assertTrue(all(isinstance(obj, Department) for obj in result.values()))

        # Test with cls argument as "Course"
        result = models.storage.all(cls="Course")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), storage.count(Course))
        self.assertTrue(all(isinstance(obj, Course) for obj in result.values()))

        # Test with cls argument as "Document"
        result = models.storage.all(cls="Document")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), storage.count(Document))
        self.assertTrue(all(isinstance(obj, Document) for obj in result.values()))

    def test_save_and_reload(self):

        # Save the objects to file
        models.storage.save()

        # Clear the objects from memory
        models.storage._FileStorage__objs = {}

        # Reload the objects from file
        models.storage.reload()

        # Check if the objects are reloaded correctly
        self.assertEqual(len(models.storage.all()), storage.count())
        self.assertIsInstance(models.storage.get("Student", "1234"), Student)
        self.assertIsInstance(models.storage.get("Department", '3214'), Department)
        self.assertIsInstance(models.storage.get("Course", '4545'), Course)
        self.assertIsInstance(models.storage.get("Document", '8585'), Document)

    def test_get(self):
        # Test get() with cls argument as string
        student = models.storage.get("Student", "1234")
        self.assertIsInstance(student, Student)
        self.assertEqual(student.name, "John")
        self.assertEqual(student.stud_id, "1234/56")
        self.assertEqual(student.email, "john@example.com")

        # Test get() with cls argument as class
        department = models.storage.get(Department, '3214')
        self.assertIsInstance(department, Department)
        self.assertEqual(department.name, "Computer Science")

        course = models.storage.get(Course, '4545')
        self.assertIsInstance(course, Course)
        self.assertEqual(course.name, "Python Programming")

        document = models.storage.get(Document, '8585')
        self.assertIsInstance(document, Document)
        self.assertEqual(document.name, "Sample Document")

        # Test get() with invalid cls argument
        invalid_obj = models.storage.get("InvalidClass", None)
        self.assertIsNone(invalid_obj)

    def test_close(self):
        """Test close() method"""
        # Save the objects to file
        models.storage.save()

        # Clear the objects from memory
        models.storage._FileStorage__objs = {}

        # Call close() method to reload the objects
        models.storage.close()

        # Check if the objects are reloaded correctly
        self.assertEqual(len(models.storage.all()), storage.count())
        self.assertIsInstance(models.storage.get("Student", "1234"), Student)
        self.assertIsInstance(models.storage.get("Department", '3214'), Department)
        self.assertIsInstance(models.storage.get("Course", '4545'), Course)
        self.assertIsInstance(models.storage.get("Document", '8585'), Document)

if __name__ == '__main__':
    unittest.main()
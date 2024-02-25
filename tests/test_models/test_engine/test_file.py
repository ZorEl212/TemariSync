import unittest
from models.engine.file import FileStorage
from models.student import Student
import models
class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.student = Student(name="Yeabsira", stud_id='3156/14', email='yabsirad212@gmail.com')

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_new(self):
        key = f"{self.student.cls_name}.{self.student.id}"
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


if __name__ == '__main__':
    unittest.main()
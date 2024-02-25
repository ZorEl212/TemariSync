import unittest
from models.base import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base_model = BaseModel()

    def test_init(self):
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_str(self):
        expected_str = f"[{self.base_model.cls_name}] ({self.base_model.id}) {self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), expected_str)

    def test_save(self):
        old_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(self.base_model.updated_at, old_updated_at)

    def test_get_cls_name(self):
        self.assertEqual(self.base_model.get_cls_name(), "BaseModel")

    def test_cls_name(self):
        self.assertEqual(self.base_model.cls_name, "BaseModel")

    def test_to_dict(self):
        base_model_dict = self.base_model.to_dict()
        self.assertEqual(base_model_dict['__class__'], "BaseModel")
        self.assertIsInstance(base_model_dict['created_at'], str)
        self.assertIsInstance(base_model_dict['updated_at'], str)

    def test_init_with_kwargs(self):
        kwargs = {
            'id': 'test_id',
            'created_at': '2022-01-01T00:00:00.000000',
            'updated_at': '2022-01-01T00:00:00.000000',
            'name': 'test_name',
            'value': 123
        }
        base_model = BaseModel(**kwargs)
        self.assertEqual(base_model.id, 'test_id')
        self.assertEqual(base_model.created_at, datetime(2022, 1, 1, 0, 0))
        self.assertEqual(base_model.updated_at, datetime(2022, 1, 1, 0, 0))
        self.assertEqual(base_model.name, 'test_name')
        self.assertEqual(base_model.value, 123)

if __name__ == '__main__':
    unittest.main()
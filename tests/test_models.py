import unittest

from parameterized import parameterized

from ramorm import orm, fields, model


class TestModel(model.Model):
    a = model.IntegerField(default=1)


class TestModel2(model.Model):
    a = model.IntegerField(default=1)


class OrmTest(unittest.TestCase):

    @parameterized.expand([
        ['int', 123],
        ['obj', model.Model]
    ])

    def test_Orm(self, name, val):
        self.assertTrue(orm.Orm('test'))
        with self.assertRaises(TypeError):
            orm.Orm(val)

    def test_orm_push(self):
        db = orm.Orm('testcase')
        valerr = [int(), str(), float(), list(), tuple(), object(), int, str, float, list, tuple, object]
        for item in valerr:
            with self.assertRaises(ValueError):
                db.push(item)
        self.assertTrue(db.push(TestModel()))

    def test_orm_get(self):
        db = orm.Orm('testcase')
        test = TestModel()
        test2 = TestModel2()
        db.push(test)
        self.assertEqual(db.get(TestModel), test)
        self.assertIsNone(db.get(TestModel2))
        db.push(test2)
        self.assertNotEqual(db.get(TestModel), test2)

    def test_orm_drop(self):
        db = orm.Orm('testcase')
        test = TestModel()
        db.push(test)
        self.assertEqual(db.get(TestModel), test)
        self.assertEqual(db.drop(), [])

    def test_orm_delete(self):
        db = orm.Orm('testcase')
        test = TestModel()
        db.push(test)
        test3 = TestModel(a=2)
        db.push(test3)
        test2 = TestModel2()
        db.push(test2)
        db.delete(TestModel, a=1)
        self.assertEqual(db.filter(TestModel), [test3])
        print(db.filter(TestModel))
        self.assertEqual(db.get(TestModel2), test2)


class FieldsTest(unittest.TestCase):

    def test_IntegerField(self):
        self.assertTrue(fields.IntegerField(default=1))


if __name__ == '__main__':
    unittest.main()

# ramorm
Model based ORM in memory

###Usage
```python
import orm
import model

db = orm.Orm('my_test_database') 

class TestModel(model.Model):
    a = model.IntegerField(default=1)

test_obj = TestModel()

print(test_obj.a)
>> 1

db.push(test_obj)

get_my_obj = db.get(TestModel, a=1)
print(get_my_obj.a)
>> 1

```
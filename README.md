# ramorm
Model based ORM in memory

![codecov](https://codecov.io/gh/Yurzs/ramorm/branch/master/graph/badge.svg)
### Usage
```python
import orm
import model

db = orm.Orm('my_test_database') 

class Vehicle(model.Model):
    name = model.TextField()
    wheels = model.IntegerField(default=4)
    max_speed = model.IntegerField(default=100)

tesla3 = Vehicle(name='Tesla Model3', max_speed=230)
print(tesla3.name,tesla3.wheels, tesla3.max_speed)
>> ('Tesla Model3', 4, 230)

bicycle = Vehicle(name='Bicycle', wheels=2, max_speed=50)
print(bicycle.wheels, bicycle.max_speed)
>> ('Bicycle', 2, 50)

db.push(tesla3, bicycle)

print(db.get(Vehicle, wheels=4).name)
>> 'Tesla Model3'

print(db.get(Vehicle, name='Bicycle').max_speed
>> 50

db.push(test_obj)

get_my_obj = db.get(TestModel, a=1)
print(get_my_obj.a)
>> 1

```

### Comming soon

-[ ] Filter

-[ ] Backup to file

-[ ] Integration with postgresql, reddis
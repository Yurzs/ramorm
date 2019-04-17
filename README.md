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
```
Add your model based objects to database using ```push``` function, you can pass one or multiple objects at once
```python
db.push(tesla3, bicycle)
```
Retrieving single objects from database is possible using ```get``` function
```python
print(db.get(Vehicle, wheels=4).name)
>> 'Tesla Model3'

print(db.get(Vehicle, name='Bicycle').max_speed
>> 50
```
For filtering numerical parameters you can use ```__gt``` (greater), ```__gte``` (greater or equal), ```__lt``` (lower), ```__lte```(lower or equal)
```python
print(db.get(Vehicle, max_speed__gt=70).name)
>> 'Tesla Model3'
```
For retrieving multiple objects at once use ```filter```

```python
for vehicle in db.filter(Vehicle, max_speed__gte=10):
    print(vehicle.name, vehicle.wheels, vehicle.max_speed)
>>  ('Tesla Model3', 4, 230)
>>  ('Bicycle', 2, 50)
```
For deleting objects from db use ```delete``` function. Returns true if changes were made to database
```python
db.delete(Vehicle, name='Bicycle')
>> True
db.delete(Vehicle, name='Starship')
>> False
```
If you want completely delete all data in your database use ```drop```
.Returns array of objects in db (empty)
```python
db.drop()
>> []
```
### Coming soon

- [ ] Delete objects using ```.delete()```
    
- [ ] Order by

- [ ] Backup to file

- [ ] PyPI package

- [ ] Integration with postgresql, redis
# ramorm [Alpha]
Model based ORM in RAM. Made for performance. Please do not store critical data (yet)

![codecov](https://codecov.io/gh/Yurzs/ramorm/branch/master/graph/badge.svg)

### Installation
```
pip install ramorm
```
### Usage
```python
from ramorm import orm, model

db = orm.Orm('my_test_database') 

class Vehicle(model.Model):
    name = model.TextField()
    wheels = model.IntegerField(default=4)
    max_speed = model.IntegerField(default=100)

sports_car = Vehicle(name='Aventador', max_speed=230)
print(sports_car.name,sports_car.wheels, sports_car.max_speed)
>> 'Aventador' 4 230

bicycle = Vehicle(name='Bicycle', wheels=2, max_speed=50)
print(bicycle.wheels, bicycle.max_speed)
>> 'Bicycle' 2 50
```
Add your model based objects to database using ```push``` function, you can pass one or multiple objects at once
```python
db.push(sports_car, bicycle)
```
Retrieving single objects from database is possible using ```get``` function
```python
print(db.get(Vehicle, wheels=4).name)
>> 'Aventador'

print(db.get(Vehicle, name='Bicycle').max_speed
>> 50
```
For filtering numerical parameters you can use ```__gt``` (greater), ```__gte``` (greater or equal), ```__lt``` (lower), ```__lte```(lower or equal)
```python
print(db.get(Vehicle, max_speed__gt=70).name)
>> 'Aventador'
```
For retrieving multiple objects at once use ```filter```

```python
for vehicle in db.filter(Vehicle, max_speed__gte=10):
    print(vehicle.name, vehicle.wheels, vehicle.max_speed)
>>  'Aventador' 4 230
>>  'Bicycle' 2 50
```
For deleting objects from db use ```delete``` function. Returns ```True``` if changes were made to database
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

- [x] PyPI package

- [ ] Integration with postgresql, redis

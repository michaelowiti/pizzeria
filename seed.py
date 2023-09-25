from app import db, Restaurant, Pizza, RestaurantPizza
from faker import Faker

fake = Faker()

# Create restaurants
for _ in range(10):
    restaurant = Restaurant(
        name=fake.unique.first_name() + " Pizza",
        address=fake.address(),
    )
    db.session.add(restaurant)

# Create pizzas
for _ in range(10):
    pizza = Pizza(
        name=fake.unique.first_name(),
        ingredients=fake.sentence()
    )
    db.session.add(pizza)

# Create restaurant_pizzas
for restaurant in Restaurant.query.all():
    for pizza in Pizza.query.all():
        restaurant_pizza = RestaurantPizza(
            price=fake.random_int(min=1, max=30),
            restaurant=restaurant,
            pizza=pizza
        )
        db.session.add(restaurant_pizza)

db.session.commit()
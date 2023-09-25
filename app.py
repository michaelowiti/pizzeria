from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from models import Restaurant, Pizza, RestaurantPizza
from database import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
db.init_app(app)
api = Api(app)

app.app_context().push()
db.create_all()

parser = reqparse.RequestParser()
parser.add_argument('price', type=float, help='Price must be a float between 1 and 30', required=True)
parser.add_argument('pizza_id', type=int, help='Pizza ID is required', required=True)
parser.add_argument('restaurant_id', type=int, help='Restaurant ID is required', required=True)


class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in restaurants]


class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'pizzas': [
                    {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
                    for pizza in restaurant.pizzas
                ]
            }
        else:
            abort(404, error='Restaurant not found')

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            abort(404, error='Restaurant not found')


class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas]


class RestaurantPizzaResource(Resource):
    def post(self):
        args = parser.parse_args()
        price = args['price']
        pizza_id = args['pizza_id']
        restaurant_id = args['restaurant_id']

        if not (1 <= price <= 30):
            abort(400, errors=['Validation error: Price must be between 1 and 30'])

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if pizza and restaurant:
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()
            return {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }, 201
        else:
            abort(400, errors=['Validation error: Pizza or Restaurant not found'])


@app.route('/')
def home():
    return f'<h1>Welcome to the Pizza Restaurant API</h1>'


api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaListResource, '/pizzas')
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(debug=True)

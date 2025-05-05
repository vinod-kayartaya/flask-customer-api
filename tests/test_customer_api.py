import unittest
import json
from app import create_app, db
from app.models.customer import Customer

class TestCustomerAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        # Test valid customer creation
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'city': 'New York'
        }
        response = self.client.post('/api/customers',
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

        # Test duplicate email
        response = self.client.post('/api/customers',
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing required fields
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/customers',
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_customers(self):
        # Create test customers
        with self.app.app_context():
            customer1 = Customer(name='John Doe', email='john@example.com')
            customer2 = Customer(name='Jane Doe', email='jane@example.com')
            db.session.add_all([customer1, customer2])
            db.session.commit()

        response = self.client.get('/api/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_customer(self):
        # Create test customer
        with self.app.app_context():
            customer = Customer(name='John Doe', email='john@example.com')
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

        # Test get existing customer
        response = self.client.get(f'/api/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

        # Test get non-existing customer
        response = self.client.get('/api/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        # Create test customer
        with self.app.app_context():
            customer = Customer(name='John Doe', email='john@example.com')
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

        # Test valid update
        data = {'name': 'John Updated'}
        response = self.client.put(f'/api/customers/{customer_id}',
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Updated')

        # Test update non-existing customer
        response = self.client.put('/api/customers/999',
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        # Create test customer
        with self.app.app_context():
            customer = Customer(name='John Doe', email='john@example.com')
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

        # Test delete existing customer
        response = self.client.delete(f'/api/customers/{customer_id}')
        self.assertEqual(response.status_code, 204)

        # Test delete non-existing customer
        response = self.client.delete('/api/customers/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 
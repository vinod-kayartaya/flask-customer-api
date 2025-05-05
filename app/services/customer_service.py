from app.dao.customer_dao import CustomerDAO
from app.dto.customer_dto import CustomerDTO
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()
        self.dto = CustomerDTO()

    def create_customer(self, data):
        try:
            # Validate input data
            validated_data = self.dto.load(data)
            
            # Check for existing email
            if self.dao.get_by_email(validated_data['email']):
                raise ValueError("Email already exists")
            
            # Check for existing phone if provided
            if validated_data.get('phone') and self.dao.get_by_phone(validated_data['phone']):
                raise ValueError("Phone number already exists")
            
            # Create customer
            customer = self.dao.create(validated_data)
            return self.dto.dump(customer)
        except ValidationError as e:
            raise ValueError(str(e))
        except IntegrityError:
            raise ValueError("Database integrity error")

    def get_all_customers(self):
        customers = self.dao.get_all()
        return self.dto.dump(customers, many=True)

    def get_customer_by_id(self, customer_id):
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        return self.dto.dump(customer)

    def update_customer(self, customer_id, data):
        try:
            # Validate input data
            validated_data = self.dto.load(data, partial=True)
            
            # Check if customer exists
            if not self.dao.get_by_id(customer_id):
                raise ValueError("Customer not found")
            
            # Check for email uniqueness if email is being updated
            if 'email' in validated_data:
                existing = self.dao.get_by_email(validated_data['email'])
                if existing and existing.id != customer_id:
                    raise ValueError("Email already exists")
            
            # Check for phone uniqueness if phone is being updated
            if 'phone' in validated_data:
                existing = self.dao.get_by_phone(validated_data['phone'])
                if existing and existing.id != customer_id:
                    raise ValueError("Phone number already exists")
            
            # Update customer
            customer = self.dao.update(customer_id, validated_data)
            return self.dto.dump(customer)
        except ValidationError as e:
            raise ValueError(str(e))
        except IntegrityError:
            raise ValueError("Database integrity error")

    def delete_customer(self, customer_id):
        if not self.dao.delete(customer_id):
            raise ValueError("Customer not found")
        return True 
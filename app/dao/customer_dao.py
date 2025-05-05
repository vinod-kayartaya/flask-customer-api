from app.models.customer import Customer
from app import db
from sqlalchemy.exc import IntegrityError

class CustomerDAO:
    @staticmethod
    def create(customer_data):
        customer = Customer(**customer_data)
        try:
            db.session.add(customer)
            db.session.commit()
            return customer
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def get_all():
        return Customer.query.all()

    @staticmethod
    def get_by_id(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def get_by_email(email):
        return Customer.query.filter_by(email=email).first()

    @staticmethod
    def get_by_phone(phone):
        return Customer.query.filter_by(phone=phone).first()

    @staticmethod
    def update(customer_id, customer_data):
        customer = CustomerDAO.get_by_id(customer_id)
        if customer:
            for key, value in customer_data.items():
                setattr(customer, key, value)
            try:
                db.session.commit()
                return customer
            except IntegrityError:
                db.session.rollback()
                raise
        return None

    @staticmethod
    def delete(customer_id):
        customer = CustomerDAO.get_by_id(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return True
        return False 
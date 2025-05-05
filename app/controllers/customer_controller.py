from flask import Blueprint, request, jsonify
from app.services.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__)
customer_service = CustomerService()

@customer_bp.route('/api/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        result = customer_service.create_customer(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/api/customers', methods=['GET'])
def get_all_customers():
    try:
        customers = customer_service.get_all_customers()
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        return jsonify(customer), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.get_json()
        result = customer_service.update_customer(customer_id, data)
        return jsonify(result), 200
    except ValueError as e:
        # Check if the error message indicates a not found error
        if "Customer not found" in str(e):
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer_service.delete_customer(customer_id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
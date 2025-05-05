from marshmallow import Schema, fields, validate

class CustomerDTO(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    city = fields.Str(validate=validate.Length(max=50)) 
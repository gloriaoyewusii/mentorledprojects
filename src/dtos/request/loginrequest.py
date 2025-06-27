from marshmallow import Schema, fields, validate

from src.models.user import User


class LoginRequest(Schema):
    id = fields.String(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=4, max=8))

    class Meta(Schema.Meta):
        model = User
        fields = ('id', 'email')

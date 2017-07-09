from schematics.types import IntType, StringType, FloatType, UUIDType
from schematics.types.compound import ModelType, ListType
from schematics.exceptions import DataError, ValidationError
from schematics.models import Model
import uuid


def validate_age(value):
	if int(value) < 0:
		raise ValidationError(u'Age must be a positive integer')
	return value

def validate_income(value):
	if float(value) < 0:
		raise ValidationError(u'Income must be a float greater than or equal to zero')
	return value

class User(Model):
    age = IntType(required=True, validators=[validate_age])
    gender = StringType(required=True, choices=['male', 'female'])


class Household(Model):
    members = ListType(ModelType(User), required=True, min_size=1)
    income = FloatType(required=True, validators=[validate_income])
    id = UUIDType(default=uuid.uuid4)
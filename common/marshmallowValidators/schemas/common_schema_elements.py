import re
from marshmallow import Schema, ValidationError, fields


def validate_all_caps(value):
    if not value.isupper():
        raise ValidationError("Field must be all capital letters.")


def validate_positive_integer_as_string(value):
    if not isinstance(value, str):
        if not value.isdigit():
            raise ValidationError("String value is not a positive integer")
        int_value = int(value)
        if int_value < 0:
            raise ValidationError("Field must be a positive integer.")


def validate_positive_integer(value):
    if not isinstance(value, int) or value <= 0:
        raise ValidationError("Field must be a positive integer.")

def validate_positive_float(value):
    if not isinstance(value, float) or value <= 0:
        raise ValidationError("Field must be a positive float.")

def validate_non_negative_integer(value):
    if not isinstance(value, int) or value < 0:
        raise ValidationError("Field must be a non negative integer.")


def validate_non_negative_float(value):
    if not isinstance(value, float) or value < 0:
        raise ValidationError("Field must be a non-negative float")


def validate_float_constrained(value):
    if not isinstance(value, float) or value < 0 or value > 1:
        raise ValidationError("Field must be a float within 0 <= value <= 1")


def validate_hex_40(value):
    if not re.match(r"^0x[0-9a-fA-F]{40}$", value):
        raise ValidationError(
            "Field must be a 40-character hexadecimal string starting with 0x."
        )


def validate_hex_64(value):
    if not re.match(r"^0x[0-9a-fA-F]{64}$", value):
        raise ValidationError(
            "Field must be a 64-character hexadecimal string starting with 0x."
        )


def validate_hex(value):
    if not re.match(r"^0x[0-9a-fA-F]+$", value):
        raise ValidationError("Field must be a hexadecimal string starting with 0x.")


def validate_non_zero_integer(value):
    if not isinstance(value, int) or value == 0:
        raise ValidationError("Field must be a non zero integer.")
    
def validate_postion_type(value):
    testSet = {"swap","concentrated", "knockout", "ambient"}
    if not isinstance(value, str) or not value in testSet:
        raise ValidationError("Field must be a swap, concentrated, knockout or ambient postion type.")

class serverResponce(Schema):
    hostname = fields.String(required=True)
    serverTime = fields.Integer(required=True,validate=validate_positive_integer)


from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
import phonenumbers


class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])

    def validate_phone(form, field):
        number = field.data
        if number.startswith('0'):
            number = '+353' + number[1:]
        try:
            input_number = phonenumbers.parse(number)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number!')
        except:
            raise ValidationError('Invalid phone number!')
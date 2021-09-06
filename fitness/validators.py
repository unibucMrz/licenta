from django.core.exceptions import ValidationError
from account.models import Account
from django.utils.timezone import now as today

def validate_trainer(user):


    print(user)

    return user

    if not user.is_trainer:
        raise ValidationError("Is not trainer")
    else:
        return user


def validate_date(date):
    if date < today().date():
        raise ValidationError('Day in the past.')
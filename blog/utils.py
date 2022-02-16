from django.core.exceptions import ValidationError

def validate_password_strength(value):
    """Validates that a password is as least 10 characters long and has at least
    2 digits and 1 Upper case letter.
    """
    min_length = 8

    if len(value) < min_length:
        raise ValidationError(f'Password must be at least {min_length} characters '
                                'long.')

    if sum(c.isdigit() for c in value) < 1 or sum(c.isalpha() for c in value) < 1:
        raise ValidationError('Password must container at least 1 digits and 1 letter')

    return value
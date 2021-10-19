import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
username_reguex = "^[a-zA-Z0-9_.-]+$"
user_reguex = "^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+" \
              "([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+" \
              "[\s]?([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])?$"
text_reguex = "[a-zA-Z ]{2,254}"
number_reguex = "^[0-9,.$]{2,}$"
phone_reguex = "(^3[0-9]{9,9}$)|(^5[0-9]{11,11}$)"
address_reguex = "^[A-Za-z0-9#\u00f1\u00d1 -]{3,40}$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid


def isUserValid(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False


def isUsernameValid(username):
    if re.search(username_reguex, username):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False


def isPhoneValid(phone):
    if re.search(phone_reguex, phone):
        return True
    else:
        return False


def isAddressValid(address):
    if re.search(address_reguex, address):
        return True
    else:
        return False


def isTextValid(text):
    if re.search(text_reguex, text):
        return True
    else:
        return False


def isNumberValid(number):
    if re.search(number_reguex, number):
        return True
    else:
        return False

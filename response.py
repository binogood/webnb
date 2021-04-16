class ApiException(Exception):
    def __init__(self, code, error_message, result=None):
        self.result = result
        self.code = code
        self.error_message = error_message

#SUCCESS MESSAGE
USER_CREATED = "success create user"


#FAILED MESSAGE

## USER CREATE FAILED MESSAGE
INVALID_INPUT_FIRST_NAME = "INVALID_INPUT_FIRST_NAME"
INVALID_INPUT_LAST_NAME = "INVALID_INPUT_LAST_NAME"
INVALID_INPUT_PASSWORD = "INVALID_INPUT_PASSWORD"
INVALID_INPUT_DATE_OF_BIRTH = "INVALID_INPUT_DATE_OF_BIRTH"
INVALID_INPUT_PHONE_NUMBER = "INVALID_INPUT_PHONE_NUMBER"
INVALID_INPUT_EMAIL = "INVALID_INPUT_EMAIL"
DUPLICATED_EMAIL = "DUPLICATED_EMAIL"
USER_NOT_FOUND = "USER_NOT_FOUND"  
PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
INVALID_INPUT_START_DATE = "INVALID_INPUT_START_DATE"
INVALID_INPUT_END_DATE = "INVALID_INPUT_END_DATE"

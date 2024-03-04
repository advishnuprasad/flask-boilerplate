class UnauthorizedException(Exception):
    """
    Authentication Failed (401) Exception
    """

    def __init__(self, **kwargs):
        self.messages = {"_entity": ["Please login to continue!"]}
        super().__init__(**kwargs)


class ForbiddenException(Exception):
    """
    Forbidden (403) Exception
    """

    def __init__(self, **kwargs):
        self.messages = {"_entity": ["Access Denied!"]}
        super().__init__(**kwargs)


class JWTBackendException(Exception):
    """
    Base except which all flask_jwt_extended errors extend
    """


class JWTDecodeError(JWTBackendException):
    """
    An error decoding a JWT
    """


class CSRFError(JWTBackendException):
    """
    An error with CSRF protection
    """


class InvalidFileError(Exception):
    """
    An error thrown on encountering malformed files
    """

    def __init__(self, messages, **kwargs):
        self.messages = messages
        super().__init__(**kwargs)


class EmailNotVerifiedError(Exception):
    """
    An error thrown when user tries to login without authentication
    """

    def __init__(self, **kwargs):
        self.messages = {"_entity": ["Please verify email to login!"]}
        super().__init__(**kwargs)

"""This module defines password handler"""

import re

from marshmallow import ValidationError

REGEX_MAPPINGS = {
    "upper_case": ".*[A-Z].*",
    "lower_case": ".*[a-z].*",
    "digit": ".*[0-9].*",
}


class PasswordHandler:
    """This module defines limitations for the password"""

    def __init__(self, config):
        self.config = config

    def validate(self, password):
        """This method validates password strength"""
        try:
            if self.is_password_strong(password) and self.validate_if_blacklisted(
                password
            ):
                return True, ""
        except Exception as error:
            return False, error.messages

    def validate_if_blacklisted(self, password):
        """Validate if the password is blacklisted"""
        if password in self.config.get("blacklist"):
            raise ValidationError("Avoid using common passwords")

        return True

    def is_password_strong(self, password):
        """Validate if strong password"""
        constrains = ["upper_case", "lower_case", "digit"]
        generic_message = "Password should contain" + ",".join(
            [
                " 1 {}".format(m.replace("_", " "))
                for m in constrains
                if self.config.get(m)
            ]
        )

        generic_message += " and length should be from {} to {}".format(
            self.config.get("min_length"), self.config.get("max_length")
        )

        if (
            not self.config.get("min_length")
            <= len(password)
            <= self.config.get("max_length")
        ):
            raise ValidationError(generic_message)
        elif self.config.get("upper_case") and not bool(
            re.match(REGEX_MAPPINGS["upper_case"], password)
        ):
            raise ValidationError(generic_message)
        elif self.config.get("lower_case") and not bool(
            re.match(REGEX_MAPPINGS["lower_case"], password)
        ):
            raise ValidationError(generic_message)
        elif self.config.get("digit") and not bool(
            re.match(REGEX_MAPPINGS["digit"], password)
        ):
            raise ValidationError(generic_message)

        return True

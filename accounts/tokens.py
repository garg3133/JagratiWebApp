from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
            + six.text_type((user.is_active is True))
            + six.text_type((user.auth is True))

            # Wasn't working correctly in cpanel because in activation func
            # user.is_active and all other booleans somehow becomes null (or None)
            # and thus the token don't match with is_active False at one place and 
            # None at other

        )
        # return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = TokenGenerator()
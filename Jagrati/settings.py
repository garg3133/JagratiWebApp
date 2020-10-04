
from decouple import config

# Import Production/Development settings
IN_PROD = (config("PRODUCTION") == 'True')

if IN_PROD:
    from .prod_settings import *
else:
    from .dev_settings import *
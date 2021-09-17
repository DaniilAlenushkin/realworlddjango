import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_base import *

DEBUG = False

django_heroku.settings(locals())

sentry_sdk.init(
    dsn=env('dsn'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

)

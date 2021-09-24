import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_base import *

DEBUG = False

django_heroku.settings(locals())

sentry_sdk.init(
    dsn=env('dsn'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

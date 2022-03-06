from django.conf import settings as dj_settings

from iamheadless_translate.conf import settings as iamheadless_translate_settings

from .apps import IamheadlessPublisherSiteSearchConfig as AppConfig
from .translations import translations


class Settings:

    APP_NAME = AppConfig.name
    VAR_PREFIX = APP_NAME.upper()

    URLNAME_SEARCH = 'search'

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()


iamheadless_translate_settings.TRANSLATION_REGISTRY.bulk_register(translations)

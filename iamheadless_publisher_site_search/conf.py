from django.conf import settings as dj_settings

from iamheadless_translate.conf import settings as iamheadless_translate_settings

from .apps import IamheadlessPublisherSiteSearchConfig as AppConfig
from .translations import translations


class Settings:

    APP_NAME = AppConfig.name
    VAR_PREFIX = APP_NAME.upper()

    VAR_TEMPLATE = f'{VAR_PREFIX}_TEMPLATE'
    URLNAME_SEARCH = 'search'

    @property
    def TEMPLATE(self):
        return getattr(
            dj_settings,
            self.VAR_TEMPLATE,
            f'{self.APP_NAME}/search.html'
        )

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()


iamheadless_translate_settings.TRANSLATION_REGISTRY.bulk_register(translations)

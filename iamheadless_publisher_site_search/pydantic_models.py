from typing import List, Optional

from django.shortcuts import reverse

from iamheadless_publisher_site.pydantic_models import BaseItemContentsPydanticModel, BaseItemDataPydanticModel, BaseItemPydanticModel

from .conf import settings
from .urls import urlpatterns


class SearchPageContentPydanticModel(BaseItemContentsPydanticModel):
    title: str
    slug: str
    language: str
    content: Optional[str]
    seo_keywords: Optional[str]
    seo_description: Optional[str]


class SearchPageDataPydanticModel(BaseItemDataPydanticModel):
    contents: List[SearchPageContentPydanticModel]


class SearchPagePydanticModel(BaseItemPydanticModel):
    _content_model = SearchPageContentPydanticModel
    _data_model = SearchPageDataPydanticModel
    _display_name_plural = 'search_pages'
    _display_name_singular = 'search_page'
    _item_type = 'site_search_page'
    _searchable = False
    _browsable = True
    _urlpatterns = urlpatterns

    data: SearchPageDataPydanticModel

    def get_item_url(self, language):
        return reverse(
            settings.URLNAME_SEARCH,
            kwargs={
                'language': language
            }
        )

    @property
    def CONTENTS(self):
        return self.dict()['data']['contents']

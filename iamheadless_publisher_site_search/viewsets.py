import re

from django.shortcuts import reverse

from iamheadless_publisher_site import utils as iamheadless_publisher_site_utils
from iamheadless_publisher_site.conf import settings as iamheadless_publisher_site_settings
from iamheadless_publisher_site.viewsets.items import ItemsViewSet
from iamheadless_translate.translations import translate

from .conf import settings


class SearchViewSet(ItemsViewSet):

    count = 10
    template = settings.TEMPLATE

    def get_context(self):

        language = iamheadless_publisher_site_utils.get_request_language(self.request)
        languages = iamheadless_publisher_site_settings.LANGUAGES

        context = super().get_context()
        context['page']['title'] = translate('search', language)

        language_links = []
        for x in languages:
            language = x[0]
            language_links.append({
                'display_name': x[1],
                'url': reverse(settings.URLNAME_SEARCH, kwargs={'language': language}),
                'language': language,
            })

        context['language_links'] = language_links

        return context

    def get_browsable_item_types(self):

        types = []
        registered_types = iamheadless_publisher_site_settings.ITEM_TYPE_REGISTRY.item_types

        for x in registered_types.keys():
            if registered_types[x]._searchable is True:
                types.append(registered_types[x]._item_type)

        return types

    def get_previous_url(self, pages=1):

        page = self.get_page()
        url = self.request.build_absolute_uri()

        if page == 1:
            return None

        if page > 1:
            previous_page = page - 1
            replace_with = f'page={previous_page}'
            return re.sub(r'page\=[\d]+', replace_with, url)

        return None

    def get_next_url(self, pages=1):

        page = self.get_page()
        url = self.request.build_absolute_uri()

        if page == pages:
            return None

        if page < pages:
            next_page = page + 1
            replace_with = f'page={next_page}'
            if 'page=' in url:
                return re.sub(r'page\=[\d]+', replace_with, url)
            else:
                if '?' in url:
                    url = url + '&' + replace_with
                else:
                    url = url + '?' + replace_with
                return url

        return None

    def get_items(self):

        params = getattr(self.request, self.request.method, {})
        browsable_item_types = self.get_browsable_item_types()

        kwargs = {
            'published': True,
            'count': self.count,
            'page': self.get_page(),
        }

        if len(browsable_item_types) != 0:
            kwargs['item_type'] = browsable_item_types

        q = params.get('q', None)
        if q is not None:
            q = q.strip()
            if q != '':
                kwargs['index_filters'] = [
                    f'text_lookup_indexes__field_name||title||icontains__{q}'
                ]

        items = self.client.retrieve_items(
            self.project_id,
            **kwargs,
        )

        return {
            'results': items['results'],
            'page': items['page'],
            'pages': items['pages'],
            'total': items['total'],
        }

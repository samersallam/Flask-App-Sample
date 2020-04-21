

class SiteMap:
    # Base url
    base_url = '/v1/'

    # Site map
    site_map_dict = \
        {
            # Template
            'item': '{}/',
            'collection': '{}/page',
        }

    @classmethod
    def get_endpoint_url(cls, name_space, required_endpoint):
        template = cls.site_map_dict[required_endpoint]

        endpoint_url = template.format(name_space)

        return '{}{}'.format(cls.base_url, endpoint_url)
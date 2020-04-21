
page_model = {
            'current_page': int,  # Nullable
            'num_records': int,
            'page_records': list,
            'per_page': int  # Nullable
        }


class PageAssert:

    @staticmethod
    def assert_response_paginated_data(page_model, paginated_data, is_paginated):
        PageAssert.assert_paginated_data_keys(page_model, paginated_data)
        PageAssert.assert_paginated_data_values_types(page_model, paginated_data, is_paginated)

    @staticmethod
    def assert_paginated_data_keys(page_model, paginated_data):
        assert len(paginated_data) == len(page_model)

        for key in page_model:
            assert key in paginated_data

    @staticmethod
    def assert_paginated_data_values_types(page_model, paginated_data, is_paginated):
        # Num_num_records
        assert isinstance(paginated_data['num_records'], page_model['num_records'])
        assert paginated_data['num_records'] >= 0

        # page_records
        assert isinstance(paginated_data['page_records'], page_model['page_records'])

        if is_paginated:
            # current_page
            assert isinstance(paginated_data['current_page'], page_model['current_page'])
            assert paginated_data['current_page'] > 0

            # per_page
            assert isinstance(paginated_data['per_page'], page_model['per_page'])
            assert paginated_data['per_page'] > 0

        else:
            assert paginated_data['current_page'] is None
            assert paginated_data['per_page'] is None










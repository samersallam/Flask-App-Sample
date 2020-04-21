class GeneralAssert:

    @staticmethod
    def assert_query_status(response_body):
        assert 'status_code' in response_body
        assert 'data' in response_body
        assert 'message' in response_body

    @staticmethod
    def assert_status_code(response, status):
        print('\n******\nstatus code: ', response.json['status_code'], '\nmessage: ', response.json['message'])
        assert response.json['status_code'] == status.code




class EntityAssert:

    @staticmethod
    def assert_response_entity_object(entity_model, original_entity_object, response_entity_object):
        """
        response: the end-point response
        entity_model: has the model fields names and data types
        original_entity_object: has the data that has been sent via the endpoint
        response_entity_object: has the response data
        """
        assert len(response_entity_object) == len(entity_model)
        for key in entity_model:
            assert key in response_entity_object
            assert isinstance(response_entity_object[key], entity_model[key])
            assert response_entity_object[key] == original_entity_object[key]

    def assret_count_of_responce (count):
        assert count == 0


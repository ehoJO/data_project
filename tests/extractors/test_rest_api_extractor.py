from unittest.mock import patch

from src.extractors import RestAPIExtractor
import pytest


@patch('src.extractors.rest_api_extractor.RestAPIExtractor.__init__')
def test_get_entities_raises_exception_without_params(restapi_extractor_mock, prepare_something):
    # Arrange
    restapi_extractor_mock.return_value = None
    rest_api_extractor = RestAPIExtractor()
    inserted_params = {}

    # Assert
    with pytest.raises(TypeError):
        # Act
        rest_api_extractor.get_entities(**inserted_params)

    # assert entities_result is not None
    # assert entities_result == []

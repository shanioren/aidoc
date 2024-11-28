import pytest
from unittest.mock import patch, Mock
from my_module import fetch_data

def test_fetch_data_success():
    """Test fetch_data function with a successful response."""
    # Create a mock response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    # Patch the requests.get method
    with patch("my_module.requests.get", return_value=mock_response) as mock_get:
        result = fetch_data("http://example.com")

        # Assert the fetch_data function works as expected
        assert result == {"key": "value"}
        mock_get.assert_called_once_with("http://example.com")


def test_fetch_data_failure():
    """Test fetch_data function with a failure response."""
    # Create a mock response object
    mock_response = Mock()
    mock_response.status_code = 404

    # Patch the requests.get method
    with patch("my_module.requests.get", return_value=mock_response):
        # Assert the function raises a ValueError for non-200 status codes
        with pytest.raises(ValueError, match="Error fetching data: 404"):
            fetch_data("http://example.com")

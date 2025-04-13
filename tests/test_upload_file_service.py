import pytest
from unittest.mock import MagicMock
from app.services.upload_file import UploadFileService

@pytest.fixture
def mock_cloudinary(mocker):
    # Mock the cloudinary uploader and CloudinaryImage
    mock_uploader = mocker.patch("cloudinary.uploader.upload")
    mock_image = mocker.patch("cloudinary.CloudinaryImage")
    return mock_uploader, mock_image

def test_upload_file(mock_cloudinary):
    mock_uploader, mock_image = mock_cloudinary

    # Mock the upload response
    mock_uploader.return_value = {"version": "12345"}
    mock_image.return_value.build_url.return_value = "http://example.com/image.jpg"

    # Create an instance of the service
    service = UploadFileService("cloud_name", "api_key", "api_secret")

    # Mock file object
    mock_file = MagicMock()
    mock_file.file = MagicMock()

    # Call the upload_file method
    url = service.upload_file(mock_file, "testuser")

    # Assertions
    mock_uploader.assert_called_once_with(mock_file.file, public_id="py_avatar/testuser", overwrite=True)
    mock_image.assert_called_once_with("py_avatar/testuser")
    assert url == "http://example.com/image.jpg"
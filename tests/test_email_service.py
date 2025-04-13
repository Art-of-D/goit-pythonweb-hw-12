import pytest
from unittest.mock import AsyncMock
from fastapi_mail import FastMail
from fastapi_mail.errors import ConnectionErrors
from app.services.email import send_email

@pytest.fixture
def mock_fastmail(mocker):
    mock_fastmail = mocker.patch("app.services.email.FastMail")
    mock_instance = mock_fastmail.return_value
    mock_instance.send_message = AsyncMock()
    return mock_instance

@pytest.mark.asyncio
async def test_send_email_success(mock_fastmail):
    await send_email(email="testuser@example.com", username="testuser", host="http://localhost")

    mock_fastmail.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_send_email_connection_error(mocker, capsys):
    mock_fastmail = mocker.patch("app.services.email.FastMail")
    mock_instance = mock_fastmail.return_value
    mock_instance.send_message = AsyncMock(side_effect=ConnectionErrors("Connection failed"))

    await send_email(email="testuser@example.com", username="testuser", host="http://localhost")

    captured = capsys.readouterr()

    assert "Connection failed" in captured.out

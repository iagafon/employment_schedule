from unittest.mock import Mock, patch
import pytest
import requests

from src.check_slot_service.check_slot_service import CheckSlotService


@pytest.fixture
def mock_schedule_data():
    return {
        "days": [
            {"id": 1, "date": "2025-08-11", "start": "09:00", "end": "18:00"},
            {"id": 2, "date": "2025-08-11", "start": "08:00", "end": "17:30"},
        ],
        "timeslots": [
            {"id": 2, "day_id": 1, "start": "11:00", "end": "12:00"},
            {"id": 3, "day_id": 2, "start": "09:30", "end": "15:00"},
        ],
    }


@pytest.fixture
def mock_response(mock_schedule_data):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_schedule_data
    return mock_resp


@pytest.fixture
def mock_error_response():
    mock_resp = Mock()
    mock_resp.status_code = 500
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )
    mock_resp.json.side_effect = ValueError("Invalid JSON")
    return mock_resp


@pytest.fixture
def check_slot_service(mock_response):
    with patch("requests.get", return_value=mock_response):
        return CheckSlotService(date="2025-08-11", start_time="15:30", end_time="17:00")

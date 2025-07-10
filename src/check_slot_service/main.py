"""
Точка входа
"""

from src.check_slot_service.check_slot_service import CheckSlotService

if __name__ == "__main__":
    mock_date = "2025-02-15"
    mock_time_start = "15:00"
    mock_time_end = "16:40"

    CheckSlotService(mock_date, mock_time_start, mock_time_end)

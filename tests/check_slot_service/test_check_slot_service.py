class TestCheckSlotService:
    def test_successful_init(self, check_slot_service):
        """Тест успешной инициализации сервиса"""
        assert check_slot_service._CheckSlotService__date == "2025-08-11"
        assert check_slot_service._CheckSlotService__start_time == "15:30"
        assert check_slot_service._CheckSlotService__end_time == "17:00"

    def test_available_slot_check(self, check_slot_service):
        """Тест проверки доступности слота"""

        assert (
            check_slot_service.schedule.is_time_available(
                "2025-08-11", "15:30", "17:00"
            )
            is True
        )

        assert (
            check_slot_service.schedule.is_time_available(
                "2025-08-11", "11:30", "12:30"
            )
            is False
        )

    def test_find_available_slot(self, check_slot_service):
        """Тест поиска доступного слота"""
        slot = check_slot_service.schedule.find_available_slot("2025-08-11", 90)
        assert slot is not None
        assert slot.duration_minutes() >= 90

    def test_non_working_day(self, check_slot_service):
        """Тест обработки нерабочего дня"""
        assert check_slot_service.schedule.get_busy_slots("2025-08-10") == []
        assert check_slot_service.schedule.get_free_slots("2025-08-10") == []
        assert (
            check_slot_service.schedule.is_time_available(
                "2024-08-10", "10:00", "11:00"
            )
            is False
        )

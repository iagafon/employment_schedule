from typing import Optional

from src.check_slot_service.dto.data_models import DayModel, TimeslotModel
from src.check_slot_service.time_slot import TimeSlot, WorkDay


class EmployeeSchedule:
    """Класс для работы с графиком сотрудника с использованием Pydantic моделей"""

    def __init__(self, data: dict):
        self.days: dict[str, WorkDay] = {}
        self._parse_data(data)

    def _parse_data(self, data: dict):
        """Парсит полученные данные с использованием Pydantic моделей"""
        # Валидация входных данных
        days_data = [DayModel(**day) for day in data["days"]]
        timeslots_data = [TimeslotModel(**slot) for slot in data["timeslots"]]

        # Создаем рабочие дни
        for day_data in days_data:
            try:
                work_day = WorkDay(
                    date=day_data.date, start_time=day_data.start, end_time=day_data.end
                )
                self.days[day_data.date] = work_day
            except ValueError as e:
                print(f"Ошибка создания рабочего дня {day_data.date}: {e}")
                continue

        # Добавляем занятые слоты
        for timeslot in timeslots_data:
            try:
                # Находим день по day_id (предполагаем соответствие порядку в списке)
                day_data = days_data[timeslot.day_id - 1]
                self.days[day_data.date].add_busy_slot(timeslot.start, timeslot.end)
            except (IndexError, KeyError, ValueError) as e:
                print(f"Ошибка добавления занятого слота {timeslot.id}: {e}")
                continue

    # Остальные методы остаются без изменений
    def get_day_schedule(self, date: str) -> Optional[WorkDay]:
        """Возвращает расписание для указанной даты"""
        return self.days.get(date)

    def get_busy_slots(self, date: str) -> list[TimeSlot]:
        """Возвращает занятые промежутки для указанной даты"""
        day = self.get_day_schedule(date)
        if not day:
            return []
        return day.get_busy_slots()

    def get_free_slots(self, date: str) -> list[TimeSlot]:
        """Возвращает свободные промежутки для указанной даты"""
        day = self.get_day_schedule(date)
        if not day:
            return []
        return day.get_free_slots()

    def is_time_available(self, date: str, start: str, end: str) -> bool:
        """Проверяет, доступен ли промежуток времени в указанную дату"""
        day = self.get_day_schedule(date)
        if not day:
            return False
        return day.is_time_available(start, end)

    def find_available_slot(
        self, date: str, duration_minutes: int
    ) -> Optional[TimeSlot]:
        """Находит свободный промежуток указанной продолжительности в заданную дату"""
        day = self.get_day_schedule(date)
        if not day:
            return None
        return day.find_available_slot(duration_minutes)

from typing import Optional

from src.check_slot_service.dto.parse_time import ParseTime, ParseDateTime


class TimeSlot(ParseTime):
    """Класс для представления временного промежутка с валидацией через Pydantic"""

    def __init__(self, **data):
        super().__init__(**data)
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")

    def __contains__(self, other: "TimeSlot") -> bool:
        """Проверяет, содержится ли другой TimeSlot полностью в текущем"""
        return self.start_time <= other.start_time and self.end_time >= other.end_time

    def overlaps(self, other: "TimeSlot") -> bool:
        """Проверяет, пересекаются ли два TimeSlot"""
        return not (
            self.end_time <= other.start_time or self.start_time >= other.end_time
        )

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

    def duration_minutes(self) -> int:
        """Возвращает продолжительность в минутах"""
        return (self.end_time.hour * 60 + self.end_time.minute) - (
            self.start_time.hour * 60 + self.start_time.minute
        )


class WorkDay(ParseDateTime):
    """Класс для представления рабочего дня с валидацией через Pydantic"""

    busy_slots: list[TimeSlot] = []

    def add_busy_slot(self, start: str, end: str):
        """Добавляет занятый промежуток времени"""
        slot = TimeSlot(start_time=start, end_time=end)
        if slot not in TimeSlot(start_time=self.start_time, end_time=self.end_time):
            raise ValueError(f"Time slot {slot} is outside of working hours")
        self.busy_slots.append(slot)

    def get_busy_slots(self) -> list[TimeSlot]:
        """Возвращает список занятых промежутков"""
        return sorted(self.busy_slots, key=lambda x: x.start_time)

    def get_free_slots(self) -> list[TimeSlot]:
        """Возвращает список свободных промежутков"""
        if not self.busy_slots:
            return [TimeSlot(start_time=self.start_time, end_time=self.end_time)]

        free_slots = []
        busy_slots = self.get_busy_slots()

        # Проверяем время до первого занятого слота
        first_busy = busy_slots[0]
        if self.start_time < first_busy.start_time:
            free_slots.append(
                TimeSlot(start_time=self.start_time, end_time=first_busy.start_time)
            )

        # Проверяем промежутки между занятыми слотами
        for i in range(1, len(busy_slots)):
            prev_end = busy_slots[i - 1].end_time
            curr_start = busy_slots[i].start_time
            if prev_end < curr_start:
                free_slots.append(TimeSlot(start_time=prev_end, end_time=curr_start))

        # Проверяем время после последнего занятого слота
        last_busy = busy_slots[-1]
        if last_busy.end_time < self.end_time:
            free_slots.append(
                TimeSlot(start_time=last_busy.end_time, end_time=self.end_time)
            )

        return free_slots

    def is_time_available(self, start: str, end: str) -> bool:
        """Проверяет, доступен ли указанный промежуток времени"""
        try:
            test_slot = TimeSlot(start_time=start, end_time=end)
        except ValueError:
            return False

        work_slot = TimeSlot(start_time=self.start_time, end_time=self.end_time)
        if test_slot not in work_slot:
            return False

        for busy_slot in self.busy_slots:
            if test_slot.overlaps(busy_slot):
                return False
        return True

    def find_available_slot(self, duration_minutes: int) -> Optional[TimeSlot]:
        """Находит свободный промежуток указанной продолжительности"""
        for free_slot in self.get_free_slots():
            if free_slot.duration_minutes() >= duration_minutes:
                return free_slot
        return None

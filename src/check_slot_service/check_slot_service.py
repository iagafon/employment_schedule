"""
Логика проверки свободных слотов
"""

import requests

from src.check_slot_service.schedule import EmployeeSchedule


class CheckSlotService:
    """
    Основной класс проверки слотов
    """

    __api_url: str = "https://ofc-test-01.tspb.su/test-task/"

    __date = str
    __start_time = str
    __end_time = str

    def __init__(self, date: str, start_time: str, end_time: str):
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
        schedule_data = self.get_schedule_data()
        self.schedule = EmployeeSchedule(schedule_data)
        self.check_slot()

    def get_schedule_data(self):
        """Загружает данные с API"""
        try:
            response = requests.get(self.__api_url)
            print(f">>> response: {response}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch data from API: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")

    def check_slot(self):
        try:
            print(f"Занятые промежутки на {self.__date}:")
            for slot in self.schedule.get_busy_slots(self.__date):
                print(slot)

            print(f"\nСвободные промежутки на {self.__date}:")
            for slot in self.schedule.get_free_slots(self.__date):
                print(slot)

            print(
                f"\nДоступен ли промежуток {self.__start_time}-{self.__end_time} на {self.__date}?"
            )
            print(
                self.schedule.is_time_available(
                    self.__date, self.__start_time, self.__end_time
                )
            )

            duration = 120  # минуты
            print(
                f"\nНайдем свободный промежуток на {self.__date} продолжительностью {duration} минут:"
            )
            available_slot = self.schedule.find_available_slot(self.__date, duration)
            print(available_slot if available_slot else "Нет доступных промежутков")
        except Exception as e:
            print(f"Ошибка: {e}")

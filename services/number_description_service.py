import phonenumbers
from services.neberitrubku.number_loader import NumberLoader


class NumberDescriptionService:
    def __init__(self):
        self._loader = NumberLoader()

    def describe(self, number: str, trace_id: str):
        num_obj = phonenumbers.parse(number, region="RU")
        num_str = f"8{num_obj.national_number}"

        return self._loader.load(num_str, trace_id)

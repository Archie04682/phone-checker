import phonenumbers


class NumberNormalizeService:
    @staticmethod
    def normalize(number: str) -> str:
        num_obj = phonenumbers.parse(number, region="RU")
        return f"{num_obj.country_code}{num_obj.national_number}"

    @staticmethod
    def prettify(number: str) -> str:
        num_obj = phonenumbers.parse(number, region="RU")
        return f"+{num_obj.country_code} {num_obj.national_number}"

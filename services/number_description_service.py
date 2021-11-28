from adapters.phone_data_source import PhoneDataSource


class NumberDescriptionService:
    def __init__(self, phone_data_sources: [PhoneDataSource]):
        self._phone_data_sources = phone_data_sources

    def describe(self, number: str):
        # TODO: Organize merging of different data_sources' results
        # For now we have only 1 source  so no need to merge:
        return self._phone_data_sources[0].get_phone_info(number)

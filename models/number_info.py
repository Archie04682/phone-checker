class NumberInfo:
    def __init__(
            self,
            digits: str,
            meta_info: [],
            ratings: {},
            categories: {},
            description: str):

        # root: div.mainInfo
        self.digits = digits  # div.mainInfoHeader div.number
        self.meta_info = meta_info  # div.mainInfoHeader div.number span []
        self.ratings = ratings  # div.description div.ratings li {count, desc} (split by 'x ')
        self.categories = categories  # div.description div.categories li {count, desc} (split by 'x ')
        self.description = description  # div.description div.advanced div

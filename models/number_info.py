# root: div.mainInfo
#   digits: div.mainInfoHeader div.number
#   meta_info: div.mainInfoHeader div.number span []
#   categories: div.description div.ratings li {count, desc} (split by 'x ')
#   description: div.description div.advanced div


class NumberInfo:
    def __init__(
            self,
            digits: str,
            meta_info: [],
            ratings: {},
            categories: {},
            description: str):

        self.digits = digits
        self.meta_info = meta_info
        self.ratings = ratings
        self.categories = categories
        self.description = description

    def as_dict(self):
        return {
            "digits": self.digits,
            "meta_info": self.meta_info,
            "ratings": self.ratings,
            "categories": self.categories,
            "description": self.description
        }

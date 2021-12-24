# root: div.mainInfo
#   digits: div.mainInfoHeader div.number
#   meta_info: div.mainInfoHeader div.number span []
#   categories: div.description div.ratings li {count, desc} (split by 'x ')
#   description: div.description div.advanced div


class _Fields:
    digits = "digits"
    meta_info = "meta_info"
    ratings = "ratings"
    categories = "categories"
    description = "description"


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
            _Fields.digits: self.digits,
            _Fields.meta_info: self.meta_info,
            _Fields.ratings: self.ratings,
            _Fields.categories: self.categories,
            _Fields.description: self.description
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return NumberInfo(
            digits=dictionary[_Fields.digits],
            meta_info=dictionary[_Fields.meta_info],
            ratings=dictionary[_Fields.ratings],
            categories=dictionary[_Fields.categories],
            description=dictionary[_Fields.description]
        )

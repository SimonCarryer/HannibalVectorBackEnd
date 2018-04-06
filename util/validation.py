from cerberus import Validator


class MovieInputValidator:
    def __init__(self, valid_ids):
        schema = {'movie_imdb_1': {'type': 'string', 'required': True, 'allowed': valid_ids},
          'movie_imdb_2': {'type': 'string', 'required': True, 'allowed': valid_ids}
            }
        self.validator = Validator(schema)

    def validate(self, request):
        return self.validator.validate(request.args)

    def errors(self):
        return self.validator.errors


class SearchInputValidator:
    def __init__(self):
        schema = {'query': {'type': 'string', 'required': True}
            }
        self.validator = Validator(schema)

    def validate(self, request):
        return self.validator.validate(request.args)

    def errors(self):
        return self.validator.errors


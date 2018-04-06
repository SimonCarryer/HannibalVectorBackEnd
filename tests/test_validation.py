from util.validation import MovieInputValidator

class MockRequest:
    def __init__(self, args):
        self.args = args


def test_validate_returns_true_for_valid_request():
    validator = MovieInputValidator(['tt0241527', 'tt0330373'])
    request = MockRequest({'movie_imdb_1': 'tt0241527', 'movie_imdb_2': 'tt0330373'})
    assert validator.validate(request)

def test_validate_returns_false_for_missing_values():
    validator = MovieInputValidator(['tt0241527', 'tt0330373'])
    request = MockRequest({'movie_imdb_1': 'tt0241527'})
    assert not validator.validate(request)

def test_validate_returns_false_for_movie_not_in_list():
    validator = MovieInputValidator(['tt0241527', 'tt0330373'])
    request = MockRequest({'movie_imdb_1': 'abc', 'movie_imdb_2': 'xyz'})
    assert not validator.validate(request)

def test_validator_stores_errors():
    validator = MovieInputValidator(['tt0241527', 'tt0330373'])
    request = MockRequest({'movie_imdb_1': 'abc', 'movie_imdb_2': 'xyz'})
    validator.validate(request)
    print(validator.validator.errors)
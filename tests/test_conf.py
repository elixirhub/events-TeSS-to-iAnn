LOG_FILE = '/Users/federico/logs/tess2iann_test.log'
TESS_URL = 'http://tess.elixir-uk.org/events.json'
IANN_URL = 'http://localhost:5000'
IANN_NULL_VALUE = 'null'
MAPPER = {
    'title': 'name',
    'start': 'start_date',
    'url': 'website',
    'end': 'end_date',
    'venue': 'location',
    'organizer': 'host',
    'country': 'country',
    'description': 'description'
}

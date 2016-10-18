import os

LOG_FILE = os.environ.get('TESS_TO_IANN_LOG') or '/Users/federico/logs/tess2iann.log'
TESS_URL = os.environ.get('TESS_URL') or 'http://tess.elixir-uk.org/events.json'
IANN_URL = os.environ.get('IANN_URL') or 'http://localhost:5000'
IANN_NULL_VALUE = os.environ.get('IANN_NULL') or 'null'
TESS_TO_IANN_MAPPER = {
    'title': 'name_event',
    'start': 'start_date',
    'url': 'website',
    'end': 'end_date',
    'venue': 'location',
    'organizer': 'host',
    'country': 'country',
    'description': 'description'
}

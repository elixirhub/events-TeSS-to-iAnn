import tess_to_iann
from mock import patch
import test_conf as conf


def test_empty_entry():
    empty_dict = tess_to_iann.map_tess_to_iann()
    assert not empty_dict


def test_none_entry():
    empty_dict = tess_to_iann.map_tess_to_iann(None)
    assert not empty_dict


def test_some_entry():
    with patch('tess_to_iann.conf', new=conf):
        description = 'This course will provide an introduction to next generation sequencing (NGS) platforms'
        test_entry = dict(title='Hi there!', start='2016-10-20T09:00:00.000Z', end='2016-10-19T10:30:00.000Z',
                          url='https://www.statslife.org.uk/events/eventdetail/751/12/applying-for-certification',
                          venue='The Royal Statistical Society', organizer='University of Leicester',
                          country='United Kingdom', description=description)
        test_output = dict(name='Hi there!', start_date='2016-10-20T09:00:00.000Z', end_date='2016-10-19T10:30:00.000Z',
                           website='https://www.statslife.org.uk/events/eventdetail/751/12/applying-for-certification',
                           location='The Royal Statistical Society', host='University of Leicester',
                           country='United Kingdom', description=description)
        assert tess_to_iann.map_tess_to_iann(test_entry) == test_output

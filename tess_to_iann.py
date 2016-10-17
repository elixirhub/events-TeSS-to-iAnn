"""
TeSS to iAnn events sync v 0.0

This module aims to provide a schedulable process to make automatic sync
from TeSS to iAnn event registry.
"""
from dateutil.parser import parse
from pytz import UTC as utc
from datetime import datetime
import pysolr
import urllib2
import json
from docs import conf
import logging
import daemon
import time
import click


def init():
    logging.basicConfig(filename=conf.LOG_FILE, level=logging.INFO,
                        format='%(levelname)s[%(asctime)s]: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a')


def map_tess_to_iann(tess_event=None):
    """
    Map an TeSS event to a iAnn event
    :param tess_event: dictionary that represents an event in TeSS
    :return: dictionary that represents an event in iAnn
    """
    iann_event = dict()
    if not tess_event:
        return iann_event
    for key, value in conf.TESS_TO_IANN_MAPPER.iteritems():
        iann_event[value] = conf.IANN_NULL_VALUE if not tess_event[key] else tess_event[key]
    return iann_event


def get_tess_page_events(page=1, start_dt=None, end_dt=None):
    """
    Gets the events data for a given TeSS results page
    :param page: the number of the page corresponding to the result set pagination (default 1)
    :param start_dt:
    :param end_dt:
    :return: all the events retrieved for the page
    """
    start_dt = start_dt or utc.localize(parse("2000-01-01"))
    end_dt = end_dt or utc.localize(datetime.now())
    # Generate the URL to make the query
    query_url = conf.TESS_URL + '?' + 'page=%d' % page
    # Execute the HTTP query
    page_data = urllib2.urlopen(query_url)
    # Load the JSON data into a Python dict
    tess_events = json.load(page_data)

    # Iterate over the result set and map the TeSS events fields to iAnn events fields
    iann_events = [map_tess_to_iann(tess_event) for tess_event in tess_events
                   if start_dt < parse(tess_event['updated_at']) < end_dt]
    return iann_events


def get_tess_all_events(start_dt=None, end_dt=None):
    """
    Retrieves all the data available from TeSS
    :return: all the events available from TeSS
    """
    page = 1
    data = []
    logging.info("Starting harvesting of TeSS events data")
    # Repeat the data gathering for every possible page until there is no results
    while True:
        logging.info("Retrieving TeSS data for page # %d" % page)
        page_results = get_tess_page_events(page, start_dt, end_dt)
        if not page_results:
            logging.info("Finishing harvesting")
            logging.info('/**********************************/')
            break
        data.append(page_results)
        page += 1
    return data


def push_to_iann(docs):
    """
    Adds data to Iann Solr from a Solr data structure
    :param docs: a list of dictionaries containing Solr docs
    """
    # Instantiates Solr service
    solr = pysolr.Solr(conf.IANN_URL, timeout=10)
    # Add Solr documents to service
    solr.add(
        docs
    )


@click.command()
@click.option('--delay', default=60, help='Seconds between executions')
@click.option('--log', default=conf.LOG_FILE, help='Log file path, if not defined will use the one on the conf.py')
@click.option('--tess_url', default=conf.TESS_URL, help='TeSS service URL, if not defined will use the one on conf.py')
@click.option('--iann_url', default=conf.IANN_URL, help='iAnn Solr URL, if not defined will use the one on conf.py')
def run(delay, log, tess_url, iann_url):
    conf.LOG_FILE = log
    conf.TESS_URL = tess_url
    conf.IANN_URL = iann_url
    click.secho('Fetching events from TeSS every %d seconds' % delay, fg='red', bold=True)
    with daemon.DaemonContext():
        init()
        while True:
            get_tess_all_events()
            time.sleep(delay)


#if __name__ == "__main__":
#    run()
init()
get_tess_all_events()


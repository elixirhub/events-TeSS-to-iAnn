"""
TeSS to iAnn events sync v 0.0

This module aims to provide a schedulable process to make automatic sync
from TeSS to iAnn event registry.
"""
from dateutil.parser import parse
from pytz import UTC as utc
from datetime import datetime, timedelta
import pysolr
import urllib2
import json
from docs import conf
import logging
import daemon
import time
import click
import os
import sys


WELCOME_MSJ = 'ELIXIR TeSS to iAnn events synchronizer script V 0.0'


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
    for tess_field, iann_field in conf.TESS_TO_IANN_MAPPER.iteritems():
        if tess_event[tess_field]:
            iann_event[iann_field] = tess_event[tess_field]
    return iann_event


def get_tess_events_from_url(query_url):
    """
    Gets the events data for a given TeSS query URL
    :param query_url: query url
    :return: all the events retrieved for the page
    """
    # Execute the HTTP query
    logging.info("Query to TeSS web service: " + query_url)
    page_data = urllib2.urlopen(query_url)
    # Load the JSON data into a Python dict
    tess_events = json.load(page_data)
    return tess_events


def get_tess_all_events(start_dt=None, expired=False):
    """
    Retrieves all the data available from TeSS
    :param start_dt: date to start harversting events
    :param expired: flag to indicate if expired events must be fetched
    :return: all the events available from TeSS
    """
    page = 1
    tess_events = []
    end_dt = utc.localize(datetime.now())
    start_dt = start_dt or utc.localize(parse('2000-01-01'))
    logging.info('Starting harvesting of TeSS events data from ' + str(start_dt) + ' to ' + str(end_dt))
    # Repeat the data gathering for every possible page until there is no results
    while True:
        logging.info('Retrieving TeSS data for page # %d' % page)
        # Generate the URL to make the query
        query_url = conf.TESS_URL + '?' + 'page=%d' % page
        if expired:
            query_url += '&include_expired=true'
        page_results = get_tess_events_from_url(query_url)
        if not page_results:
            logging.info('Finishing harvesting')
            break
        tess_events += page_results
        page += 1
    logging.info('Performing conversion from TeSS events to iAnn events')
    # Iterate over the result set and map the TeSS events fields to iAnn events fields
    iann_events = [map_tess_to_iann(tess_event) for tess_event in tess_events
                   if start_dt < parse(tess_event['updated_at']) < end_dt]
    logging.info('Conversion done! %d updated events retrieved and converted' % len(iann_events))
    logging.info('/****************************************/')
    return dict(start=start_dt, end=end_dt, events=iann_events)


def push_to_iann(events):
    """
    Adds data to iAnn Solr from a Solr data structure
    :param events: list of events to be pushed to iAnn Solr
    """
    # Instantiates Solr service
    solr = pysolr.Solr(conf.IANN_URL, timeout=10)
    # Add Solr documents to service
    solr.add(events)


@click.command()
@click.option('--delay', default=10, help='Seconds between executions when the script is run as a daemon (eg. 60)')
@click.option('--log', default=conf.LOG_FILE, help='Log file path, if not defined will use the one on the conf.py')
@click.option('--tess_url', default=conf.TESS_URL, help='TeSS service URL, if not defined will use the one on conf.py')
@click.option('--iann_url', default=conf.IANN_URL, help='iAnn Solr URL, if not defined will use the one on conf.py')
@click.option('--daemonize', is_flag=True, help='Flag to run the script as a daemon')
@click.option('--include_expired', is_flag=True, help='Flag to fetch expired events from TeSS')
@click.option('--start', default=None, help='Start date')
def run(delay, log, tess_url, iann_url, daemonize, start, include_expired):
    """
    ELIXIR TeSS to iAnn events synchronizer script V 0.0
    Script to get TeSS events and push them to iAnn. It can be used as a batch process or as a daemon process.
    """
    conf.LOG_FILE = log
    conf.TESS_URL = tess_url
    conf.IANN_URL = iann_url
    start = utc.localize(parse(start)) if  start  else utc.localize(parse('2000-01-01'))
    click.secho(WELCOME_MSJ, fg='yellow', bg='red', bold=True)
    if not daemonize:
        click.secho('Fetching events from TeSS', fg='blue', bold=True)
        init()
        get_tess_all_events(start)
        click.secho('Done!', fg='blue', bold=True)
        return
    click.secho('Fetching events from TeSS every %d seconds' % delay, fg='blue', bold=True)
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stdout):
        init()
        click.secho('Process ID: %d' % os.getpid(), fg='red', bold=True, blink=True)
        while True:
            results = get_tess_all_events(start, include_expired)
            push_to_iann(results['events'])
            start = results['end']
            time.sleep(delay)


if __name__ == "__main__":
    try:
        run()
    except AttributeError:
        print "Try 'python tess_to_iann.py --help' to get information about usage"


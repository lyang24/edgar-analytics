import logging
import datetime
import csv
import codecs
import os
import heapq

try:
    from contextlib import ContextDecorator
except ImportError:
    from contextdecorator import ContextDecorator

log = logging.getLogger(__name__)


def dump_list_to_file_as_line(data, useFilePath, delimiter):
    '''
    out put data to list with error handling
    :param data:
    :param useFilePath:
    :param delimiter:
    :return:
    '''
    if data:
        if os.path.exists(useFilePath) and os.path.isfile(useFilePath):
            fobj = codecs.open(useFilePath, 'ab')
        else:
            fobj = codecs.open(useFilePath, 'wb')
        with fobj:
            line = [str(lineitem).encode('utf-8') for lineitem in data]
            fobj.write(str.encode(delimiter).join(line) + b"\n")
    else:
        log.info('Empty Data Being Attempted To Be Written To File')


def get_inactivity_period(inactivityFilePath):
    try:
        if os.path.exists(inactivityFilePath) and os.path.isfile(inactivityFilePath):
            with open(inactivityFilePath, "r") as inactivityFile:
                timeout = int(inactivityFile.read())
                assert 1 <= timeout <= 86400
                return timeout
        else:
            raise OSError
    except Exception as e:
        logging.critical('Invaild inactivity file due to {}'.format(e.message))


def get_log_data(csv_fname):
    '''
    A generator for the data in log.csv. Since csv files can contain over 10
    millions of records, it is not necessary to store all the record in memory
    all at once.
    Input: csv_fname:
        filename/location of the csv.
    Output: log_record
    '''
    with open(csv_fname, "r") as log_records:
        for log_record in csv.reader(log_records, delimiter=','):
            yield log_record


def valiad_row(row):
    '''
    Helper function to check if each record has the missing information or not
    Input: row from readint the csv
    Output: True or False
    '''
    if len(row[0]) > 0 and len(row[1]) > 0 and len(row[2]) > 0 and len(row[4]) > 0 and len(row[5]) > 0 and len(
            row[6]) > 0:
        return True
    else:
        return False


def convert_datetime(date, time, format):
    """ creates a datetime object from given date and time
        Args:
            date: a string of date in %Y-%m-%d
            time: a string of time in
        Returns:
            A datetime obeject with the given date and time information
    """
    return datetime.datetime.strptime(date + " " + time, format)


def time_diff(dt1, dt2):
    """ calculates difference of time between two datetime objects in seconds
        Args:
            dt1: a datime object
            dt2: another datime object for comparison
        Returns:
            The difference of time between dt1 and dt2 in seconds
    """
    return abs(int((dt2 - dt1).total_seconds()))


class exec_time(ContextDecorator):
    """Usage: Simplified Execution Timing Decorator
    @exec_time()
    def func_to_be_timed(...):
        pass
    """

    def __enter__(self):
        self.start_time = datetime.datetime.now()
        return self

    def __exit__(self, log_name, *exc):
        end_time = datetime.datetime.now()
        log = logging.getLogger(log_name)
        log.info('this function completed in {} sec'.format(
            (end_time - self.start_time).total_seconds()))
        return False

class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()

    def add(self, d, pri):
        if not d in self.set:
            heapq.heappush(self.heap, (pri, d))
            self.set.add(d)

    def get(self):
        pri, d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d
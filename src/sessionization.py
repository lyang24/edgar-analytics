import logging
import os
import sys
import contextlib
from collections import OrderedDict
from argparse import ArgumentParser

from utils import dump_list_to_file_as_line, get_inactivity_period, \
    get_log_data, valiad_row, convert_datetime, time_diff, exec_time
from session import Session

log = logging.getLogger(__name__)

@exec_time()
def parse(args):
    '''
    take in log file row by row added to ordered dict.
    subtracted by ordered dict
    by if new session is identified, current max time - timeout > min time,
    and dump at the end of file
    :param args:
    :return: void write file to outputPath
    '''
    timeout = get_inactivity_period(args.inactivityFilePath)
    rows = iter(get_log_data(args.logFilePath))
    next(rows, None)  # skip the header
    ip_map = OrderedDict()
    unique_timestamp = set()

    with contextlib.suppress(FileNotFoundError):
        os.remove(args.outPath)

    for (i, row) in enumerate(rows):
        try:
            if valiad_row(row):
                fields = row
                init_time = convert_datetime(fields[1], fields[2], args.time_format)
                unique_timestamp.add(init_time)
                ip = fields[0]
                if ip in ip_map:
                    if time_diff(init_time, ip_map[ip].get_last_session_time()) > timeout:
                        dump_list_to_file_as_line(ip_map[ip].output_session(), args.outPath, args.delimiter)
                        ip_map[ip] = Session(ip, init_time)
                    else:
                        ip_map[ip].set_last_session_time(init_time)
                        ip_map[ip].increment_doc()
                else:
                    ip_map[ip] = Session(ip, init_time)

                if (len(unique_timestamp) - 1 > timeout):
                    exp_ips = [v.get_ip() for v in ip_map.values() if v.get_last_session_time() == min(unique_timestamp)]
                    for exp in exp_ips:
                        dump_list_to_file_as_line(ip_map.pop(exp).output_session(), args.outPath, args.delimiter)
                    unique_timestamp.remove(min(unique_timestamp))
            else:
                logging.warning('row {} has invalid data'.format(i))
        except Exception as e:
            logging.warning('row {} could not be processed because {}'.format(i, str(e)))

    for ip in ip_map.keys():
        dump_list_to_file_as_line(ip_map[ip].output_session(), args.outPath, args.delimiter)

    logging.info('Excution complete')


if __name__ == '__main__':
    parser = ArgumentParser(description='Process logs')
    parser.add_argument('--logFilePath', help='the location of the logs', required=True)
    parser.add_argument('--inactivityFilePath', help='the location of the inactivity file', required=True)
    parser.add_argument('--outPath', help='where do you want to output result', required=True)
    parser.add_argument('--time_format', help='the format of the time string', default='%Y-%m-%d %H:%M:%S')
    parser.add_argument('--delimiter', help='separator of output', default=',')
    args = parser.parse_args()
    parse(args)
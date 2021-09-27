import copy
import datetime
import logging
import requests
import time

# csv ony used in parallel mode with acre r-script
import csv
from util.util_csv import CsvException
from util.util_csv import extract_row_data_csv

from util.geo import latitude_longitude_to_pixel, pixel_to_latitude_longitude
from util.timestamp import LocalDate

from base.model import Entity

ARC2_HOST = 'localhost'
ARC2_PORT = 5000
ARC2_PATH = 'arc2/rainfall'
ARC2_TIMEOUT_S = 2

ARC2_URL_TEMPLATE = "http://{}:{}/{}"

# query param example: ?lat=-0.9&long=37.7&date=20200201&days=7"
ARC2_LATITUDE = "lat"
ARC2_LONGITUDE = "long"
ARC2_DATE = "date"
ARC2_DAYS = "days"

class Arc2(Entity):

    # TODO remove this once ftp downloaded arc2 data is considered master for policy-engine and actuarial purposes
    # switch to indicate if rainfall data is to be extracted from
    # pixel rainfall csv file provided by acre
    USE_CSV = False
    MONTH_TO_INT = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }


    def __init__(self, host=ARC2_HOST, port=ARC2_PORT, path=ARC2_PATH, timeout=ARC2_TIMEOUT_S):
        self['host'] = host
        self['port'] = int(port)
        self['url'] = ARC2_URL_TEMPLATE.format(host, int(port), path)
        self['timeout_s'] = ARC2_TIMEOUT_S


    def rainfall(self, pixel, date, days):

        if Arc2.USE_CSV:
            return self._rainfall_csv(pixel, date, days)
        
        request_params = {}
        (request_params[ARC2_LATITUDE], request_params[ARC2_LONGITUDE]) = pixel_to_latitude_longitude(pixel)
        request_params[ARC2_DATE] = LocalDate.to_compact(datetime.date.fromordinal(date))
        request_params[ARC2_DAYS] = int(days)

        logging.debug('arc2 pixel location {}'.format(pixel))
        logging.debug('arc2 rainfall request params {}'.format(request_params))

        while True:
            try:
                response = requests.get(
                    self._url('arc2/rainfall'), 
                    params = request_params, 
                    timeout = int(days * self['timeout_s']))

                logging.debug('ARC2 rainfall data\n{}'.format(response.text))

                return response.status_code, response.url, response.encoding, response.text
        
            except Exception as e:
                message = "error calling arc2 server {}".format(e)
                logging.warning(message)

                if "Read timed out" in message or "Max retries exceeded" in message:
                    logging.info("arc2/rainfall connection issue, trying again after 5s ...")
                    time.sleep(5.0)
                else:
                    return 500, self._url('arc2/rainfall'), None, ""


    def _rainfall_csv(self, pixel, date, days):
        days_int = int(days)

        rainfall_csv = self._process_rainfall_csv(pixel)

        text_list = []        
        for days_offset in range(days):
            day = LocalDate.to_compact(datetime.date.fromordinal(date + days_offset))
            if day in rainfall_csv:
                text_list.append('{} {}'.format(day, rainfall_csv[day]))
                logging.debug('RAINFALL CSV date {} day {} rainfall_csv[day] {}'.format(date, day, rainfall_csv[day]))
            else:
                text_list.append('{} ""'.format(day))
                logging.debug('RAINFALL CSV date {} day {} rainfall_csv[day] na-> ""'.format(date, day))

        status_code = 200
        url = None
        encoding = None
        text = '\n'.join(text_list)

        return status_code, url, encoding, text


    # 210825 Pixel400568Sorghum2254700121146for june 28th the 0.34008mm -> 0 which leads to many loss blocks
    # day = int(date_raw[0])
    def _process_rainfall_csv(self, pixel):
        file_path = '/engine/tmp/s3/download/{}.csv'.format(pixel)
        header = { '':0, '2021': 39 }
        rainfall = {}

        logging.info('reading arc2 rainfall data from {}'.format(file_path))

        with open(file_path, newline='') as fil:
            line = 0
  
            for row in csv.reader(fil):
                line += 1

                if line == 1:
                    continue

                row_data = extract_row_data_csv(header, row)
                date_raw = row_data[''].split('-')
                day = int(date_raw[0])
                month = Arc2.MONTH_TO_INT[date_raw[1]]
                date_key = '2021{:02d}{:02d}'.format(month, day)

                if date_key == '20210628':
                    logging.debug('line "{}" date_key {} rainfall {}'.format(row_data, date_key, row_data['2021']))

                rainfall[date_key] = row_data['2021']
        
        return rainfall


    # only used to provide cache status info to openapi interface
    def cache(self, date, days):
        request_params = {}
        request_params[ARC2_DATE] = LocalDate.to_compact(date)
        request_params[ARC2_DAYS] = days

        logging.debug('arc2 rainfall cache params {}'.format(request_params))

        response = requests.get(
            self._url('arc2/cache'), 
            params = request_params, 
            timeout = self['timeout_s'])

        # TODO have arc2 server provide the ftp url data source
        ftp_url = 'https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/geotiff/'

        logging.debug('arc2 cache content\n{}'.format(response.text))

        return response.status_code, response.url, response.encoding, response.text, ftp_url
    

    def _url(self, path=ARC2_PATH):
        return ARC2_URL_TEMPLATE.format(self['host'], self['port'], path)


class RainfallCalculator(object):

    @staticmethod
    def sum(rainfall, date, days, cap_mm=999):
        """ calculate cumulative rainfall (and count missing rainfall data days) """

        idx_start, idx_end = RainfallCalculator.get_start_end(rainfall, date, days)
        count_missing = 0
        sum_mm = 0.0

        if idx_start < 0:
            return sum_mm, count_missing

        for (rainfall_date, rainfall_amount) in rainfall['data'][idx_start:idx_end]:
            # check for missing rainfall value
            if rainfall_amount == 999.0:
                count_missing += 1
                continue

            # sanity check for rainfall >= 0 mm
            if rainfall_amount >= 0.0:
                sum_mm += min(rainfall_amount, cap_mm)
            else:
                logging.warning("unexpected negative amount of rain for block {}".format(rainfall_amount))

        return sum_mm, count_missing


    @staticmethod
    def count_days_with_percipitation(rainfall, date, days, min_mm=0.0):
        """ count number of days with rainfall matching at least required amount """

        idx_start, idx_end = RainfallCalculator.get_start_end(rainfall, date, days)
        count_missing = 0
        rainy_days = 0

        if idx_start < 0:
            return rainy_days

        for (rainfall_date, rainfall_amount)  in rainfall['data'][idx_start:idx_end]:
            # check for missing rainfall value
            if rainfall_amount == 999.0:
                count_missing += 1
                continue

            if rainfall_amount >= min_mm: 
                rainy_days += 1

        return rainy_days


    @staticmethod
    def get_start_end(rainfall, date, days):
        idx_start = date - rainfall['day_date']
        idx_end = idx_start + days

        if idx_start < 0 or idx_start >= rainfall['days']:
            logging.warning("start index {} outside range(0 .. {})".format(idx_start, rainfall['days'] - 1))
            return -1, -1
        
        if idx_end < 0 or idx_end > rainfall['days']:
            logging.warning("end index {} outside range(0 .. {})".format(idx_end, rainfall['days']))
            return -1, -1

        return idx_start, idx_end


class Rainfall(Entity):
    """Class to obtain rainfall data from Arc2 server"""

    def __init__(self, arc2, pixel, date, days, log_message=''):
        self['pixel'] = pixel
        self['day_date'] = date
        self['days'] = days
        self['data'] = None
        (self['latitude'], self['longitude']) = pixel_to_latitude_longitude(pixel)

        info = '{} {} {} lat/long {}/{}'.format(pixel, datetime.date.fromordinal(date), days, self['latitude'], self['latitude'])

        if log_message:
            logging.info('requesting arc2 rainfall data ({}) {}'.format(info, log_message))
        else:
            logging.info('requesting arc2 rainfall data {}'.format(info))

        status_code, url, encoding, text = arc2.rainfall(pixel, date, days)

        if status_code == 200:
            logging.debug("Percipitation.__init__ url: {}, encoding: {}, txt: (starting on next line)\n{}".format(url, encoding, text))
        else:
            logging.warning("Percipitation.__init__ url: {}, encoding: {}, txt: (starting on next line)\n{}".format(url, encoding, text))
            return

        # update object data cache
        data = []
        for line in text.split('\n'):
            if len(line) > 0:
                try:
                    tok = line.split(' ')
                    if len(tok) == 2 and len(tok[1]) > 0:
                        data.append((tok[0], float(tok[1])))
                    elif len(tok) == 2 and tok[1] == '':
                        logging.info("arc2 response line with single token {}".format(tok[0]))
                    else:
                        logging.warning("unexpected arc2 response line '{}'".format(line))
                except Exception as e:
                    logging.error("unexpected arc2 server response {} exception {}".format(line, e))
                    data.append(('None', 999))

        self['data'] = data

    def data(self):
        return self['data']

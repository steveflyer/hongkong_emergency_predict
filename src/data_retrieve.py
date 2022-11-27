import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

from utils import DatetimeUtils, NetworkUtils, OsUtils, WaitTimeUtils
from conf import RAW_DATA_DIR

ARCHIVE_DIR = os.path.join(RAW_DATA_DIR, 'archive')
if not os.path.exists(ARCHIVE_DIR):
    print('ARCHIVE_DIR not detected: {}. Constructing it now...'.format(ARCHIVE_DIR))
    os.makedirs(ARCHIVE_DIR)


class WaitTimeDataRetriever:
    """
    The Data Retriever class for retrieving Emergency Wait Time Data in Hong Kong from https://data.gov.hk/sc/.
    """

    def __init__(self, data_path: str = ARCHIVE_DIR):
        self.data_path = data_path

    def retrieve(self, begin_datetime: datetime, end_datetime: datetime = None, verbose=False):
        """
        retrieve data from remote websites.
        :param begin_datetime:  the start time
        :param end_datetime:  the end time
        :param verbose:  whether to output debugging information
        :return: no return
        """
        if end_datetime is None:
            end_datetime = DatetimeUtils.get_date_start(datetime.now())
        target_urls = self.__get_target_urls(begin_datetime, end_datetime)
        save_fnames = [self.__get_save_filename(url) for url in target_urls]
        save_fpaths = [os.path.join(self.data_path, fname) for fname in save_fnames]
        NetworkUtils.download_urls(target_urls, save_fpaths, verbose=verbose)

    @staticmethod
    def __get_save_filename(target_url: str):
        file_str = target_url.split('%2')[-1].split('&')[0]
        file_name_str = file_str.split('.')[0]
        file_suffix_str = file_str.split('.')[1]
        time_str = target_url.split(';')[-1][5:]
        file_str = file_name_str + '-' + time_str + '.' + file_suffix_str
        return file_str

    @staticmethod
    def __get_target_urls(begin_datetime: datetime, end_datetime: datetime):
        cur_datetime = end_datetime
        target_urls = []
        while cur_datetime >= begin_datetime:
            url = 'https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fwww.ha.org.hk%2Fopendata' \
                  '%2Faed%2Faedwtdata-en.json&amp;time=' + (
                      cur_datetime.strftime('%Y%m%d-%H%M'))
            target_urls.append(url)
            cur_datetime -= timedelta(minutes=15)
        return target_urls

    def info(self):
        print('The Emergency WaitTime Data Retriever: there\'re {} files in archive dir, '
              'date range from {} to {}.'.format(len(os.listdir(self.data_path))))

    def merge_archive(self):
        result_dict = defaultdict(lambda : [])
        data_paths = OsUtils.listdir_paths(self.data_path)
        for fpath in data_paths:
            with open(fpath) as f:
                record = json.loads((json.load(f)))['waitTime']
                hosp_list = [d['hospName'] for d in record]
                topwait_list = [d['topWait'] for d in record]
                dt = WaitTimeUtils.get_datetime_from_fname(fpath)
                result_dict['record_time'].append(dt)
                # for hosp_name in hospital_list:
                #     if hosp_name in hosp_list:
                #         idx = hosp_list.index(hosp_name)
                        # data_dict[hosp_name].append(quantify_time(topwait_list[idx]))
                    # else:
                    #     data_dict[hosp_name].append(-1.)
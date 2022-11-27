from datetime import datetime, timedelta
import requests
import json
import os


class OsUtils:
    def __init__(self):
        pass

    @staticmethod
    def listdir_paths(dp: str):
        return [os.path.join(dp, fname) for fname in os.listdir(dp)]

    @staticmethod
    def get_fn_from_fp(fp: str):
        return fp.split('/')[-1]


class DatetimeUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_date_start(dt: datetime):
        return datetime.strptime(datetime.strftime(dt, '%Y-%m-%d'), '%Y-%m-%d')


class NetworkUtils:
    def __init__(self):
        pass

    @staticmethod
    def download_urls(urls: list, save_paths: list, is_json=True, verbose=False):
        if len(urls) > len(save_paths):
            raise ValueError(
                "Incompatible urls and save paths. The length of save_paths({}) is smaller than the length of url "
                "list({})".format(len(urls), len(save_paths)))

        for url, save_path in zip(urls, save_paths):
            response = requests.get(url)
            content = response.content
            if 200 <= response.status_code < 300:
                if verbose:
                    print('[Download_urls]: Downloading from ', url)
                if is_json:
                    JsonUtils.save_json(content, save_path)
                    continue
                else:
                    with open(save_path, 'w') as f:
                        f.write(content)
                    continue
            else:
                if verbose:
                    print('[Download_urls]: ', url, ' response with status code: ', response.status_code)


class JsonUtils:
    def __init__(self):
        pass

    @staticmethod
    def save_json(json_content, save_path):
        json_result = json.dumps(json.loads(json_content.decode()))
        with open(save_path, 'w+') as f:
            json.dump(json_result, f)


class WaitTimeUtils:
    @staticmethod
    def get_datetime_from_fname(fname: str):
        """
        retrieve the datetime info from the saved file name.
        Example:
          > fname: `Faedwtdata-en-20220301-0930.json`

          > output: `datetime(2022,3,1,9,30)`
        :param fname: saved file name
        :return: retrived datetime
        """
        date, time = fname.split('.')[-2].split('-')[-2:]
        return datetime(int(date[:4]), int(date[4:6]), int(date[6:]), int(time[:2]), int(time[2:], 0))

import json
import os.path

CONF_FILE = '../conf/project.json'
json_content = json.load(open(CONF_FILE))


class Config:
    def __init__(self, conf_path: str):
        self.conf_path = conf_path
        self.json = None
        self.refresh_conf()   # parse the json into self.json
        self.parse_conf()     # parse self.json into self.fields

    def refresh_conf(self):
        self.json = json.load(open(CONF_FILE))

    def change_conf_path(self, conf_path:str):
        self.conf_path = conf_path
        self.refresh_conf()

    def parse_conf(self):
        pass

    def get_conf_path(self, show_abs=False):
        if show_abs:
            absolute_path = os.path.abspath(self.conf_path)
            return absolute_path
        else:
            return self.conf_path


INIT_CONF_FILE_PATH = '../conf/project.json'
CONF = Config(conf_path=INIT_CONF_FILE_PATH).json
F_CONF = CONF["file_config"]
DATA_DIR = F_CONF['data_dir']
VISUAL_DIR = F_CONF['visual_output_dir']

RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw_data')
PROC_DATA_DIR = os.path.join(DATA_DIR, 'processed_data')

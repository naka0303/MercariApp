import shutil
from logging import basicConfig, info, debug, warning, DEBUG, INFO, WARNING
import datetime

class LOGGER:

    app_path = None
    logs_path = None
    filename = None

    dt_now = datetime.datetime.now()
    logfilename = str(dt_now.year) + str(dt_now.month) + str(dt_now.day) + '_log.txt'

    # コンストラクタ
    def __init__(self, app_path, logs_path, filename):
        self.app_path = app_path
        self.logs_path = logs_path
        self.filename = filename

    # 空のログファイル生成用関数
    def make_logfile(self):
        with open(self.logs_path + '/' + LOGGER.logfilename, 'w') as f:
            f.write('')
        
    def info(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + LOGGER.logfilename, level=INFO)

        info(self.filename + ' ' + log_msg)

    def debug(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + LOGGER.logfilename, level=DEBUG)

        debug(self.filename + ' ' + log_msg)

    def warning(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + LOGGER.logfilename, level=WARNING)

        warning(self.filename + ' ' + log_msg)

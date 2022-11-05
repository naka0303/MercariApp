import os
from logging import basicConfig, info, debug, warning, error, DEBUG, INFO, WARNING, ERROR
import datetime

class Logger:

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

    # 空のログファイル生成用関数(既に存在すれば生成しない)
    def make_logfile(self):
        logfile_flg = os.path.isfile(self.logs_path + '/' + Logger.logfilename)
        if logfile_flg:
            return 0

        with open(self.logs_path + '/' + Logger.logfilename, 'w') as f:
            f.write('')

        return 0
        
    def info(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + Logger.logfilename, level=INFO)

        info(self.filename + ' ' + log_msg)

        return 0

    def debug(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + Logger.logfilename, level=DEBUG)

        debug(self.filename + ' ' + log_msg)

        return 0

    def warning(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + Logger.logfilename, level=WARNING)

        warning(self.filename + ' ' + log_msg)

        return 0

    def error(self, log_msg):
        basicConfig(filename=self.logs_path + '/' + Logger.logfilename, level=ERROR)

        error(self.filename + ' ' + log_msg)

        return 0

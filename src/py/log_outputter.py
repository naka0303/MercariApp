import os
from logging import basicConfig, info, debug, warning, error, DEBUG, INFO, WARNING, ERROR

class LogOutputter:

    app_path = None
    logs_path = None
    filename = None

    # コンストラクタ
    def __init__(self, app_path, logs_path, filename):
        self.app_path = app_path
        self.logs_path = logs_path
        self.filename = filename

    # 空のログファイル生成用関数(既に存在すれば生成しない)
    def make_logfile(self, log_file):
        logfile_flg = os.path.isfile(self.logs_path + '/' + log_file)
        if logfile_flg:
            return 0

        with open(self.logs_path + '/' + log_file, 'w') as f:
            f.write('')

        return 0
        
    def info(self, log_msg, log_file):
        basicConfig(filename=self.logs_path + '/' + log_file, level=INFO)

        info(self.filename + ' ' + log_msg)

        return 0

    def debug(self, log_msg, log_file):
        basicConfig(filename=self.logs_path + '/' + log_file, level=DEBUG)

        debug(self.filename + ' ' + log_msg)

        return 0

    def warning(self, log_msg, log_file):
        basicConfig(filename=self.logs_path + '/' + log_file, level=WARNING)

        warning(self.filename + ' ' + log_msg)

        return 0

    def error(self, log_msg, log_file):
        basicConfig(filename=self.logs_path + '/' + log_file, level=ERROR)

        error(self.filename + ' ' + log_msg)

        return 0

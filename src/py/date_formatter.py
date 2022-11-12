import datetime

class DateFormatter:
    DT_NOW = datetime.datetime.now()
    YEAR = DT_NOW.year
    MONTH = DT_NOW.month
    DAY = DT_NOW.day
    HOUR = DT_NOW.hour
    MINUTE = DT_NOW.minute
    SECOND = DT_NOW.second

    # 日時のフォーマットを任意の形式にする
    def format_date(self):
        yyyymmdd = str(self.YEAR) + '-' + str(self.MONTH).zfill(2) + '-' + str(self.DAY).zfill(2)
        yyyymmddhhmmss = yyyymmdd + '-' + str(self.HOUR).zfill(2) + '-' + str(self.MINUTE).zfill(2) + '-' + str(self.SECOND).zfill(2)

        return [yyyymmdd, yyyymmddhhmmss]

# filename: unicon
# aggregates all the unix -> date conversion functions into one package

from datetime import datetime
import time


def convert_date_to_unix_time(date):
    unaware_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")  # converts the input string into a type: datetime
    s = time.mktime(unaware_date.timetuple())  # converts datetime to unix time (time since Jan 1, 1970 at midnight)
    return s


def convert_unix_to_date(time_unix):  # Converts unix time (type = int/float) to date (type = datetime)
    return datetime.fromtimestamp(time_unix)

def convert_telemetry_date_to_unix_time(date):
    unaware_date = datetime.strptime(date, "%m/%d/%Y %H:%M:%S")  # converts the input string into a type: datetime
    s = time.mktime(unaware_date.timetuple())  # converts datetime to unix time (time since Jan 1, 1970 at midnight)
    return s

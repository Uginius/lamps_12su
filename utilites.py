import os
import re
from datetime import datetime
import time


def get_last_file():
    files = os.listdir('htmls/')
    all_dates = []
    for file in files:
        dates = re.findall(r'\d{2}-\d{2}-202\d', file)
        if dates:
            all_dates.append(datetime.strptime(dates[0], '%d-%m-%Y'))
    return f"htmls/{sorted(all_dates)[-1].strftime('%d-%m-%Y')}_lamps.html"


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nФункция работала {elapsed} секунд(ы)')
        return result

    return surrogate


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

import datetime
import os

from lib.debugging.subdirectory import Subdirectory


def write_log(content, sub: Subdirectory):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        with open(file_path(sub), 'a') as file:
            file.write(f'[{current_time}] {content}\n')
    except ValueError:
        return


def file_path(sub_directory: Subdirectory):
    if sub_directory not in Subdirectory:
        raise ValueError

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return f'debugging/{sub_directory.value}/log-{current_date}.txt'


def delete_log(sub: Subdirectory):
    try:
        if os.path.exists(file_path(sub)):
            os.remove(file_path(sub))
    except ValueError:
        return

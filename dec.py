import csv
import json

from functools import wraps

def in_file_json(source):
    def dec(func):
        @wraps(func)
        def wrapper():
            info = func()
            with open(source, 'w') as f:
                json.dump(info, f)
            return info
        return wrapper
    return dec

def in_file_csv(source):
    def dec(func):
        @wraps(func)
        def wrapper():
            info = func()
            with open(source, 'w', newline='') as f:
                write_info = csv.writer(f, delimiter=';')
                write_info.writerow(['PID', 'USER', 'PRI', 'S', 'CPU', 'MEM', 'TIME', 'Command'])
                for el in info:
                    write_info.writerow([str(el), info[el]['username'],info[el]['nice'], info[el]['status'], info[el]['cpu_percent'], 
                            info[el]['memory_percent'], info[el]['create_time'], info[el]['exe']])
            return info
        return wrapper
    return dec
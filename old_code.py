import csv
import json

from datetime import datetime
from os import system
from psutil import *
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

@in_file_json('info/sys_info.json')
def get_sys_info():
    boot_t = str(datetime.fromtimestamp(boot_time()))
    usrs = users()
    user = usrs[0].name
    bat = sensors_battery()
    bat = round(bat.percent)
    return boot_t, user, bat

def show_sys_info(sys):
    print('Boot time: {0}\nUser: {1}\nBattery: {2}%'.format(sys[0], sys[1], sys[2]), end='\n\n')

@in_file_json('info/cpu_info.json')
def get_cpu_info():
    return cpu_percent(interval=1, percpu=True)

def show_cpu_info(info):    
    for i in range(len(info)):
        _ = '|' * round(((30*info[i])/100))
        p = 'cpu{0:<2} {1:>4} % [{2:<30}]'.format(i+1, info[i], _)
        if (i+1)%3 == 0:
            print(p)
        else:
            print('{:<50}'.format(p), end='')

@in_file_json('info/mem_info.json')
def get_mem_info():
    mem = virtual_memory()
    total_phys = round(mem.total * 1e-9, 1)
    used_phys = round(mem.used * 1e-9, 1)
    swp = swap_memory()
    total_swp = round(swp.total * 1e-9, 1)
    used_swp = round(swp.used * 1e-9, 1)
    memory = {'total_phys':total_phys, 'used_phys':used_phys, 'total_swp':total_swp, 'used_swp':used_swp}
    return memory

def show_mem_info(mem):
    print('\nMem {0:>15}Gb/{1}Gb'.format(mem['used_phys'], mem['total_phys']))
    print('swp {0:>15}Gb/{1}Gb'.format(mem['used_swp'], mem['total_swp']))       

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

@in_file_csv('info/proc_info.csv')
def get_process_info():
    proc_info = {p.pid: p.info for p in process_iter(['name', 'username', 'nice', 'status', 'cpu_percent', 'memory_percent', 'exe', 'create_time'])}
    return proc_info

def show_process_info(proc):
    print('\n{0:^10}|{1:^20}|{2:^10}|{3:^10}|{4:^10}%|{5:^10}%|{6:^20}|{7:^10}'
          .format('PID', 'USER', 'PRI', 'S', 'CPU', 'MEM', 'TIME', 'Command'), end='\n'+'-'*170+'\n')
    for el in proc:
        proc[el]['create_time'] = datetime.fromtimestamp(boot_time()).strftime("%H:%M:%S")
        proc[el]['cpu_percent'] = round(proc[el]['cpu_percent'], 2)
        proc[el]['memory_percent'] = round(proc[el]['memory_percent'], 2)
        if proc[el]['exe'] != None : 
            print('{0:^10}|{1:^20}|{2:^10}|{3:^10}|{4:^10}%|{5:^10}%|{6:^20}|{7:^10}'
                    .format(el, proc[el]['username'],proc[el]['nice'], proc[el]['status'], proc[el]['cpu_percent'], 
                            proc[el]['memory_percent'], proc[el]['create_time'], proc[el]['exe']))  

def init_term_params():
    system('resize -s 45 170')
    system('clear')

def show(sys, cpu, mem, proc):
    init_term_params()
    show_sys_info(sys)
    show_cpu_info(cpu)
    show_mem_info(mem)
    show_process_info(proc)

def main():
    sys_info = get_sys_info()
    cpu_info = get_cpu_info()
    mem_info = get_mem_info()
    proc_info = get_process_info()
    show(sys_info, cpu_info, mem_info, proc_info)

if __name__ == "__main__":
    main()

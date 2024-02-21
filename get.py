import dec

from datetime import datetime
from psutil import *

@dec.in_file_json('info/sys_info.json')
def get_sys_info():
    boot_t = str(datetime.fromtimestamp(boot_time()))
    usrs = users()
    user = usrs[0].name
    bat = sensors_battery()
    bat = round(bat.percent)
    return boot_t, user, bat

@dec.in_file_json('info/cpu_info.json')
def get_cpu_info():
    return cpu_percent(interval=1, percpu=True)

@dec.in_file_json('info/mem_info.json')
def get_mem_info():
    mem = virtual_memory()
    total_phys = round(mem.total * 1e-9, 1)
    used_phys = round(mem.used * 1e-9, 1)
    swp = swap_memory()
    total_swp = round(swp.total * 1e-9, 1)
    used_swp = round(swp.used * 1e-9, 1)
    memory = {'total_phys':total_phys, 'used_phys':used_phys, 'total_swp':total_swp, 'used_swp':used_swp}
    return memory

@dec.in_file_csv('info/proc_info.csv')
def get_process_info():
    proc_info = {p.pid: p.info for p in process_iter(['name', 'username', 'nice', 'status', 'cpu_percent', 'memory_percent', 'exe', 'create_time'])}
    return proc_info
from datetime import datetime
from psutil import *
from os import system

class GetMethods():
    
    def get_sys_info(self):
        boot_t = str(datetime.fromtimestamp(boot_time()))
        usrs = users()
        user = usrs[0].name
        bat = sensors_battery()
        bat = round(bat.percent)
        return boot_t, user, bat
    
    def get_cpu_info(self):
        return cpu_percent(interval=1, percpu=True)
    
    def get_mem_info(self):
        mem = virtual_memory()
        total_phys = round(mem.total * 1e-9, 1)
        used_phys = round(mem.used * 1e-9, 1)
        swp = swap_memory()
        total_swp = round(swp.total * 1e-9, 1)
        used_swp = round(swp.used * 1e-9, 1)
        memory = {'total_phys':total_phys, 'used_phys':used_phys, 'total_swp':total_swp, 'used_swp':used_swp}
        return memory
    
    def get_process_info(self):
        proc_info = {p.pid: p.info for p in process_iter(['name', 'username', 'nice', 'status', 'cpu_percent', 'memory_percent', 'exe', 'create_time'])}
        return proc_info

class ShowMethods():
    
    def show_sys_info(self, sys_info):
        print('Boot time: {0}\nUser: {1}\nBattery: {2}%'.format(sys_info[0], sys_info[1], sys_info[2]), end='\n\n')

    def show_cpu_info(self, info):    
        for i in range(len(info)):
            _ = '|' * round(((30*info[i])/100))
            p = 'cpu{0:<2} {1:>4} % [{2:<30}]'.format(i+1, info[i], _)
            if (i+1)%3 == 0:
                print(p)
            else:
                print('{:<50}'.format(p), end='')

    def show_mem_info(self, mem):
        print('\nMem {0:>15}Gb/{1}Gb'.format(mem['used_phys'], mem['total_phys']))
        print('swp {0:>15}Gb/{1}Gb'.format(mem['used_swp'], mem['total_swp']))    

    def show_process_info(self, proc):
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

def main():
    
    init_term_params()

    sys_info = GetMethods().get_sys_info()
    cpu_info = GetMethods().get_cpu_info()
    mem_info = GetMethods().get_mem_info()
    proc_info = GetMethods().get_process_info()

    ShowMethods().show_sys_info(sys_info)
    ShowMethods().show_cpu_info(cpu_info)
    ShowMethods().show_mem_info(mem_info)
    ShowMethods().show_process_info(proc_info)


if __name__ == "__main__":
    main()

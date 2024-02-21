from datetime import datetime
from psutil import boot_time
from os import system

def show_sys_info(sys):
    print('Boot time: {0}\nUser: {1}\nBattery: {2}%'.format(sys[0], sys[1], sys[2]), end='\n\n')

def show_cpu_info(info):    
    for i in range(len(info)):
        _ = '|' * round(((30*info[i])/100))
        p = 'cpu{0:<2} {1:>4} % [{2:<30}]'.format(i+1, info[i], _)
        if (i+1)%3 == 0:
            print(p)
        else:
            print('{:<50}'.format(p), end='')

def show_mem_info(mem):
    print('\nMem {0:>15}Gb/{1}Gb'.format(mem['used_phys'], mem['total_phys']))
    print('swp {0:>15}Gb/{1}Gb'.format(mem['used_swp'], mem['total_swp']))      

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

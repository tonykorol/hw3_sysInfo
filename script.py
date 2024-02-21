from get import *
from show import *

def main():
    init_term_params()
    show_sys_info(get_sys_info())
    show_cpu_info(get_cpu_info())
    show_mem_info(get_mem_info())
    show_process_info(get_process_info())

if __name__ == "__main__":
    main()

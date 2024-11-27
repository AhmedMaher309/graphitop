import psutil

def get_memory():
    mem = psutil.virtual_memory()
    return mem


def get_swap():
    swap = psutil.swap_memory()
    return swap


def get_cpu_percent():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent

def get_cpu_count():
    return psutil.cpu_count(logical=True)


def get_cores_percentages():
    cpu_percentages = psutil.cpu_percent(interval=None, percpu=True)    
    return cpu_percentages


def get_process_details():
    process_list = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                     'memory_percent', 'cpu_times', 'nice',
                                     'memory_info', 'cmdline']):
        try:
            # Get process info
            pinfo = proc.info

            # Get memory information (convert to MB)
            mem_info = proc.memory_info()
            virt = mem_info.vms / 1024 / 1024
            res = mem_info.rss / 1024 / 1024 
            if hasattr(mem_info, 'shared'):
                shr = mem_info.shared / 1024 / 1024
            else: 
                shr = 0

            # Get CPU priority
            try:
                priority = proc.nice()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                priority = 'N/A'

            # Calculate CPU time
            cpu_time = proc.cpu_times()[0] + proc.cpu_times()[1]
            cpu_time_str = f"{int(cpu_time // 60):02d}:{int(cpu_time % 60):02d}"

            # Get command
            try:
                cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                cmdline = '[Access Denied]'

            process_info = {
                'PID': proc.pid,
                'USER': pinfo['username'] or 'N/A',
                'PRI': priority,
                'NI': pinfo['nice'] or 'N/A',
                'VIRT': f"{virt:.1f}MB",
                'RES': f"{res:.1f}MB",
                'SHR': f"{shr:.1f}MB",
                'CPU%': f"{pinfo['cpu_percent']:.1f}",
                'MEM%': f"{pinfo['memory_percent']:.1f}",
                'TIME': cpu_time_str,
                'COMMAND': cmdline
            }

            process_list.append(process_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_list


def get_load_avg():
    return psutil.getloadavg()



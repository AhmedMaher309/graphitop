import psutil


def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.pid
            cpu_percent = proc.cpu_percent(interval=None)
            name = proc.name()
            cmdline = ' '.join(proc.cmdline()) or name
            processes.append((pid, cpu_percent, cmdline))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


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


def display_processes(processes):
    top_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:50]
    print(f"{'PID':<10}{'CPU %':<10}{'Command':<60}")
    print("-" * 80)
    for pid, cpu_percent, cmdline in top_processes:
        print(f"{pid:<10}{cpu_percent:<10.2f}{cmdline[:57]:<60}")



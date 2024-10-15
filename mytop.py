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


def display_cpu(num_cores):
    cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
    print(f"Overall CPU Usage: {sum(cpu_percent) / num_cores:.1f}%")
    print("CPU Core Usage:")
    for i, usage in enumerate(cpu_percent):
        print(f"Core {i}: {usage:.1f}%", end="  ")
        if (i + 1) % 4 == 0:
            print()  # New line every 4 cores
    if num_cores % 4 != 0:
        print()  # Ensure a new line after cores if not divisible by 4
    print()


def display_processes(processes):
    top_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:50]
    print(f"{'PID':<10}{'CPU %':<10}{'Command':<60}")
    print("-" * 80)
    for pid, cpu_percent, cmdline in top_processes:
        print(f"{pid:<10}{cpu_percent:<10.2f}{cmdline[:57]:<60}")



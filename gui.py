from tkinter import ttk
import tkinter as tk
import time

from mytop import get_memory, get_swap, get_cpu_percent, get_cpu_count, get_cores_percentages

mem_vertical_start_point = 0.35
mem_horizontal_start_point = 0.05

swap_vertical_start_point = 0.35
swap_horizontal_start_point = 0.60

cpu_percent_vertical_start_point = 0.01
cpu_percent_horizontal_start_point = 0.05

cores_vertical_start_point = 0.05
cores_horizontal_start_point = 0.60

cores_vertical_range = swap_vertical_start_point - cores_vertical_start_point
cores_horizontal_range = 0.35



"""
Create the staic memory bar and define the progress variable (progress_var)
"""
def create_memory_bar(root, screen_width):
    style = ttk.Style()
    style.configure("memory.Horizontal.TProgressbar", troughcolor='white', background='green')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="memory.Horizontal.TProgressbar")

    progress_bar.place(relx=mem_horizontal_start_point, rely=mem_vertical_start_point, relwidth=0.35, relheight=0.032)

    # Create a label to display the percentage inside the progress bar
    percent_label = tk.Label(root, text="0%", fg="white", bg="black", font=("Arial", 12, "bold"))
    percent_label.place(relx=mem_horizontal_start_point+0.35, rely=mem_vertical_start_point+0.01)

    return progress_var, percent_label


"""
create the swap memory static bar and define its progress variable (progress_var)
"""
def create_swap_bar(root, screen_width):
    style = ttk.Style()
    style.configure("swap.Horizontal.TProgressbar", troughcolor='white', background='green')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="swap.Horizontal.TProgressbar")

    progress_bar.place(relx=swap_horizontal_start_point, rely=swap_vertical_start_point, relwidth=0.35, relheight=0.032)

    # Create a label to display the percentage inside the progress bar
    percent_label = tk.Label(root, text="0%", bg="black", fg="white", font=("Arial", 12, "bold"))
    percent_label.place(relx=swap_horizontal_start_point+0.35, rely=swap_vertical_start_point+0.01)

    return progress_var, percent_label


"""
create the fields for the cpu usage graphline
"""
def create_cpu_graph_line(root, screen_width):

    cpu_graph = tk.Canvas(root, bg="black")
    cpu_graph.place(relx=cpu_percent_horizontal_start_point, rely=cpu_percent_vertical_start_point, relwidth=0.4, relheight=0.3)

    # Add grid lines
    width = int(screen_width * 0.9)
    height = int(screen_height * 0.25)
    for i in range(0, 101, 20):
        y = height - (i / 100 * height)
        cpu_graph.create_line(0, y, width, y, fill='red', dash=(2, 4))
        cpu_graph.create_text(10, y, text=f"{i}%", fill='white', anchor='w')

    return cpu_graph


"""
create the bars for the cpu cores
"""
def create_cpu_cores_bars(root, screen_width):
    cores_count = get_cpu_count()

    #calculate the height (thickness) of each bar representing a core\
    # put additional 0.18 for the spacing between bars
    bar_height = (cores_vertical_range - 0.18) / (cores_count / 2)

    bar_width = (cores_horizontal_range - 0.05) / 2
    start_y_point = cpu_percent_vertical_start_point

    progress_vars = []
    for i in range(cores_count):
        start_x_point = cores_horizontal_start_point
        if i%2 != 0:
            start_x_point += bar_width + 0.05
        style = ttk.Style()
        style.configure("cores.Horizontal.TProgressbar", troughcolor='white', background='red')

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="cores.Horizontal.TProgressbar")

        progress_bar.place(relx=start_x_point, rely=start_y_point, relwidth=bar_width, relheight=bar_height)

        if i%2 != 0:
            start_y_point += 0.08
        
        progress_vars.append(progress_var)
    
    return progress_vars



"""
Update the swap bar progress_var and label
Use the root.after to update the changes every 100 ms
"""
def update_swap_bar(root, progress_var, percent_label):
    swap = get_swap()
    swap_percentage = swap.percent

    progress_var.set(swap_percentage)
    percent_label.config(text=f"{swap_percentage:.1f}%")

    root.after(100, update_swap_bar, root, progress_var, percent_label)


"""
Update the memory bar progress_var and label
Use the root.after to update the changes every 100 ms
"""
def update_memory_bar(root, progress_var, percent_label):
    mem = get_memory()
    memory_usage_percentage = mem.percent

    progress_var.set(memory_usage_percentage)
    percent_label.config(text=f"{memory_usage_percentage:.1f}%")

    root.after(100, update_memory_bar,root, progress_var, percent_label)


"""
Update the CPU usage graphline every 100 ms 

"""
def update_cpu_graph(root, cpu_graph, cpu_data, start_time):
    cpu_percent = get_cpu_percent()
    current_time = time.time() - start_time

    cpu_data.append((current_time, cpu_percent))

    #delete data after every 60 seconds
    while cpu_data and current_time - cpu_data[0][0] > 60:
        cpu_data.pop(0)

    # delete previous lines drawn on canvas that has the tag "graph"
    # to avoid multiple lines and overlaping
    cpu_graph.delete("graph")

    width = cpu_graph.winfo_width()
    height = cpu_graph.winfo_height()

    # Draw the graph line
    if len(cpu_data) > 1:
        points = []
        for i, (t, cpu) in enumerate(cpu_data):
            x = width * (t - (current_time - 60)) / 60
            y = height * (1 - cpu / 100)
            points.extend([x, y])

        cpu_graph.create_line(points, fill='blue', width=3, tags="graph")

    root.after(100, update_cpu_graph, root, cpu_graph, cpu_data, start_time)


"""
Update the cores bars according to each core usage
"""
def update_cores_bars(root, progress_vars):
    cores = get_cores_percentages()
    for i, percentage in enumerate(cores):
        progress_vars[i].set(percentage)

    root.after(100, update_cores_bars, root, progress_vars)



root = tk.Tk()
root.title("My Top")
root.configure(background="black")
root.minsize(1200, 900)

# Set the window size to fill the entire screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Create the progress bar and percentage label using the function
mem_progress_var, mem_percent_label = create_memory_bar(root, screen_width)
swap_progress_var, swap_percent_label = create_swap_bar(root, screen_width)

# Start updating the memory bar
update_memory_bar(root, mem_progress_var, mem_percent_label)
update_swap_bar(root, swap_progress_var, swap_percent_label)

# Draw cpu cores
cores_vars = create_cpu_cores_bars(root, screen_width)
update_cores_bars(root, cores_vars)

# Create CPU graph and start updating it
cpu_graph = create_cpu_graph_line(root, screen_width)

cpu_data = []
start_time = time.time()
update_cpu_graph(root, cpu_graph, cpu_data, start_time)


root.mainloop()


from tkinter import ttk
import tkinter as tk
import time

from system_metrics import get_memory, get_swap, get_cpu_percent, get_cpu_count, get_cores_percentages, get_process_details

mem_vertical_start_point = 0.35
mem_horizontal_start_point = 0.05

swap_vertical_start_point = 0.35
swap_horizontal_start_point = 0.60

cpu_percent_vertical_start_point = 0.01
cpu_percent_horizontal_start_point = 0.05

cores_vertical_start_point = 0.03
cores_horizontal_start_point = 0.60

cores_vertical_range = swap_vertical_start_point - cores_vertical_start_point
cores_horizontal_range = 0.35

processess_table_vertical_start_point = 0.4
processess_table_horizontal_start_point = 0.02



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

    # Add a descriptive label
    desc_label = tk.Label(root, text="Memory Usage:", fg="white", bg="black", 
                            font=("Arial", 12, "bold"))
    desc_label.place(relx=mem_horizontal_start_point, rely=mem_vertical_start_point-0.025)
    
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
    
    # Add a descriptive label
    desc_label = tk.Label(root, text="Swap Usage:", fg="white", bg="black", 
                            font=("Arial", 12, "bold"))
    desc_label.place(relx=swap_horizontal_start_point, rely=swap_vertical_start_point-0.025)
    
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
    start_y_point = cores_vertical_start_point

    progress_vars = []

    # Add a descriptive label
    desc_label = tk.Label(root, text="CPU Cores Usage:", fg="white", bg="black", 
                            font=("Arial", 12, "bold"))
    desc_label.place(relx=cores_horizontal_start_point, rely=cores_vertical_start_point-0.02)

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
Display the running processess with their details in the rest of the screen
"""
def create_processess_frame(root, screen_width):
    # Create a frame to hold the table and scrollbar
    process_frame = tk.Frame(root, bg="black")
    process_frame.place(relx=processess_table_horizontal_start_point, 
                        rely=processess_table_vertical_start_point, 
                        relwidth=0.98, relheight=0.6)

    # Create the treeview with columns
    columns = ('PID', 'USER', 'PRI', 'NI', 'VIRT', 'RES', 'SHR', 'CPU%', 'MEM%', 'TIME', 'COMMAND')
    tree = ttk.Treeview(process_frame, columns=columns, show='headings')

    # Configure the treeview style
    style = ttk.Style()
    style.configure("Treeview", 
                    background="black",
                    foreground="white",
                    fieldbackground="black")
    style.configure("Treeview.Heading",
                    background="gray25",
                    foreground="white")

    # Set column widths and headings
    column_widths = {
        'PID': 70,
        'USER': 100,
        'PRI': 50,
        'NI': 50,
        'VIRT': 80,
        'RES': 80,
        'SHR': 80,
        'CPU%': 60,
        'MEM%': 60,
        'TIME': 70,
        'COMMAND': 300
    }

    for col in columns:
        tree.heading(col, text=col, anchor='w')
        tree.column(col, width=column_widths[col], anchor='w')

    # Add scrollbars
    vsb = ttk.Scrollbar(process_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(process_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Grid layout
    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    # Configure grid weights
    process_frame.grid_rowconfigure(0, weight=1)
    process_frame.grid_columnconfigure(0, weight=1)

    return tree




"""
Update the swap bar progress_var and label
Use the root.after to update the changes every 100 ms
"""
def update_swap_bar(root, progress_var, percent_label):
    swap = get_swap()
    swap_percentage = swap.percent

    progress_var.set(swap_percentage)
    percent_label.config(text=f"{swap_percentage:.1f}%")

    root.after(500, update_swap_bar, root, progress_var, percent_label)


"""
Update the memory bar progress_var and label
Use the root.after to update the changes every 100 ms
"""
def update_memory_bar(root, progress_var, percent_label):
    mem = get_memory()
    memory_usage_percentage = mem.percent

    progress_var.set(memory_usage_percentage)
    percent_label.config(text=f"{memory_usage_percentage:.1f}%")

    root.after(500, update_memory_bar,root, progress_var, percent_label)


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

    root.after(500, update_cpu_graph, root, cpu_graph, cpu_data, start_time)


"""
Update the cores bars according to each core usage
"""
def update_cores_bars(root, progress_vars):
    cores = get_cores_percentages()
    for i, percentage in enumerate(cores):
        progress_vars[i].set(percentage)

    root.after(500, update_cores_bars, root, progress_vars)



"""
Update the processes in their table
"""
def update_processes(root, process_tree):

    # Clear current items
    for item in process_tree.get_children():
        process_tree.delete(item)

    # Get fresh process data
    processes = get_process_details()

    # Sort processes by CPU usage (descending)
    processes.sort(key=lambda x: float(x.get('CPU%', 0)), reverse=True)
    
    for proc in processes:
        try:
            values = (
                proc['PID'],
                proc['USER'],
                proc['PRI'],
                proc['NI'],
                proc['VIRT'],
                proc['RES'],
                proc['SHR'],
                f"{float(proc['CPU%']):.1f}",
                f"{float(proc['MEM%']):.1f}",
                proc['TIME'],
                proc['COMMAND']
            )

            if len(process_tree.get_children()) % 2 == 0:
                tag = 'oddrow'
            else:
                tag = 'evenrow'
            process_tree.insert('', 'end', values=values, tags=(tag,))

        except (KeyError, ValueError):
            continue

    # Configure row colors
    process_tree.tag_configure('oddrow', background='dark red')
    process_tree.tag_configure('evenrow', background='black')

    root.after(500, update_processes, root, process_tree)


root = tk.Tk()
root.title("GraphiTop")
root.configure(background="black")
root.minsize(1200, 900)

# Set the window size to fill the entire screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Create the bars for the memory and return the label and the progress_var for each bar
mem_progress_var, mem_percent_label = create_memory_bar(root, screen_width)
swap_progress_var, swap_percent_label = create_swap_bar(root, screen_width)

# Start updating the memory bar
update_memory_bar(root, mem_progress_var, mem_percent_label)
update_swap_bar(root, swap_progress_var, swap_percent_label)

# Draw cpu cores and update them 
cores_vars = create_cpu_cores_bars(root, screen_width)
update_cores_bars(root, cores_vars)

# Create CPU graph and start updating it
cpu_graph = create_cpu_graph_line(root, screen_width)
cpu_data = []
start_time = time.time()
update_cpu_graph(root, cpu_graph, cpu_data, start_time)

# Create the frame for the processess
process_tree = create_processess_frame(root, screen_width)
update_processes(root, process_tree)


root.mainloop()


from tkinter import ttk
import tkinter as tk
import time

from mytop import get_memory, get_swap, get_cpu_percent

"""
Create the staic memory bar and define the progress variable (progress_var)
"""
def create_memory_bar(root, screen_width):
    style = ttk.Style()
    style.configure("TProgressbar", troughcolor='white', background='green')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="TProgressbar")

    progress_bar.place(relx=0.05, rely=0.3, relwidth=0.3, relheight=0.032)

    # Create a label to display the percentage inside the progress bar
    percent_label = tk.Label(root, text="0%", fg="white", bg="black", font=("Arial", 12, "bold"))
    percent_label.place(relx=0.35, rely=0.31)

    return progress_var, percent_label


"""
create the swap memory static bar and define its progress variable (progress_var)
"""
def create_swap_bar(root, screen_width):
    style = ttk.Style()
    style.configure("TProgressbar", troughcolor='white', background='green')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="TProgressbar")

    progress_bar.place(relx=0.65, rely=0.3, relwidth=0.3, relheight=0.032)

    # Create a label to display the percentage inside the progress bar
    percent_label = tk.Label(root, text="0%", bg="black", fg="white", font=("Arial", 12, "bold"))
    percent_label.place(relx=0.95, rely=0.31)

    return progress_var, percent_label


"""
Draw the fiels for the cpu usage graphline
"""
def create_cpu_graph_line(root, screen_width):

    cpu_graph = tk.Canvas(root, bg="black")
    cpu_graph.place(relx=0.05, rely=0.01, relwidth=0.4, relheight=0.25)

    # Add grid lines
    width = int(screen_width * 0.9)
    height = int(screen_height * 0.25)
    for i in range(0, 101, 20):
        y = height - (i / 100 * height)
        cpu_graph.create_line(0, y, width, y, fill='#333333', dash=(2, 4))
        cpu_graph.create_text(10, y, text=f"{i}%", fill='white', anchor='w')

    return cpu_graph


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

        cpu_graph.create_line(points, fill='green', width=3, tags="graph")

    root.after(100, update_cpu_graph, root, cpu_graph, cpu_data, start_time)



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


# Create CPU graph and start updating it
cpu_graph = create_cpu_graph_line(root, screen_width)

cpu_data = []
start_time = time.time()
update_cpu_graph(root, cpu_graph, cpu_data, start_time)


root.mainloop()


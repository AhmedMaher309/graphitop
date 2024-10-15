from tkinter import ttk
import tkinter as tk

from mytop import get_memory, get_swap


def create_memory_bar(root, screen_width):
    style = ttk.Style()
    style.configure("TProgressbar", troughcolor='white', background='green')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="TProgressbar")

    progress_bar.place(relx=0.02, rely=0.3, relwidth=0.3, relheight=0.032)

    # Create a label to display the percentage inside the progress bar
    percent_label = tk.Label(root, text="0%", fg="white", bg="black", font=("Arial", 12, "bold"))
    percent_label.place(relx=0.32, rely=0.31)

    return progress_var, percent_label



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




def update_swap_bar(progress_var, percent_label):
    """Updates the swap usage progress bar and label."""
    swap = get_swap()
    swap_percentage = swap.percent

    progress_var.set(swap_percentage)
    percent_label.config(text=f"{swap_percentage:.1f}%")

    root.after(1000, update_swap_bar, progress_var, percent_label)




def update_memory_bar(progress_var, percent_label):
    """Updates the memory usage progress bar and label."""
    mem = get_memory()
    memory_usage_percentage = mem.percent

    progress_var.set(memory_usage_percentage)
    percent_label.config(text=f"{memory_usage_percentage:.1f}%")

    root.after(1000, update_memory_bar, progress_var, percent_label)




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
update_memory_bar(mem_progress_var, mem_percent_label)
update_swap_bar(swap_progress_var, swap_percent_label)

root.mainloop()


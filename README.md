# GraphiTop

GraphiTop is a graphical system monitoring tool for Linux systems, providing real-time visualization of system resources including CPU, memory, swap usage, and process information. It offers a user-friendly interface with dynamic graphs and tables for easy system performance monitoring.

![GraphiTop Screenshot](https://github.com/AhmedMaher309/graphitop/blob/main/imgs/Screenshot%20from%202024-10-22%2021-56-44.png)

## Features

- **Real-time System Monitoring**
  - CPU usage graph with 60-second history
  - Individual CPU core usage bars
  - Memory usage visualization
  - Swap memory usage tracking
  - Detailed process information table
  - Load average

- **Process Information Display**
  - PID (Process ID)
  - User
  - Priority
  - Nice value
  - Virtual memory usage
  - Resident memory usage
  - Shared memory usage
  - CPU usage percentage
  - Memory usage percentage
  - Process runtime
  - Command/process name

- **Dynamic Updates**
  - All metrics update every second
  - Color-coded visualizations
  - Sortable process table

## Prerequisites

- Python 3.6 or higher
- Linux operating system
- Required Python packages:
  ```bash
  - psutil
  - tkinter
  ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AhmedMaher309/graphitop.git
cd graphitop
```

2. Install the required dependencies:
```bash
pip install psutil
pip install tkinter
```


## Usage

Run the program using:
```bash
python3 graphitop.py
```

### Interface Guide

- **Top Section**
  - CPU usage graph shows the last 60 seconds of CPU activity
  - Individual core usage bars display real-time usage for each CPU core
  
- **Middle Section**
  - Memory usage bar shows current RAM utilization
  - Swap usage bar indicates virtual memory usage
  
- **Bottom Section**
  - Process table displays detailed information about running processes
  - Use scrollbars to view more processes


## Configuration

The interface is configured for a minimum resolution of 1200x900 pixels. The window will automatically scale to your screen size for optimal viewing.

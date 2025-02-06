# MeetMetrics: Comparative Analysis of Meeting Applications' Resource Consumption

**MeetMetrics** is a research project that compares the computational resource usage of various online meeting applications—including Voov, Skype, Zoom, and TeamViewer—to determine their efficiency in real-time communication scenarios. The goal is to provide actionable insights into which application is best suited for environments with limited computational resources, such as those used in online education.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Code Overview](#code-overview)
- [Research Criteria](#research-criteria)
- [Research Method](#research-method)
- [Monitoring Details](#monitoring-details)
  - [TeamViewer](#monitoring-of-teamviewer)
  - [Skype](#monitoring-of-skype)
  - [VooV](#monitoring-of-voov)
  - [Zoom](#monitoring-of-zoom)
- [Performance Comparison](#performance-comparison)
- [Conclusion](#conclusion)
- [License](#license)
- [Contact](#contact)

---

## Problem Statement

One of the primary challenges in our research is that each meeting application (Voov, Skype, Zoom, TeamViewer) executes multiple processes during its runtime. To accurately measure the resource usage of these applications, it is essential to identify **every process** spawned by the software and monitor them individually. Without process-level granularity, the total resource consumption cannot be precisely determined.

---

## Solution

To address this challenge, we developed a Python script that monitors system resources on a per-process basis. Since each meeting application uses a specific process name for all its processes, the solution involves filtering processes by their name and tracking resource metrics such as CPU usage, memory consumption, and the number of threads.

---

## Code Overview

The following Python code demonstrates how we monitor CPU and RAM usage for a given meeting application (in this example, *Zoom*). The script uses the `psutil` library to retrieve process information, the `csv` module to log data, and the `time` module to control the sampling interval.

### Code Explanation

1. **Library Imports:**
   - **psutil:** Retrieves data on active processes and system utilization (CPU, RAM, etc.).
   - **csv:** Reads and writes tabular data in CSV format.
   - **time:** Manages delays and time-based operations during code execution.

2. **Continuous Monitoring:**
   - An infinite loop (`while True:`) repeatedly scans for processes that match a specified name (e.g., `"Zoom"`).
   - The script gathers process IDs, names, statuses, CPU usage (normalized by the number of CPU cores), thread counts, and memory usage.

3. **Data Logging:**
   - The collected data is appended to a CSV file (`cpuzoom.csv`) for later analysis.
   - The code uses a slight delay between measurements to ensure accurate CPU usage calculation.

### The Code

```python
# Import the required libraries
import psutil
import time
import csv

# Initialize iteration counter and CSV header fields
x_value = 0
fields = ['x_value', 'ProcessID', 'ProcessNAME', 'ProcessSTATUS', 'ProcessCPU', 'ProcessNUM_THREADS', 'Process_MEMORY(MB)']

# Continuous monitoring loop
while True:
    Proc_name = 'Zoom'  # Change this string to monitor a different meeting application
    proc_list = []

    # Iterate over running processes and filter by the target application name
    for process in psutil.process_iter():
        try:
            if Proc_name in process.name():
                proc = psutil.Process(process.pid)
                # Activate cpu_percent() (first call returns 0.0)
                proc.cpu_percent()
                proc_list.append(proc)
        except psutil.NoSuchProcess:
            pass

    # Dictionary to hold CPU usage per process (normalized per CPU core)
    resource_usage = {}
    time.sleep(0.1)  # Short delay for accurate measurement

    for proc in proc_list:
        resource_usage[proc] = proc.cpu_percent() / psutil.cpu_count()

    # Sort processes by CPU usage and select the top 200
    sorted_usage = sorted(resource_usage.items(), key=lambda x: x[1])[-200:]
    sorted_usage.reverse()

    # Fetch detailed metrics and store in Table1
    Table1 = []
    for proc, cpu_percent in sorted_usage:
        try:
            with proc.oneshot():
                Table1.append([
                    x_value,
                    str(proc.pid),
                    proc.name(),
                    proc.status(),
                    f'{cpu_percent:.2f}%',
                    proc.num_threads(),
                    f'{proc.memory_info().rss / 1e6:.3f}'
                ])
        except psutil.NoSuchProcess:
            pass

    # Print collected data to console
    print(Table1)

    # Append data to a CSV file for later analysis
    with open('cpuzoom.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(Table1)

    x_value += 1
    time.sleep(1)  # 1-second delay before next iteration

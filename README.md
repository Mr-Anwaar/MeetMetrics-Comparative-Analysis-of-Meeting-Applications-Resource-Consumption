# Comparative Analysis of Meeting Applications Based on Resource Usage

## Overview

This research project evaluates the computational resource consumption of various meeting applications (such as Zoom, Skype, and TeamViewer) to determine which one operates most efficiently during real-time communication sessions. The tool uses Python scripts to monitor system processes, capture CPU, memory, and thread data, and log the information into CSV files for further analysis.

The repository includes:
- The Python monitoring script.
- Sample CSV output data.
- Jupyter notebooks (or additional scripts) to generate comparison tables and graphs.
- Documentation of the experimental setup and methodology.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Methodology](#methodology)
- [Comparison Table and Graphs](#comparison-table-and-graphs)
- [Installation and Usage](#installation-and-usage)
- [Results](#results)
- [Future Work](#future-work)
- [License](#license)
- [Contact](#contact)

## Features

- **Real-Time Monitoring:** Continuously monitors CPU, memory, thread count, and process status of targeted meeting applications.
- **Process Filtering:** Easily filter and select different meeting applications (e.g., Zoom, Skype) by changing a configuration variable.
- **Data Logging:** Writes performance metrics to a CSV file (`cpuzoom.csv`) for detailed analysis.
- **Efficient Data Retrieval:** Utilizes the `psutil` library’s `oneshot()` method to reduce the overhead of multiple system calls.
- **Comparative Analysis:** Enables comparison of total, average, and peak resource usage across multiple meeting applications.

## Methodology

1. **Toolset and Libraries:**
   - **Python:** Primary language for scripting and data collection.
   - **psutil:** For retrieving system and process information.
   - **csv:** For writing the captured data in CSV format.
   - **time:** For controlling sampling intervals.

2. **Data Collection:**
   - The script runs an infinite loop that continuously samples the resource usage of processes filtered by application name.
   - Each iteration collects metrics such as Process ID, Process Name, Process Status, CPU usage (normalized per CPU core), number of threads, and memory usage in MB.
   - The collected data is appended to a CSV file for post-session analysis.

3. **Experiment Setup:**
   - **Idle Session:** Applications are launched and left idle.
   - **Active Session:** Applications are used actively (e.g., initiating video calls, using background effects) to simulate real-world usage.
   - Data from both sessions are analyzed to compare the efficiency of different meeting applications.

## Comparison Table and Graphs

### Comparison Table

After data collection, the following key metrics are computed and tabulated for each application:

| **Process ID** | **Process Name**       | **Total CPU Usage (%)** | **Average CPU Usage (%)** | **Peak CPU Usage (%)** | **Total Memory (MB)** | **Total Threads** |
|----------------|------------------------|-------------------------|---------------------------|------------------------|-----------------------|-------------------|
| 2692           | Zoom.exe               | 104.57                  | 17.22                     | 99.13                  | 401500.33             | 12840             |
| 1028           | SkypeBridge.exe        | 0.54                    | 0.54                      | 0.54                   | 68706.27              | 12840             |
| ...            | ...                    | ...                     | ...                       | ...                    | ...                   | ...               |

*Note:* The above values are sample data from a test session. Actual values may vary based on system configuration and session activity.

### Graphs

The following graphs are generated from the CSV data using a Jupyter Notebook (or your preferred data visualization tool):

- **Total Resource Consumption Graph:**  
  This bar graph displays the cumulative CPU and memory usage per process. It clearly shows which primary processes (like `Zoom.exe` or `SkypeApp.exe`) are the most resource-intensive.
  
- **Average Resource Usage Chart:**  
  This line or bar chart highlights the average CPU usage of each process during the session, offering insights into the baseline resource requirements.
  
- **Peak Resource Usage Plot:**  
  A scatter or line plot illustrates the maximum CPU and memory usage recorded for each process, indicating the load experienced during intensive usage.

*Graph examples and notebooks can be found in the `/analysis` folder of this repository.*

## Installation and Usage

### Prerequisites

- **Python 3.9+**
- Required Python libraries:
  - `psutil`
  - `csv` (built-in)
  - `time` (built-in)

You can install `psutil` using pip:

```bash
pip install psutil

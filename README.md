# MeetMetrics: Comparative Analysis of Meeting Applications' Resource Consumption

**MeetMetrics** is a research project that compares the computational and network resource usage of various online meeting applications—including TeamViewer, Skype, VooV, and Zoom—to determine their efficiency in real-time communication and online educational environments. This project provides insights for selecting the best tool for users with limited computational power.

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Monitoring an Application](#monitoring-an-application)
  - [Visualizing the Data](#visualizing-the-data)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mr-Anwaar/MeetMetrics-Comparative-Analysis-of-Meeting-Applications-Resource-Consumption.git
    cd MeetMetrics-Comparative-Analysis-of-Meeting-Applications-Resource-Consumption
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

This project provides two main scripts: `monitor.py` for collecting data and `visualize.py` for generating comparison graphs.

### Monitoring an Application

The `monitor.py` script allows you to track the CPU, memory, and network usage of any application, even if it runs under multiple process names.

1.  **Identify all process names** associated with the application you want to monitor. For example, Zoom runs processes under both `Zoom` and `zwebview`.
2.  **Run the script** from your terminal, providing an output file path and a list of all process names to monitor:
    ```bash
    python monitor.py <output_file.csv> <process_name_1> <process_name_2> ...
    ```
    For example, to accurately monitor Zoom, you should track both of its main processes like this:
    ```bash
    python monitor.py zoom_data.csv Zoom zwebview
    ```
3.  **Let the script run** while you use the application. Press `Ctrl+C` to stop monitoring.

### Visualizing the Data

Once you have collected data for multiple applications, you can use the `visualize.py` script to generate comparison graphs.

1.  **Run the script** from your terminal, providing the paths to the CSV files you want to compare:
    ```bash
    python visualize.py <file1.csv> <file2.csv> ...
    ```
    For example, to compare the data from `zoom_data.csv` and `skype_data.csv`, you would run:
    ```bash
    python visualize.py zoom_data.csv skype_data.csv
    ```
2.  The script will generate bar charts comparing the average CPU usage, memory consumption, and number of threads for each application. The graphs will be saved in the `graphs` directory by default.

---

## Project Structure

The project has the following structure:

-   `monitor.py`: The main script for monitoring application resource usage.
-   `visualize.py`: The script for generating comparison graphs from the collected data.
-   `requirements.txt`: A file listing the project's dependencies.
-   `graphs/`: The default directory where the output graphs are saved.
-   `README.md`: This file.

---

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

---

## Contact

For any questions or feedback, please contact:

-   **Muhammad Anwaar**
-   **LinkedIn:** [https://www.linkedin.com/in/muhammad-anwaar-7a1221214](https://www.linkedin.com/in/muhammad-anwaar-7a1221214)
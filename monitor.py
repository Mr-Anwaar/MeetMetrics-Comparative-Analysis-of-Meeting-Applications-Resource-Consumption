import psutil
import time
import csv
import argparse
from scapy.all import *
from collections import defaultdict
from threading import Thread
import pandas as pd

# Global variables
connectionpid_store = {}
Traffic_Pids = defaultdict(lambda: [0, 0])
program_running = True
all_macs_addrs = {iface.mac for iface in ifaces.values()}

def convert_size(bytes):
    """
    Convert bytes to a human-readable format.
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def packet_process(packet):
    """
    Process each captured packet to calculate network traffic.
    """
    global Traffic_Pids
    try:
        packet_connection = (packet.sport, packet.dport)
    except (AttributeError, IndexError):
        pass
    else:
        packet_pid = connectionpid_store.get(packet_connection)
        if packet_pid:
            if packet.src in all_macs_addrs:
                Traffic_Pids[packet_pid][0] += len(packet)
            else:
                Traffic_Pids[packet_pid][1] += len(packet)

def connection_add():
    """
    Continuously update the mapping of connections to PIDs.
    """
    global connectionpid_store
    while program_running:
        for con in psutil.net_connections():
            if con.laddr and con.raddr and con.pid:
                connectionpid_store[(con.laddr.port, con.raddr.port)] = con.pid
                connectionpid_store[(con.raddr.port, con.laddr.port)] = con.pid
        time.sleep(1)

def monitor_resources(process_names, output_file):
    """
    Monitor CPU, memory, and network usage for a given list of processes.
    """
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'PID', 'Process Name', 'Status', 'CPU %', 'Num Threads', 'Memory (MB)', 'Upload (Bytes)', 'Download (Bytes)'])

    x_value = 0
    while program_running:
        processes_to_monitor = []
        for process in psutil.process_iter(['pid', 'name']):
            # Check if any of the target process names are in the current process name
            if any(p_name.lower() in process.info['name'].lower() for p_name in process_names):
                try:
                    p = psutil.Process(process.info['pid'])
                    p.cpu_percent()  # First call returns 0.0
                    processes_to_monitor.append(p)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        time.sleep(1)

        for p in processes_to_monitor:
            try:
                with p.oneshot():
                    cpu_percent = p.cpu_percent() / psutil.cpu_count()
                    upload, download = Traffic_Pids.get(p.pid, [0, 0])

                    with open(output_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            time.time(),
                            p.pid,
                            p.name(),
                            p.status(),
                            f'{cpu_percent:.2f}',
                            p.num_threads(),
                            f'{p.memory_info().rss / 1e6:.3f}',
                            upload,
                            download
                        ])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        x_value += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor system and network resources for specific processes.")
    parser.add_argument("output_file", help="The path to the output CSV file.")
    parser.add_argument("process_names", nargs='+', help="A list of process names to monitor.")
    args = parser.parse_args()

    # Start the network monitoring threads
    connections_thread = Thread(target=connection_add)
    connections_thread.start()
    sniff_thread = Thread(target=sniff, kwargs={'prn': packet_process, 'store': False})
    sniff_thread.start()

    # Start the resource monitoring
    try:
        monitor_resources(args.process_names, args.output_file)
    except KeyboardInterrupt:
        program_running = False
        print("Stopping the monitoring script.")
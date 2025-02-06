import psutil
from scapy.all import *
from collections import defaultdict
import os
from threading import Thread
import pandas as pd

TIME_IN_SECONDS = 1
# for fetching all Processes of software program to monitor
process_name = 'zWebview2Agent'
Proc = None
x_value = 0

for process in [psutil.Process(pid) for pid in psutil.pids()]:
    if process_name in process.name():
        Proc = psutil.Process(process.pid)
# fetching the all network adapter's MAC addresses
all_macs_addrs = {iface.mac for iface in ifaces.values()}
# A dict to map every connection to its corresponding manner ID (PID)
connectionpid_store = {}
# A dictionary to map every manner ID (PID) to general Upload (zero) and Download (1) site visitors
Traffic_Pids = defaultdict(lambda: [0, 0])
# the global Pandas DataFrame used to keep track of earlier traffic statistics
global_dataframe = None
# global boolean for the program's status
program_running = True


def convert_size(bytes):
    """
    To return the length of bytes in a pleasant form
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


def packet_process(packet):
    global Traffic_Pids
    try:
        # obtain the packet source & destination IP addresses and ports
        packet_connection = (packet.sport, packet.dport)
    except (AttributeError, IndexError):
        # occasionally the packet does not have TCP/UDP layers, we specifically skip these packets
        pass
    else:
        # fetch the PID accountable for this connection from our `connectionpid_store` global dict
        packet_pid = connectionpid_store.get(packet_connection)
        if packet_pid:
            if packet.src in all_macs_addrs:
                # the source MAC address of the packet is our MAC address,
                # so it's an outgoing packet, meaning it's upload
                Traffic_Pids[packet_pid][0] += len(packet)
            else:
                # incoming packet, download
                Traffic_Pids[packet_pid][1] += len(packet)


def connection_add():
    """ this function that keeps listening for connections on this machine
    and adds them to `connectionpid_store` global variable"""
    global connectionpid_store
    while program_running:
        # using psutil, we can grab each connection's source and destination ports
        # and their process ID
        for con in psutil.net_connections():
            if con.laddr and con.raddr and con.pid:
                # if local address, remote address and PID are in the connection
                # add them to our global dictionary
                connectionpid_store[(con.laddr.port, con.raddr.port)] = con.pid
                connectionpid_store[(con.raddr.port, con.laddr.port)] = con.pid
        # sleep for a second, feel free to adjust this
        time.sleep(1)


def print_pid2traffic():
    global global_dataframe
    # initialize the list of processes
    processes = []
    for pid, traffic in Traffic_Pids.items():
        # `pid` is an integer that represents the Process ID
        # `traffic` is a list of two values: total Upload and Download size in bytes
        try:
            # get the Process object from psutil
            Proc
        except psutil.NoSuchProcess:
            # if Process is not found, simply continue to the next PID for now
            continue
        # get the name of the Process, such as chrome.exe, etc.
        name = Proc.name()
        # get the time the Process was spawned
        try:
            create_time = datetime.fromtimestamp(Proc.create_time())
        except OSError:
            # system processes, using boot time instead
            create_time = datetime.fromtimestamp(psutil.boot_time())
        # construct our dictionary that stores Process info
        Process = {
            "x_value": x_value, "pid": pid, "name": name, "create_time": create_time, "Upload": traffic[0],
            "Download": traffic[1],
        }
        try:
            # calculate the upload and download speeds by simply subtracting the old stats from the new stats
            Process["Upload Speed"] = traffic[0] - global_dataframe.at[pid, "Upload"]
            Process["Download Speed"] = traffic[1] - global_dataframe.at[pid, "Download"]
        except (KeyError, AttributeError):
            # If it's the first time running this function, then the speed is the current traffic
            # You can think of it as if old traffic is 0
            Process["Upload Speed"] = traffic[0]
            Process["Download Speed"] = traffic[1]
        # append the Process to our processes list
        processes.append(Process)
    # construct our Pandas DataFrame
    dataframe = pd.DataFrame(processes)
    try:
        # set the PID as the index of the dataframe
        dataframe = dataframe.set_index("x_value", drop=False)
        # sort by column, feel free to edit this column
        dataframe.sort_values("Download", inplace=True, ascending=False)
    except KeyError as e:
        # when dataframe is empty
        pass
    # make another copy of the dataframe just for fancy printing
    printing_dataframe = dataframe.copy()
    try:
        # apply the function get_size to scale the stats like '532.6KB/s', etc.
        printing_dataframe["Download"] = printing_dataframe["Download"].apply(convert_size)
        printing_dataframe["Upload"] = printing_dataframe["Upload"].apply(convert_size)
        printing_dataframe["Download Speed"] = printing_dataframe["Download Speed"].apply(convert_size).apply(
            lambda s: f"{s}/s")
        printing_dataframe["Upload Speed"] = printing_dataframe["Upload Speed"].apply(convert_size).apply(
            lambda s: f"{s}/s")

    except KeyError as e:
        # when dataframe is empty again
        pass
    # clear the screen based on your OS
    os.system("cls") if "nt" in os.name else os.system("clear")
    # print our dataframe

    # print function
    print(printing_dataframe.to_string())
    printing_dataframe.to_csv('intZoom2.csv', mode='a', index=False, header=False)
    # update the global dataframe to our dataframe
    global_dataframe = dataframe


def status_print():
    """Simple function that keeps printing the stats"""
    while program_running:
        time.sleep(TIME_IN_SECONDS)
        print_pid2traffic()
        global x_value
        x_value += 1


if __name__ == "__main__":
    # start the printing thread
    print_thread = Thread(target=status_print)
    print_thread.start()
    # start the get_connections() function to update the current connections of this machine
    connections_thread = Thread(target=connection_add)
    connections_thread.start()
    # start sniffing
    print("Sniffing Started")
    sniff(prn=packet_process, store=False)
    # setting the global variable to False to exit the program
    program_running = False
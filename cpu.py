# Import the required libraries
import psutil
import time
import csv

x_value = 0

# In order to continuously check on the System, this (while True:) expression executes an infinite loop
while True:
    Proc_name = 'Zoom'
    Proc = None

    #  This code obtains the processes from the available processes that have the highest CPU usage for Proc_name.

    Table1 = []
    proc = []
    # Obtain the pids of the Software from which mostly are user processes
    for process in psutil.process_iter():
        try:
            if Proc_name in process.name():
                Proc = psutil.Process(process.pid)
                # activate cpu_percent() the first time, which leads to a return of 0.0
                Proc.cpu_percent()
                proc.append(Proc)

        except psutil.NoSuchProcess:
            pass
    # sort by cpu_percent
    time.sleep(0.1)
    Parry = {}
    for Proc in proc:
        # activates cpu_percent() the second time for computation
        Parry[Proc] = Proc.cpu_percent() / psutil.cpu_count()

    Parry_list = sorted(Parry.items(), key=lambda x: x[1])
    Parry200 = Parry_list[-200:]
    Parry200.reverse()

    for Proc, cpu_percent in Parry200:
        # Some subprocesses may exit during process acquisition.
        # So you need to put this code in a try-except block to handle exceptions.
        try:
            # Use Oneshot to improve  efficiency when retrieving information
            with Proc.oneshot():
                Table1.append([
                    x_value, str(Proc.pid), Proc.name(), Proc.status(),
                    f'{cpu_percent:.2f}' + "%", Proc.num_threads(), f'{Proc.memory_info().rss / 1e6:.3f}'
                ])

        except psutil.NoSuchProcess:
            pass

    print(Table1)

    with open('cpuzoom.csv', 'a') as f:

        # use the csv.writer method from the CSV package
        write = csv.writer(f)
        write.writerows(Table1)
    x_value += 1
    # Create a 1-second delay
    time.sleep(1)

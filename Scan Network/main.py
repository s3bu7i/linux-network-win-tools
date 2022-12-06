import sys
import timeit
from tkinter import *
from tkinter import ttk


from startswith import allow_ip_address as allow_ip_address_startswith
from net import allow_ip_address as allow_ip_address_net
from netlist import allow_ip_address as allow_ip_address_netlist

ipaddress = sys.argv[1]

print(allow_ip_address_startswith(ipaddress))
print (allow_ip_address_net(ipaddress))
print (allow_ip_address_netlist(ipaddress))

def benchmark(fn, number):
    time_per_run = timeit.timeit(f"{fn}('{ipaddress}')", globals=globals(),
                                 number = number) / number

    time_per = f"{time_per_run:.20f}"
    time_in_microseconds = round(float(time_per)*1000000, 2)
    executions_per_second = f"{round(1/float(time_per)):,}"

    results = f"""
[{fn}]
Time per run i seconds: {time_per} ({time_in_microseconds} microseconds)
Executions per second: {executions_per_second}
"""
    print(results)

    return None

benchmark("allow_ip_address_startswith", 1000)
benchmark("allow_ip_address_net",1000)
benchmark("allow_ip_address_netlist",10)




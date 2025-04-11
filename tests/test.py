import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading


class PerformanceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Performance Monitor")
        self.root.geometry("1200x800")

        # Initialize variables
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []
        self.network_usage = []
        self.update_interval = 1  # in seconds

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Dashboard")
        self.tab_control.add(self.tab2, text="Processes")
        self.tab_control.add(self.tab3, text="Historical Data")
        self.tab_control.pack(expand=1, fill="both")

        # Dashboard Tab
        self.create_dashboard_tab()

        # Processes Tab
        self.create_processes_tab()

        # Historical Data Tab
        self.create_historical_data_tab()

        # Start monitoring
        self.monitor_performance()

    def create_dashboard_tab(self):
        # CPU Usage
        self.cpu_label = ttk.Label(self.tab1, text="CPU Usage: 0%")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=10)

        # Memory Usage
        self.memory_label = ttk.Label(self.tab1, text="Memory Usage: 0%")
        self.memory_label.grid(row=1, column=0, padx=10, pady=10)

        # Disk Usage
        self.disk_label = ttk.Label(self.tab1, text="Disk Usage: 0%")
        self.disk_label.grid(row=2, column=0, padx=10, pady=10)

        # Network Usage
        self.network_label = ttk.Label(self.tab1, text="Network Usage: 0 KB/s")
        self.network_label.grid(row=3, column=0, padx=10, pady=10)

    def create_processes_tab(self):
        self.process_tree = ttk.Treeview(self.tab2, columns=(
            "PID", "Name", "CPU%", "Memory%"), show="headings")
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Name", text="Name")
        self.process_tree.heading("CPU%", text="CPU%")
        self.process_tree.heading("Memory%", text="Memory%")
        self.process_tree.pack(expand=1, fill="both")

        self.kill_button = ttk.Button(
            self.tab2, text="Kill Process", command=self.kill_process)
        self.kill_button.pack(pady=10)

        self.update_processes()

    def create_historical_data_tab(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab3)
        self.canvas.get_tk_widget().pack(expand=1, fill="both")

    def monitor_performance(self):
        def update():
            while True:
                # CPU Usage
                cpu_percent = psutil.cpu_percent(interval=self.update_interval)
                self.cpu_usage.append(cpu_percent)
                self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

                # Memory Usage
                memory_info = psutil.virtual_memory()
                memory_percent = memory_info.percent
                self.memory_usage.append(memory_percent)
                self.memory_label.config(
                    text=f"Memory Usage: {memory_percent}%")

                # Disk Usage
                disk_usage = psutil.disk_usage('/').percent
                self.disk_usage.append(disk_usage)
                self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

                # Network Usage
                net_io = psutil.net_io_counters()
                network_usage = (net_io.bytes_sent + net_io.bytes_recv) / 1024
                self.network_usage.append(network_usage)
                self.network_label.config(
                    text=f"Network Usage: {network_usage:.2f} KB/s")

                # Update historical data plot
                self.update_historical_data()

                # Update processes
                self.update_processes()

                time.sleep(self.update_interval)

        threading.Thread(target=update, daemon=True).start()

    def update_processes(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                self.process_tree.insert("", "end", values=(
                    proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent']))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def kill_process(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            pid = self.process_tree.item(selected_item, "values")[0]
            try:
                psutil.Process(int(pid)).terminate()
                messagebox.showinfo(
                    "Success", f"Process {pid} terminated successfully.")
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "Process not found.")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "Access denied.")
        else:
            messagebox.showwarning(
                "Warning", "Please select a process to kill.")

    def update_historical_data(self):
        self.ax.clear()
        self.ax.plot(self.cpu_usage, label="CPU Usage")
        self.ax.plot(self.memory_usage, label="Memory Usage")
        self.ax.plot(self.disk_usage, label="Disk Usage")
        self.ax.plot(self.network_usage, label="Network Usage")
        self.ax.legend()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Usage (%)")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceMonitor(root)
    root.mainloop()

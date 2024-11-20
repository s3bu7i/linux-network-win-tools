import requests
import threading
import time
from .models import NetworkMonitorDB


def update_record(id, status):
    record = NetworkMonitorDB.objects.get(id=id)
    record.status = status
    record.save()


def update_latency(id, latency):
    record = NetworkMonitorDB.objects.get(id=id)
    record.latency = latency
    record.save()


def start_ping():
    while True:
        list_data = NetworkMonitorDB.objects.all()

        for item in list_data:
            try:
                start_time = time.time()
                response = requests.get(item.url, timeout=5)
                end_time = time.time()
                if response.status_code == 200:
                    print("POST request successful")
                    update_record(item.id, response.status_code)
                else:
                    print("POST request failed")
                    print("Status code:", response.status_code)
                    update_record(item.id, response.status_code)

                latency_ms = (end_time - start_time) * 1000
                formatted_latency = f"{latency_ms:.1f} ms"
                update_latency(item.id, formatted_latency)
                print("Latency:", formatted_latency)
            except requests.Timeout:
                print("POST request timed out (502 error)")
                update_record(item.id, 502)
                update_latency(item.id, "9999 ms")
            except:
                update_record(item.id, 404)
                update_latency(item.id, "9999 ms")

        # time.sleep(1)


threading.Thread(target=start_ping).start()

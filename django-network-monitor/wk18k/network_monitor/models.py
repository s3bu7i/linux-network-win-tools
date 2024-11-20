from django.db import models


class NetworkMonitorDB(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    status = models.CharField(max_length=100, default="400", auto_created=True)
    latency = models.CharField(max_length=100, default=0)

    def __str__(self):
        return f"{self.name} {self.url} {self.status}"

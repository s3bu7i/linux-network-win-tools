from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('network-monitor/', include("network_monitor.urls")),
    path('users/', include("users.urls")),
    path('', include("home.urls")),
]

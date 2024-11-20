from django.urls import path
from . import views

app_name = "network_monitor"

urlpatterns = [
    path("", views.index, name="index"),
    path("remove_data/<int:id>", views.remove_data, name="remove_data"),
    path("add_data/", views.add_data, name="add_data"),
    path('table_data/', views.table_data_view, name='table_data'),
    path('update_data/<int:id>', views.update_data, name='update_data'),
]

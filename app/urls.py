from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('working/', views.working, name='working'),
    path('send_capture/', views.send_capture(), name='send_capture'),
    path('finish_task/', views.finish_task, name='finish_task')
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL pattern for the home view
    path('results/', views.show_results, name='show_results'),
    path('run_all/', views.run_all, name='run_all'),
    path('check_log_step/', views.check_log_step, name='check_log_step'),
]


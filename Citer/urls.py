from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),      # URL pattern for the home view
    path('run_all/', views.run_all, name='run_all'),  # URL pattern for the run_all view
]

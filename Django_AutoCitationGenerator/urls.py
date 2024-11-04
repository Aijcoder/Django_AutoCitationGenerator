from django.contrib import admin
from django.urls import path, include  # Include is imported here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Citer.urls')),  # Include the URL patterns from Citer app
]

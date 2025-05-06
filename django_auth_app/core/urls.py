from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_auth_app.myapp.urls')),
    
# Use just the app name here, not the full Python path

]

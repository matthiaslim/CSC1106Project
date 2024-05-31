"""
URL configuration for CSC1106Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from csc1106app import views as hrms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hrms_views.home_page, name='home_page'),  # Main page URL
    path('hrms_main/', hrms_views.hrms_main, name='hrms_main'),  # HRMS home URL
    path('hrms/', include('hrms.urls')),  # Include HRMS app URLs
]

"""
URL configuration for aspire project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

# admin.autodiscover()
# admin.site.site_header = "Aspire Admin Panel"
# admin.site.index_title = "Aspire"
# admin.site.site_title = "Aspire Loan Panel"

urlpatterns = [

    path('aspire-super-admin/', admin.site.urls),

    path('admin/', include('admin_honeypot.urls')),

    path('api/profile/', include((
        'aspireprofile.api.urls', 'aspireprofile'), namespace='profile_api')),

    path('api/loan/', include((
        'aspireloan.api.urls', 'aspireloan'), namespace='loan_api'))
]

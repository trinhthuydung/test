"""demooo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path, include
from dungdung import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', views.registration),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z]_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name = 'activate'),
    # url(r'^active/')
    # path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name = 'activate'),
    path('login', views.login1, name = 'login'),
    path('home', views.home, name = 'home'),
    path('input', views.input, name='input'),
    path('myform', views.myform, name='myform')
]

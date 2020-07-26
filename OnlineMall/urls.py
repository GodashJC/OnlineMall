"""OnlineMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from app1.views import *
from app1.models import Shangpin
admin.site.register(Shangpin)

urlpatterns = [
    path("",shouye,name='shouye'),
    path('admin/', admin.site.urls),
    path('reg/',Reg.as_view(),name='reg'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',logout,name='logout'),
    path('edit_user/',Edit_user.as_view(),name='edit_user'),
    re_path('index/(\d+)/',index,name="index"),
    re_path('gooddetails/(\d+)/',gooddetails,name="gooddetails"),
    re_path('add2cart/(\d+)/',add2cart,name="add2cart"),
    re_path('sub2cart/(\d+)/',sub2cart,name="sub2cart"),
    path('add2order/',add2order,name="add2order"),
    path('showorder/',showorder,name="showorder"),
    re_path('deleteorder/(\d+)/',deleteorder,name="deleteorder"),
    re_path('pay/(\d+)',Pay.as_view(),name="pay")


]


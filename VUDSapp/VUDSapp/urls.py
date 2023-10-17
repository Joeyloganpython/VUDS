"""VUDSapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
#from vuapp.views import new_flowsheet,
from vuapp import views
#from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index,name="index"),
    path("new_flowsheet/",views.new_flowsheet,name="new_flowsheet"),
    path("flow_result/",views.flow_result,name="flow_result"),
    path("upload_text_file/",views.upload_text_file,name="upload_text_file"),
    path("textfileresult/",views.textfileresult,name="textfileresult"),
    path("upload_dicom_file/",views.upload_dicom_file,name="upload_dicom_file"),
    path("dicomresult/",views.dicomresult,name="dicomresult")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
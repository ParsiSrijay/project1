from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signup,name ='signup'),
    path('display',views.display,name='display'),
    path('install',views.payinstallments,name='install'),
]

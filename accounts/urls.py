from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.first,name ='first'),
    path('display',views.disp,name="display"),
    path('accounts',views.allAcc,name="Accounts"),
    path('RandP',views.RandPDisplay,name="randp"),
    path('IandE',views.IandEDisplay,name="iande"),
    path('Bals',views.BalSheetDisp,name="balsheet")
]

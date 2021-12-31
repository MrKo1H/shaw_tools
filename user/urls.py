from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.home,name="home"),
	path('pay/', views.pay,name="pay"),
	path('user/info', views.info, name = "info"),
	path('refund/', views.refund, name="refund"),	
	path('device/', views.device, name="device")
]
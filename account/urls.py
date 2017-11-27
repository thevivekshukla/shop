from django.conf.urls import url

from account import views



urlpatterns = [
    url(r'^signup/$', views.RegisterUserAPIView.as_view(), name='signup'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', views.UserLogoutAPIView.as_view(), name='logout'),
]

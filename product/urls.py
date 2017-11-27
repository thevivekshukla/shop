from django.conf.urls import url

from product import views



urlpatterns = [
    url(r'^items/$', views.ItemView.as_view(), name='items'),
    url(r'^buy/(?P<pk>\d+)/$', views.BuyItemView.as_view(), name='buy'),
    url(r'^rate/(?P<pk>\d+)/$', views.ProductRateView.as_view(), name='rate'),
]

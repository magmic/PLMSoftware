from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# ex: /polls/5/
	url(r'^products/(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /polls/5/results/
	url(r'^(?P<product_id>[0-9]+)/results/$', views.results, name='results'),
	# ex: /polls/5/vote/
	url(r'^(?P<product_id>[0-9]+)/vote/$', views.vote, name='vote'),

	url(r'^products/$', views.productList, name='products'),
	url(r'^suppliers/$', views.supplierList, name='suppliers'),
	url(r'^offers/$', views.offerList, name='offers'),
	url(r'^orders/$', views.orderList, name='orders'),
	#url(r'^orders/add/$', views.orderList, name='addOrder'),
	url(r'^base/$', views.base, name='base'),
]
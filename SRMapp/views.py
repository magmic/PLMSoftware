from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import *

# Create your views here.
def index(request):
	latest_product_list = Product.objects.order_by('-name')[:5]
	#template = loader.get_template('SRMapp/index.html')
	context = {'latest_product_list': latest_product_list}
	return render(request, 'SRMapp/index.html', context)
	#context = RequestContext(request, {
	#	'latest_product_list': latest_product_list,
	#})
	#return HttpResponse(template.render(context))


def detail(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request, 'SRMapp/detail.html', {'product': product})

def results(request, product_id):
	response = "You're looking at the results of product %s."
	return HttpResponse(response % product_id)

def vote(request, product_id):
	return HttpResponse("You're voting on product %s." % product_id)


def productList(request):
	product_list = Product.objects.order_by('-name')[:100]
	context = {'product_list': product_list, 'productsOn': "1"}
	return render(request, 'SRMapp/productList.html', context)

def supplierList(request):
	supplier_list = Supplier.objects.order_by('-name')[:100]
	context = {'supplier_list': supplier_list, 'suppliersOn': "1"}
	return render(request, 'SRMapp/supplierList.html', context)

def offerList(request):
	offer_list = Offer.objects.order_by('-product')[:100]
	product_list = Product.objects.order_by('-name')[:100]
	supplier_list = Supplier.objects.order_by('-name')[:100]
	context = {'offer_list': offer_list, 'product_list': product_list, 'supplier_list': supplier_list, 'offersOn': "1"}
	return render(request, 'SRMapp/offerList.html', context)

def orderList(request):
	order_list = Order.objects.order_by('-product')[:100]
	offer_list = Offer.objects.order_by('-product')[:100]
	context = {'order_list': order_list, 'offer_list': offer_list, 'ordersOn': "1"}
	return render(request, 'SRMapp/orderList.html', context)


def base(request):
	return render(request, 'SRMapp/base.html')
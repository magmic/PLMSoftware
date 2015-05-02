from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import Product

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
	latest_product_list = Product.objects.order_by('-name')[:15]
	context = {'latest_product_list': latest_product_list}
	return render(request, 'SRMapp/productList.html', context)
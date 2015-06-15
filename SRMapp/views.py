from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json as simplejson
import random
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
	pr = get_object_or_404(Product, pk=product_id)
	supplier_list = Supplier.objects.order_by('-name')[:100]
	supList = []
	r = lambda: random.randint(0,255)
	for s in supplier_list:
		a = Order.objects.filter(product = pr, supplier = s).aggregate(quantity_sum=Sum('quantity'))
		#supList.append({'name': s.name, 'sum': a['quantity_sum']})
		#supList.append({'value': a['quantity_sum']})
		#supList.append({'color': "#F7464A" })
		#supList.append({'highlight': "#FF5A5E"})
		#supList.append({'label': s.name})
		#quantity = '0'
		#if a['quantity_sum']:
		#	quantity = str(a['quantity_sum'])
		#supList.append({'value': quantity, 'color': ('#%02X%02X%02X' % (r(), r(), r())), 'highlight': "#5A5A5A", 'label': s.name})
		if a['quantity_sum']:
			supList.append({'value': str(a['quantity_sum']), 'color': ('#%02X%02X%02X' % (r(), r(), r())), 'highlight': "#5A5A5A", 'label': s.name})

	#c = Context({'supList': supList})
	js_data = simplejson.dumps(supList)
	return render(request, 'SRMapp/detail.html', {'supList': js_data, 'product': pr})

def results(request, product_id):
	response = "You're looking at the results of product %s."
	return HttpResponse(response % product_id)

def vote(request, product_id):
	return HttpResponse("You're voting on product %s." % product_id)


def productList(request):
	product_list = Product.objects.order_by('-name')[:100]
	#supplier_list = Supplier.objects.order_by('-name')[:100]
	#mapping = []
	#for pr in product_list:
	#	supList = []
	#	for s in supplier_list:
	#		a = Order.objects.filter(product = pr, supplier = s).aggregate(quantity_sum=Sum('quantity'))
	#		supList.append({'name': s.name, 'sum': a['quantity_sum']})
	#	mapping.append({pr.id: supList})#.append((pr, supList))
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

def addOrder(request):
	try:
		newOffer = get_object_or_404(Offer, pk=request.POST['offerId'])
		newOrder = Order(
			product = newOffer.product,
			supplier = newOffer.supplier,
			price = newOffer.price,
			quantity = request.POST['quantity'],
			offer = newOffer
		)
		newOrder.save()
	except:
		return HttpResponse("Invalid data.")
	else:
		return HttpResponseRedirect(reverse('orders'))#HttpResponse("Added new offer %s." % newOffer.id)

def receiveOrder(request):
	#try:
		receivedOrder = get_object_or_404(Order, pk=request.POST['receivedOrderId'])
		receivedOrder.received = True
		receivedOrder.surv_price = request.POST['surv_price']
		receivedOrder.surv_quality = request.POST['surv_quality']
		receivedOrder.surv_delivery_time = request.POST['surv_delivery_time']
		receivedOrder.save()

		order_list = Order.objects.order_by('-product')[:100]
		sumPrice=0
		sumDeliveryTime=0
		sumQuality=0
		count=0
		supplier = receivedOrder.supplier
		for o in Order.objects.filter(received=True, supplier=supplier):
			sumPrice+=o.surv_price
			sumQuality+=o.surv_quality
			sumDeliveryTime+=o.surv_delivery_time
			count+=1

		print("count " + str(count))
		print("count " + str(sumPrice/count))
		print("count " + str(sumQuality/count))
		print("count " + str(sumDeliveryTime/count))
		supplier.surv_price = sumPrice/count
		supplier.surv_quality = sumQuality/count
		supplier.surv_delivery_time = sumDeliveryTime/count

		supplier.save()
	#except:
	#	return HttpResponse("Invalid data.")
	#else:
		return HttpResponseRedirect(reverse('orders'))

def render_to(template):
	def renderer(func):
		def wrapper(request, *args, **kw):
			output = func(request, *args, **kw)
			if isinstance(output, (list, tuple)):
				return render_to_response(output[1], output[0], RequestContext(request))
			elif isinstance(output, dict):
				return render_to_response(template, output, RequestContext(request))
			return output
		return wrapper
	return renderer

@render_to("SRMapp/productList.html")
def getProductInfo(request, product_id):
	pr = Product.objects.get(pk=product_id)
	supplier_list = Supplier.objects.order_by('-name')[:100]
	mapping = []
	supList = []
	for s in supplier_list:
		a = Order.objects.filter(product = pr, supplier = s).aggregate(quantity_sum=Sum('quantity'))
		supList.append({'name': s.name, 'sum': a['quantity_sum']})
	mapping.append({pr.id: supList})
	return {'supList': supList}

@csrf_exempt
def list_posts(request, product_id):
	t = loader.get_template('SRMapp/productList.html')
	pr = Product.objects.get(pk=product_id)
	supplier_list = Supplier.objects.order_by('-name')[:100]
	supList = []
	for s in supplier_list:
		a = Order.objects.filter(product = pr, supplier = s).aggregate(quantity_sum=Sum('quantity'))
		supList.append({'name': s.name, 'sum': a['quantity_sum']})
	c = Context({
        'supList': supList
    })
	return HttpResponse(simplejson.dumps(supList))
	#return render_to_response('SRMapp/productList.html', {'mapping': mapping}, context_instance=RequestContext(request))

@csrf_exempt
def ajax_view(request):
	product_id = request.POST['product_id'] 
	pr = Product.objects.get(pk=product_id)
	supplier_list = Supplier.objects.order_by('-name')[:100]
	supList = []
	for s in supplier_list:
		a = Order.objects.filter(product = pr, supplier = s).aggregate(quantity_sum=Sum('quantity'))
		supList.append({'name': s.name, 'sum': a['quantity_sum']})
	#c = Context({'supList': supList})
	return HttpResponse(simplejson.dumps(supList))

def base(request):
	return render(request, 'SRMapp/base.html')
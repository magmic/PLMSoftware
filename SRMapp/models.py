from django.db import models

# Create your models here.
class  Product(models.Model):
	"""docstring for Product"""
	name = models.CharField(max_length=200)
	unit = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Supplier(models.Model):
	"""docstring for Supplier"""
	name = models.CharField(max_length=200)
	surv_price = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	surv_quality = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	surv_delivery_time = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	def __unicode__(self):
		return self.name

class Offer(models.Model):
	"""docstring for Offer"""
	product = models.ForeignKey(Product)
	supplier = models.ForeignKey(Supplier)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return str(self.product)+" "+str(self.supplier)+" "+str(self.price)

class Order(models.Model):
	"""docstring for Order"""
	product = models.ForeignKey(Product)
	supplier = models.ForeignKey(Supplier)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
	offer = models.ForeignKey(Offer)
	surv_price = models.IntegerField(default=0)
	surv_quality = models.IntegerField(default=0)
	surv_delivery_time = models.IntegerField(default=0)
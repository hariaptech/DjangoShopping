from django.contrib.auth.models import User
from django.db import models
from django import template
import datetime
import os
register = template.Library()
def getFileName(request,fileName):
    now_time= datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_fileName="%s%s"%(now_time,fileName)
    return os.path.join('uploads/',new_fileName)

class Catagory(models.Model):
    name= models.CharField(max_length=150, null=True, blank=True)
    images=models.ImageField(upload_to=getFileName,null=True, blank=True)
    description=models.TextField(max_length=500, null=True, blank=True)
    status=models.BooleanField(default=False, help_text='0-Show,1-Hidden')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name= models.CharField(max_length=150, null=True, blank=True)
    vendor= models.CharField(max_length=150, null=True, blank=True)
    product_images=models.ImageField(upload_to=getFileName,null=True, blank=True)
    quantity=models.IntegerField(null=True, blank=True)
    original_price=models.FloatField(null=True, blank=True)
    selling_price=models.FloatField(null=True, blank=True)
    description=models.TextField(max_length=500, null=True, blank=True)
    status=models.BooleanField(default=False, help_text='0-Show,1-Hidden')
    trending=models.BooleanField(default=False, help_text='0-default,1-Trinding')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Card(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # return self.product_qty
        return self.product.name
    
    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
    

class Favourite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
 
    
    
    
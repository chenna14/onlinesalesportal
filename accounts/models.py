import profile
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.name
  
class Manager(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # gender = models.CharField(max_length= 10, null= True)
    # dob = models.CharField(max_length=20, null= True)

    def __str__(self):
      return self.name
  
class Seller(models.Model):
    user = models.OneToOneField(User,null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "logo.wepg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # city = models.CharField(max_length=200,null=True)
    # zipcode = models.FloatField()

    def __str__(self):
      return self.name
  

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)
    
    def __str__(self):
      return self.name
    
   
class Product(models.Model):
    
    STATUS = {
        ('Indoor' , 'Indoor'),
        ('Outdoor', 'Outdoor'),
    }
    
    Seller = models.ForeignKey(Seller, null= True, blank= True, on_delete= models.SET_NULL)
    name = models.CharField(max_length=200, null= True)
    price = models.FloatField()
    category = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null= True)
    description = models.CharField(max_length=200, null= True)
    # phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(default = "logo.wepg",null=True, blank=True)
    # tags = models.ManyToManyField(Tag)
    
    def __str__(self):
      return self.name
  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
     
    

    
class Order(models.Model):
    
    STATUS = {
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    }
    
    Customer = models.ForeignKey(Customer, null= True, blank= True, on_delete= models.SET_NULL)
    product =  models.ForeignKey(Product, null= True, on_delete= models.SET_NULL)   
    date_created = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length= 200, null= True, choices= STATUS )
    complete = models.BooleanField(default=False, null= True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.Customer)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total;
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total;
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
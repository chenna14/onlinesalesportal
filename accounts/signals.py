# from django.db.models.signals import post_save
# from django.contrib.auth.models import User,Group
# from .models import Customer,Manager,Seller

# def customer_profile(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name = 'customer')
#         instance.groups.add(group)
        
#         Customer.objects.create(
#             user = instance,
#             name = instance.username,
#             # phone = instance.mobile_number
#         )
        

# post_save.connect(customer_profile, sender = User)


# def manager_profile(sender,instance,created,**kwargs):
#    if created:
#         group = Group.objects.get(name = 'manager')
#         instance.groups.add(group)
        
#         Manager.objects.create(
#             user = instance,
#             name = instance.username,
#         )  
  
# post_save.connect(manager_profile, sender = User)

# def seller_profile(sender,instance,created,**kwargs):
#    if created:
#         group = Group.objects.get(name = 'seller')
#         instance.groups.add(group)
        
#         Seller.objects.create(
#             user = instance,
#             name = instance.username,
#         )  
  
# post_save.connect(seller_profile, sender = User)
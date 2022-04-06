from django.urls import path

from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('products/', views.products, name='products'),
     path('customer/<str:test_id>/', views.customer, name='customer'),
     path('create_order/', views.createOrder, name= 'create_order'),
     path('update_order/<str:test_id>',views.updateOrder,name = 'update_order'),
     path('delete_order/<str:test_id>',views.deleteOrder,name = 'delete_order'),
     path('delete_prod/<str:test_id>',views.delete_product,name = 'delete_prod'),
     path('update_prod/<str:test_id>',views.update_prod,name = 'update_prod'),
     path('viewprod/<str:test_id>',views.view_prod,name = 'viewprod'),
     path('sellerview/<str:test_id>',views.seller_view,name = 'sellerview'),
     path('registerpage/',views.registerpage,name = 'register'),
     path('loginpage/',views.loginpage, name = 'login'),
     path('logout/', views.logoutUser, name = 'logout'),
     path('user/',views.userPage,name='user-page'),
     path('account/', views.accountSettings, name = 'account'),
     path('mregister/', views.register_manager, name = 'mregister'),
     path('seller/',views.register_seller, name = 'seller'),
     path('sellerhome/',views.seller_home, name = 'sellerhome'),
     path('sellerinventory/',views.seller_inventory, name = 'sellerinventory'),
     path('selleradditem/',views.seller_additem, name = 'selleradditem'),
     path('selleraccount/',views.seller_account, name = 'selleraccount'),
     path('buyer/', views.buyer, name="buyer"),
     path('item/', views.item, name="item"),
     path('cart/', views.cart, name="cart"),
     path('checkout/', views.checkout, name="checkout"),
     path('updateitem/', views.updateitem, name="updateitem"),
     path('processorder/', views.processorder, name="processorder"),
     path('myaccount/', views.myaccount, name = 'myaccount'),
     path('selleradditem2/',views.addprod, name = 'selleradditem2'),
     path('search/',views.search,name = 'search'),
     path('managerdashboard/', views.managerdashboard, name = 'managerdashboard'),
     path('manageraccount/', views.accountmanager, name = 'manageraccount'),
]


# Register your models here.

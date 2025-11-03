from django.urls import include, path
from . import views

urlpatterns = [
    # DJOSER Y AUTHENTICATION
    path('', include('djoser.urls')),
    
    #GROUPS - Manager
    path("groups/manager/users/", views.managers, name='managers'),
    path("groups/manager/users/<int:userId>", views.manager_delete, name='manager_delete'),
    
    #GROUPS - Delivery crew
    path("groups/delivery-crew/users/", views.delivery_crew , name='delivery-crew'),
    path("groups/delivery-crew/users/<int:userId>", views.delivery_crew_delete, name='delivery-crew-delete'),
    
    #MENU-ITEMS - GET, POST
    path("menu-items/", views.menu_items, name='menu-items'),
    
    #SINGLE-MENU-ITEM - GET, PUT, PATCH, DELETE
    path("menu-items/<int:pk>/", views.single_menu_item, name='single-menu-item'),
    
    #CART
    path("cart/menu-items/", views.cart_items, name='cart'),
    
    #ORDERS
    path("orders/", views.orders, name="orders"),
    
    #SINGLE ORDER
    path("orders/<int:pk>/", views.single_order, name="single-order"),
    
    #CATEGORIES
    path("categories/", views.category, name="categories"),
    
]
    #Functional Endpoints:
    # http://localhost:8000/api/users/
    # http://localhost:8000/api/users/me/
    # http://localhost:8000/api/groups/delivery-crew/users/
    # http://localhost:8000/api/groups/delivery-crew/users/<id>
    # http://localhost:8000/api/groups/manager/users/
    # http://localhost:8000/api/groups/manager/users/<id>
    # http://localhost:8000/api/menu-items/
    # http://localhost:8000/api/menu-items/<id>
    # http://localhost:8000/api/cart/menu-items/
    # http://localhost:8000/api/orders/
    # http://localhost:8000/api/orders/<id>
    # http://localhost:8000/api/categories/


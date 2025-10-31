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
]
    #Functional Endpoints:
    # http://localhost:8000/api/users
    # http://localhost:8000/api/users/me
    # http://localhost:8000/api/groups/delivery-crew/users/
    # http://localhost:8000/api/groups/delivery-crew/users/<id>
    # http://localhost:8000/api/groups/manager/users/
    # http://localhost:8000/api/groups/manager/users/<id>


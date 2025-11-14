from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import ManagerGroupSerializer,DeliveryCrewSerializer, MenuItemsSerializer, CategoriesSerializer
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.response import Response

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
         if not request.user.is_authenticated:
             return False
         return request.user.groups.filter(name='Manager')
     
class OnlyManagerCanCreate(BasePermission):
    def has_permission(self, request, view):
        allow_methods = ["POST", "PUT", "PATCH", "DELETE"]
        if request.method in allow_methods:
            return request.user.groups.filter(name="Manager").exists()
        return True

class AssingManagersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = ManagerGroupSerializer
    permission_classes = [CustomPermission]
    
class DeleteManagerView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name = 'Manager')
    permission_classes = [CustomPermission]
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        manager_group= Group.objects.get(name='Manager')
        user.groups.remove(manager_group)
        
        return Response({"message": "User removed from manager group"}, status=status.HTTP_200_OK)
    
class AssingDeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    serializer_class = DeliveryCrewSerializer
    permission_classes = [CustomPermission]
    
class DeleteDeliveryCrew(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    permission_classes = [CustomPermission]
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        delivery_crew = Group.objects.get(name='Delivery crew')
        user.groups.remove(delivery_crew)
        
        return Response({'message':'User removed from Delivery crew group'}, status=status.HTTP_200_OK)
    
class MenuItemsClassView(viewsets.ModelViewSet):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [ OnlyManagerCanCreate, AllowAny]
    
class CategoriesClassView(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [OnlyManagerCanCreate, AllowAny]
    
    
        
    
        
    

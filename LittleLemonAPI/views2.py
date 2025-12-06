from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import ManagerGroupSerializer,DeliveryCrewSerializer, MenuItemsSerializer, CategoriesSerializer, CartSerializer, OrderSerializer, ManagerUpdateOrderSerializer, DeliveryUpdateOrderSerializer
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response

#Permissions
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
    
class OnlyStaffCanUpdate(BasePermission):
    def has_permission(self, request, view):
        allow_methods = ['PATCH']
        if request.method in  allow_methods:
            return request.user.groups.filter(name__in=["Manager","Delivery crew"]).exists()
        return True
    
class DeleteOrdersPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        allow_methods = ['DELETE']
        if request.method in allow_methods:
            if request.user.groups.filter(name='Delivery crew').exists():
                return False
            
            if request.user.groups.filter(name='Manager').exists():
                return True
            
            return obj.user == request.user
        return True
#Managers
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
    
    
#Delivery Crew
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
    
#Menu Items
class MenuItemsClassView(viewsets.ModelViewSet):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [ OnlyManagerCanCreate, AllowAny]
    
#Categories
class CategoriesClassView(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [OnlyManagerCanCreate, AllowAny]
    
#Cart
class CartClassView(generics.ListCreateAPIView):
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)
    
    def delete(self, request, *args, **kwargs):
        queryset =Cart.objects.filter(user = request.user)
        queryset.delete()
        return Response({'message':'The cart cleaned successfully'}, status=status.HTTP_200_OK)
    
#Order
class OrderClassView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew = user)
        
        return Order.objects.filter(user=user)
    
    serializer_class= OrderSerializer
    
    
class SimpleOrderClassView(generics.RetrieveAPIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self, **kwargs):
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():     
            return Order.objects.filter(delivery_crew = user)       
        return Order.objects.filter(user=user)
    
    
class SimpleOrderUpdateClass(generics.UpdateAPIView):
    permission_classes = [OnlyStaffCanUpdate]

    def get_serializer_class(self):
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            return ManagerUpdateOrderSerializer   
        return DeliveryUpdateOrderSerializer
    
    def get_queryset(self, **kwargs):
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():     
            return Order.objects.filter(delivery_crew = user)
        
class DeleteOrderClass(generics.DestroyAPIView):
    permission_classes = [DeleteOrdersPermissions]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name="Manager").exists():
            return Order.objects.all()
        
        return Order.objects.filter(user=user)
    
    
      


    
        
    
        
    

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import MenuItem, Category

# Create your views here.

# Managers
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def managers(request):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Unautorized'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        managers = User.objects.filter(groups__name = 'Manager')
        managers_data = [{'id': m.id, 'username': m.username, 'email': m.email}for m in managers]
        return Response(managers_data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        username = request.data.get("username")
        user = get_object_or_404(User , username=username)
        manager_group = Group.objects.get(name='Manager')
        user.groups.add(manager_group)
        
        return Response({'message':'User Added to Manager group'}, status=status.HTTP_201_CREATED)
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def manager_delete(request, userId):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Unautorized'}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, pk=userId)
    manager_group = Group.objects.get(name='Manager')
    user.groups.remove(manager_group)
    
    return Response({'message':'User removed from Managers Group'}, status=status.HTTP_200_OK)

# Delivery Crew
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Unautorized'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        crew = User.objects.filter(groups__name = 'Delivery crew')
        crew_data = [{'id': c.id, 'username': c.username, 'email': c.email}for c in crew]
        return Response(crew_data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        username = request.data.get("username")
        user = get_object_or_404(User , username=username)
        crew_group = Group.objects.get(name='Delivery crew')
        user.groups.add(crew_group)
        
        return Response({'message':'User Added to Delivery crew group'}, status=status.HTTP_201_CREATED)
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delivery_crew_delete(request, userId):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Unautorized'}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, pk=userId)
    crew_group = Group.objects.get(name='Delivery crew')
    user.groups.remove(crew_group)
    
    return Response({'message':'User removed from Delivery crew Group'}, status=status.HTTP_200_OK)


# Menu items views - General
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        menu_items_data = [
            {
                'id':item.id,
                'tittle':item.tittle,
                'price':str(item.price),
                'featured':item.featured,
                'category': item.category.id
            }
            for item in menu_items
        ]
        return Response(menu_items_data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Unautorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'POST':
            items_data = request.data if isinstance(request.data, list) else [request.data]
            
            created_items = []
            for item in items_data:
                tittle = item.get('tittle')
                price = item.get('price')
                featured = item.get('featured')
                category_id = item.get('category')
                
                category = get_object_or_404(Category, pk=category_id)
                
                menu_item = MenuItem.objects.create(
                    tittle = tittle,
                    price = price,
                    featured = featured,
                    category = category
                )
                created_items.append({
                    'id':menu_item.id,
                    'tittle':menu_item.tittle,
                    'price':str(menu_item.price),
                    'featured':menu_item.featured,
                    'category': menu_item.category.id
            })
            
            return Response(created_items, status=status.HTTP_201_CREATED)
            
#Menu Items - Singular element

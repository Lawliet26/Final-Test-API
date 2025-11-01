from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import MenuItem, Category, Cart, Order, OrderItem
from datetime import date

# Create your views here.


# Managers
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def managers(request):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        managers = User.objects.filter(groups__name="Manager")
        managers_data = [
            {"id": m.id, "username": m.username, "email": m.email} for m in managers
        ]
        return Response(managers_data, status=status.HTTP_200_OK)

    if request.method == "POST":
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        manager_group = Group.objects.get(name="Manager")
        user.groups.add(manager_group)

        return Response(
            {"message": "User Added to Manager group"}, status=status.HTTP_201_CREATED
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def manager_delete(request, userId):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=userId)
    manager_group = Group.objects.get(name="Manager")
    user.groups.remove(manager_group)

    return Response(
        {"message": "User removed from Managers Group"}, status=status.HTTP_200_OK
    )


# Delivery Crew
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        crew = User.objects.filter(groups__name="Delivery crew")
        crew_data = [
            {"id": c.id, "username": c.username, "email": c.email} for c in crew
        ]
        return Response(crew_data, status=status.HTTP_200_OK)

    if request.method == "POST":
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        crew_group = Group.objects.get(name="Delivery crew")
        user.groups.add(crew_group)

        return Response(
            {"message": "User Added to Delivery crew group"},
            status=status.HTTP_201_CREATED,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delivery_crew_delete(request, userId):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=userId)
    crew_group = Group.objects.get(name="Delivery crew")
    user.groups.remove(crew_group)

    return Response(
        {"message": "User removed from Delivery crew Group"}, status=status.HTTP_200_OK
    )


# Menu items views - General
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method == "GET":
        menu_items = MenuItem.objects.all()
        menu_items_data = [
            {
                "id": item.id,
                "tittle": item.tittle,
                "price": str(item.price),
                "featured": item.featured,
                "category": item.category.id,
            }
            for item in menu_items
        ]
        return Response(menu_items_data, status=status.HTTP_200_OK)

    if request.method == "POST":
        if not request.user.groups.filter(name="Manager").exists():
            return Response(
                {"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN
            )

        items_data = request.data if isinstance(request.data, list) else [request.data]

        created_items = []
        for item in items_data:
            tittle = item.get("tittle")
            price = item.get("price")
            featured = item.get("featured")
            category_id = item.get("category")

            category = get_object_or_404(Category, pk=category_id)

            menu_item = MenuItem.objects.create(
                tittle=tittle, price=price, featured=featured, category=category
            )
            created_items.append(
                {
                    "id": menu_item.id,
                    "tittle": menu_item.tittle,
                    "price": str(menu_item.price),
                    "featured": menu_item.featured,
                    "category": menu_item.category.id,
                }
            )

        return Response(created_items, status=status.HTTP_201_CREATED)


# Menu Items - Singular element
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def single_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == "GET":

        item_data = {
            "id": item.id,
            "tittle": item.tittle,
            "price": str(item.price),
            "featured": item.featured,
            "category": item.category.id,
        }
        return Response(item_data, status=status.HTTP_200_OK)

    if request.method in ["PUT", "PATCH", "DELETE"]:
        if not request.user.groups.filter(name="Manager").exists():
            return Response(
                {"message": "Unautorized"}, status=status.HTTP_403_FORBIDDEN
            )

        if request.method == "PUT":
            item.tittle = request.data.get("tittle")
            item.price = request.data.get("price")
            item.featured = request.data.get("featured")
            category_id = request.data.get("category")
            item.category = get_object_or_404(Category, pk=category_id)
            item.save()

            return Response({"message": "Item Updated"}, status=status.HTTP_200_OK)

        elif request.method == "PATCH":
            if "tittle" in request.data:
                item.tittle = request.data.get("tittle")
            if "price" in request.data:
                item.price = request.data.get("price")
            if "featured" in request.data:
                item.featured = request.data.get("featured")
            if "category" in request.data:
                category_id = request.data.get("category")
                item.category = get_object_or_404(Category, pk=category_id)
            item.save()

            return Response(
                {"message": "Item partially updated"}, status=status.HTTP_200_OK
            )

        elif request.method == "DELETE":
            item.delete()

            return Response({"message": "Item Deleted"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_items(request):

    if request.method == "POST":
        # Get data info
        menuitem_id = request.data.get("menuitem")
        quantity = request.data.get("quantity")

        # Validate request data
        if not menuitem_id or not quantity:
            return Response(
                {"message": "menuitem and quantity are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return Response(
                {"message": "Quantity must be gretaer than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the menuitem
        menuitem = get_object_or_404(MenuItem, pk=menuitem_id)

        # Calculate de price
        unit_price = menuitem.price
        total_price = unit_price * quantity

        # Verify if the menu item already exists
        existing_cart = Cart.objects.filter(
            user=request.user, menuitem=menuitem
        ).first()

        if existing_cart:
            existing_cart.quantity = quantity
            existing_cart.price = unit_price * quantity
            existing_cart.save()

            cart_data = {
                "id": existing_cart.id,
                "menuitem": existing_cart.menuitem.id,
                "menuitem_tittle": existing_cart.menuitem.tittle,
                "quantity": existing_cart.quantity,
                "unit_price": str(existing_cart.unit_price),
                "price": str(existing_cart.price),
            }

            return Response(cart_data, status=status.HTTP_200_OK)

        else:
            cart_item = Cart.objects.create(
                user=request.user,
                menuitem=menuitem,
                quantity=quantity,
                unit_price=unit_price,
                price=total_price,
            )

            cart_data = {
                "id": cart_item.id,
                "menuitem": cart_item.menuitem.id,
                "menuitem_tittle": cart_item.menuitem.tittle,
                "quantity": cart_item.quantity,
                "unit_price": str(cart_item.unit_price),
                "total_price": str(cart_item.price),
            }

            return Response(cart_data, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        cart_items = Cart.objects.filter(user=request.user)

        cart_data = [
            {
                "id": item.id,
                "menuitem": item.menuitem.id,
                "menuitem_tittle": item.menuitem.tittle,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "price": str(item.price),
            }
            for item in cart_items
        ]
        return Response(cart_data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orders(request):

    if request.method == "POST":
        if request.user.groups.filter(name__in=["Manager", "Delivery crew"]).exists():
            return Response(
                {"message": "Only customer can create orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Extract items
        cart_items = Cart.objects.filter(user=request.user)

        # Verify cart
        if not cart_items.exists():
            return Response(
                {"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        #  Calculate Total
        total = sum(item.price for item in cart_items)

        #  Order create
        order = Order.objects.create(
            user=request.user,
            delivery_crew=None,
            status=0,
            total=total,
            date=date.today(),
        )
        
        # Create order_items from Cart items
        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order = order,
                menuitem = cart_item.menuitem,
                quantity = cart_item.quantity,
                unit_price = cart_item.unit_price,
                price = cart_item.price
            )
            order_items.append(order_item)
            
        #Delete Cart content after the order has been created
        Cart.objects.filter(user = request.user).delete()
        
        #Output
        order_data = {
            "id": order.id,
            "user": order.user.id,
            "delivery_crew": order.delivery_crew.id if order.delivery_crew else None,
            "status": order.status,
            "total": str(order.total),
            "date": str(order.date),
            "items": [
                {
                    "id": item.id,
                    "menuitem" : item.menuitem.id,
                    "menuitem_tittle": item.menuitem.tittle,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "price": str(item.price)
                } 
                for item in order_items
            ]
            
        }
        
        return Response(order_data, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        # If the user is a Manager, they will be able to see all orders
        if request.user.groups.filter(name = 'Manager').exists():
            orders = Order.objects.all()
            
        # If The user is not a Manager, they will only be able to see their own orders
        else:
            orders = Order.objects.filter(user = request.user)
            
        #Build the response
        orders_data = []
        for order in orders:
            #Get the OrderItems for this order
            order_items = OrderItem.objects.filter(order = order)
            
            order_data = {
                "id": order.id,
                "user": order.user.id,
                "delivery_crew": order.delivery_crew.id if order.delivery_crew else None,
                "status": order.status,
                "total": str(order.total),
                "date": str(order.date),
                "items": [
                    {
                        "id": item.id,
                        "menuitem" : item.menuitem.id,
                        "menuitem_tittle": item.menuitem.tittle,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "price": str(item.price)
                    } 
                    for item in order_items
                ]
                
            }
            
            orders_data.append(order_data)
            
        return Response(orders_data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request, pk):
    
    #Get the order
    order = get_object_or_404(Order, pk = pk)
    
    if request.method == "GET":
        
        #Check all permissions related to roles
        if request.user.groups.filter(name="Manager").exists():
            pass
        elif request.user.groups.filter(name="Delivery crew").exists():
            if order.delivery_crew != request.user:
                return Response({'message':'You can only view orders assigned to you'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if order.user != request.user:
                return Response({'message':'You can only view your own orders'}, status=status.HTTP_403_FORBIDDEN)
            
        #Get the order items
        order_items = OrderItem.objects.filter(order = order)
        
        #Output
        order_data = {
            "id": order.id,
                "user": order.user.id,
                "delivery_crew": order.delivery_crew.id if order.delivery_crew else None,
                "status": order.status,
                "total": str(order.total),
                "date": str(order.date),
                "items": [
                    {
                        "id": item.id,
                        "menuitem" : item.menuitem.id,
                        "menuitem_tittle": item.menuitem.tittle,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "price": str(item.price)
                    } 
                    for item in order_items
                ]
        }
        
        return Response(order_data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        if order.user == request.user:
            items_data = request.data if isinstance(request.data, list) else request.data.get('items', [])
            
            if not items_data:
                return Response({'message':'Items list is required'}, status=status.HTTP_400_BAD_REQUEST)
        
            valid_items = []
            invalid_items = []
            
            #Extract the items fron the list
            for item_data in items_data:
                menuitem_id = item_data.get("menuitem")
                quantity = item_data.get("quantity")
            
                # Check the sended info
                if not menuitem_id:
                    invalid_items.append(f"Item without menuitem ID {item_data}")
                    continue
                if not quantity or quantity<=0:
                    invalid_items.append(f"Item {menuitem_id} without quantity assigned")
                    continue
                
                #Check the menuitems existance
                try:
                    menuitem = MenuItem.objects.get(pk=menuitem_id)
                    valid_items.append({
                        'menuitem': menuitem,
                        'quantity': quantity
                    })
                except MenuItem.DoesNotExist:
                    invalid_items.append(f"Menuitem {menuitem_id} doesn't exist")
                    
            if not valid_items:
                return Response({'Message':'There are not valid items in the request to add'})
            
            #Delete all objects
            OrderItem.objects.filter(order=order).delete()
            
            #Create the new order with the valid items
            new_total=0
            for item_info in valid_items:
                menuitem = item_info['menuitem']
                quantity = item_info['quantity']
                unit_price = menuitem.price
                price = unit_price * quantity
                
                OrderItem.objects.create(
                    order=order,
                    menuitem=menuitem,
                    quantity=quantity,
                    unit_price=unit_price,
                    price=price
                )
                
                new_total += price
            
            #Total order update
            order.total = new_total
            order.save()
            
            #Response with valid and invalid items
            response_data= {
                'message': 'Order update successfully',
                'items_added': len(valid_items),
                'total_updated': str(order.total) 
            }
            
            if invalid_items:
                response_data['message'] = 'Order updated but some items were not added'
                response_data['invalid_items'] = invalid_items
                
            return Response(response_data, status=status.HTTP_200_OK)
            
        elif request.user.groups.filter(name='Manager').exists():
            return Response({'message':'Managers should use PATCH to update orders'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message':'You can only modify your own orders'}, status=status.HTTP_403_FORBIDDEN)
        
    
    if request.method == 'PATCH':
        #The manager can update the delivery crew and status
        if request.user.groups.filter(name="Manager").exists():
            allowed_fields = {'delivery_crew','status'}
            sent_fields = set(request.data.keys())
            
            if not sent_fields.issubset(allowed_fields):
                invalid_fields = sent_fields - allowed_fields
                return Response({
                    'message': f'Managers cand only update status and delivery crew: {list(invalid_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'delivery_crew' in request.data:
                delivery_crew_id = request.data.get('delivery_crew')
                
                #Check de delivery crew permissions
                if delivery_crew_id:
                    delivery_user = get_object_or_404(User, pk=delivery_crew_id)
                    
                    if not delivery_user.groups.filter(name='Delivery crew').exists():
                        return Response({'message':'User must be part of Delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
                    order.delivery_crew = delivery_user
                    
                else:
                    order.delivery_crew = None
            
            if 'status' in request.data:
                order.status = request.data.get('status')
            
            #Update the order    
            order.save()
            return Response({"message":"Order updated successfully"}, status=status.HTTP_200_OK)
        
        #Delyvery crew can only update the order status
        elif request.user.groups.filter(name="Delivery crew").exists():
            #Check if the delivery crew user is the owner
            if order.delivery_crew != request.user:
                return Response({'message':'You can only update orders assigned to you'}, status=status.HTTP_403_FORBIDDEN)
            
            #Update the ststus
            if 'status' in request.data:
                order.status = request.data.get('status')
                order.save()
                return Response({'message': 'Order status has been updated successfully'}, status=status.HTTP_200_OK)
            
            #Delivery crew cant update other parameters
            else:
                return Response({'message':'You can only update the status'}, status=status.HTTP_403_FORBIDDEN)
            
            
        elif not request.user.groups.filter(name__in=['Manager','Delivery crew']).exists() and order.user == request.user:
            # Cutomer can update menuitems and the quanity
            menuitem_id = request.data.get('menuitem')
            quantity = request.data.get('quantity')
            
            if not menuitem_id:
                return Response({'message':'menuitem ID is requiered'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not quantity:
                return Response({'message':'quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            #Check if the menuitem exists
            menuitem = get_object_or_404(MenuItem, pk=menuitem_id)
            
            #Check if the menuitem is in the order
            existing_order_item = OrderItem.objects.filter(order=order, menuitem=menuitem).first()
            
            if quantity == 0:
                #Delete the item when quantity is 0
                if existing_order_item:
                    existing_order_item.delete()
                    message = f'Item {menuitem.tittle} removed from order'
                else:
                    return Response({'message':'Is not possible to add a menuitem whose quantity is less than 0'}, status=status.HTTP_400_BAD_REQUEST)
                    
            elif quantity > 0:
                unit_price = menuitem.price
                price = unit_price * quantity
                
                if existing_order_item:
                    existing_order_item.quantity = quantity
                    existing_order_item.unit_price = unit_price
                    existing_order_item.price = price
                    existing_order_item.save()
                    message= f"Item {menuitem.tittle} has been updated successfully"
                    
                else:
                    #Create a new item in the order
                    OrderItem.objects.create(
                        order=order,
                        menuitem = menuitem,
                        quantity = quantity,
                        unit_price = unit_price,
                        price = price
                    )
                    message = f'Item {menuitem.tittle} added to order'
                    
            else:
                return Response({'message':'Is not possible to add a menuiten whose quantity less than 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            #Calculate de total again
            order_items = OrderItem.objects.filter(order=order)
            new_total = sum(item.price for item in order_items)
            order.total = new_total
            order.save()
            
            return Response({
                'message':message,
                'total_updated': str(order.total)
            },status=status.HTTP_200_OK)
            
        else:
            return Response({'message':'You can only modify your own orders'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response({'message':'The order has been deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Only Managers can delete orders'})
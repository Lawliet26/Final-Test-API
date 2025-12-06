from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *
from datetime import date


# ModelSerializer: Aplica validaciones automaticas por lo que busca coincidencia del usuario y si lo encuentra tira error ya que ele usuario ya existe, se usa con las subclase Meta:

#Serializer: Aplica solo validaciones personalizadas

class ManagerGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 100)
    email = serializers.EmailField(read_only = True)
        
    #Se sobrescribe el metodo Create de la vista desde el serializador
    def create(self, validated_data):
        username = validated_data.get('username')
        
        # Forma de filtrar objeto segun una propiedad en esta ocacion la propiedad es username
        try: 
            #Traer los objetos cuyo username sea... la variables username anterior
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise serializers.ValidationError('This username not exists')
        
        # Buscar el grupo y asignarlo a una variable
        managers = Group.objects.get(name='Manager')
        
        # Agregar el usuario con ese username al grupo anterior
        #Nose pone user,username porque anteriormente ya el username se habia asignado a la variable user
        user.groups.add(managers)
        
        return user
    
class DeliveryCrewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(read_only= True)
    
    def create(self, validated_data):
        username = validated_data.get('username')
        
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise serializers.ValidationError("The user not exist")
        
        delivery_crew = Group.objects.get(name='Delivery crew')
        
        user.groups.add(delivery_crew)
        
        return user
    
class MenuItemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()
    )
    
    quantity = serializers.IntegerField(min_value=1)
    
    unit_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only = True
    )
    
    price = serializers.DecimalField(
        decimal_places=2,
        max_digits=6,
        read_only=True
    )
    
    class Meta:
        model = Cart
        fields = ['id','menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'user', 'unit_price', 'price']
        
    def create(self, validated_data):
        menuitem = validated_data.get('menuitem')
        quantity = validated_data.get('quantity')
        
        unit_price = menuitem.price
        price = unit_price * quantity
        
        cart, created = Cart.objects.update_or_create(
            user = self.context['request'].user,
            menuitem=menuitem,
            defaults={
                'quantity': quantity,
                'unit_price':unit_price,
                'price': price
            }
        )
        
        return cart
    
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(read_only=True)
    menuitem_tittle = serializers.CharField(source='menuitem.tittle', read_only=True)
    
    class Meta:
        model= OrderItem
        fields = ["id", 'quantity', 'unit_price', 'price','menuitem', 'menuitem_tittle']
        read_only_fields = ['id','price', 'unit_price','menuitem']
        
    
class OrderSerializer(serializers.ModelSerializer):
    
    delivery_crew = serializers.PrimaryKeyRelatedField(
        required = False,
        allow_null=True,
        read_only=True
    )
    
    items = OrderItemSerializer(source = 'orderitem_set', many=True, read_only = True)
    
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew', 'status', 'date', 'total','items']
        read_only_fields = ['id','deliverry_crew', 'date', 'status', 'total', 'user']
        
    # Sobreescritura del metodo create 
    def create(self, validated_data):
        user = self.context['request'].user
        
        if user.groups.filter(name__in=['Manager','Delivery crew']).exists():
            raise serializers.ValidationError('Only Customers can create orders') 
        
        cart = Cart.objects.filter(user=user)
        
        if not cart.exists():
            raise serializers.ValidationError('The cart is empty')
        
        total = sum(item.price for item in cart)
        
        order = Order.objects.create(
            user=user,
            delivery_crew = None,
            status = 0,
            total = total,
            date = date.today()
        )
        
        for item in cart:
            OrderItem.objects.create(
                order = order,
                menuitem = item.menuitem,
                quantity = item.quantity,
                unit_price = item.unit_price,
                price = item.price
            )
            
        Cart.objects.filter(user=user).delete()
        
        return order
    
class ManagerUpdateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew', 'status', 'date', 'total']
        read_only_fields = ['id','user','date', 'total']
    
    def validate_delivery_crew(self, value):
        
        if value is None:
            return value
        
        if not value.groups.filter(name="Delivery crew").exists():
            raise serializers.ValidationError('User does not belong to the Delivery group')
        
        return value
    
        
    
class DeliveryUpdateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Order
        fields = ['id','user','delivery_crew', 'status', 'date', 'total']
        read_only_fields = ['id','user','date', 'total','delivery_crew']
            
        

    

    
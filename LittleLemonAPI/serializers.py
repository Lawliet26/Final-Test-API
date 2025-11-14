from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *


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
        
    
    
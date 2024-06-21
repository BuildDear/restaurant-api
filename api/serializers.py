from rest_framework import serializers
from api.models import Restaurant, Menu, Dish
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from api.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'build_version', 'role')

    def create(self, validated_data):
        print("Creating user with custom serializer")
        return super().create(validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'build_version', 'role')


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'contact_info']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'restaurant']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    dish_ids = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(), source='dishes', write_only=True, many=True
    )

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'dishes', 'dish_ids']

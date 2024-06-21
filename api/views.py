from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Restaurant, Menu, Dish, Vote
from api.serializers import RestaurantSerializer, MenuSerializer, DishSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False, methods=['get'], url_path='current-day')
    def get_current_day_menu(self, request):
        today = timezone.now().date()
        menus = Menu.objects.filter(date=today)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='current-day-results')
    def get_current_day_results(self, request):
        today = timezone.now().date()
        menus = Menu.objects.filter(date=today)
        results = []

        for menu in menus:
            vote_count = Vote.objects.filter(menu=menu).count()
            results.append({
                'menu_id': menu.id,
                'restaurant': menu.restaurant.name,
                'date': menu.date,
                'vote_count': vote_count
            })

        return Response(results)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

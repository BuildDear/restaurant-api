from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RestaurantViewSet, MenuViewSet, DishViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Restaurant, Menu, Dish, Vote, User
from datetime import date

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return User.objects.create_user(email='test@example.com', password='testpassword', role='restaurant_admin')

@pytest.fixture
def create_restaurant(create_user):
    return Restaurant.objects.create(name='Test Restaurant', address='123 Test St', contact_info='test@example.com')

@pytest.fixture
def create_dish(create_restaurant):
    return Dish.objects.create(name='Test Dish', description='Test Description', price=10.00, restaurant=create_restaurant)

@pytest.fixture
def create_menu(create_restaurant, create_dish):
    menu = Menu.objects.create(date=date.today(), restaurant=create_restaurant)
    menu.dishes.add(create_dish)
    return menu

@pytest.fixture
def create_vote(create_menu, create_user):
    return Vote.objects.create(menu=create_menu, user=create_user)

# Test for RestaurantViewSet
@pytest.mark.django_db
def test_create_restaurant(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    url = reverse('restaurant-list')
    data = {'name': 'New Restaurant', 'address': '456 New St', 'contact_info': 'new@example.com'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'New Restaurant'

@pytest.mark.django_db
def test_list_restaurants(api_client, create_user, create_restaurant):
    api_client.force_authenticate(user=create_user)
    url = reverse('restaurant-list')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Restaurant'

# Test for MenuViewSet
@pytest.mark.django_db
def test_create_menu(api_client, create_user, create_restaurant, create_dish):
    api_client.force_authenticate(user=create_user)
    url = reverse('menu-list')
    data = {
        'restaurant': create_restaurant.id,
        'date': date.today(),
        'dish_ids': [create_dish.id]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['restaurant'] == create_restaurant.id

@pytest.mark.django_db
def test_list_menus(api_client, create_user, create_menu):
    api_client.force_authenticate(user=create_user)
    url = reverse('menu-list')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['restaurant'] == create_menu.restaurant.id

# Test for DishViewSet
@pytest.mark.django_db
def test_create_dish(api_client, create_user, create_restaurant):
    api_client.force_authenticate(user=create_user)
    url = reverse('dish-list')
    data = {
        'name': 'New Dish',
        'description': 'New Description',
        'price': 20.00,
        'restaurant': create_restaurant.id
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'New Dish'

@pytest.mark.django_db
def test_list_dishes(api_client, create_user, create_dish):
    api_client.force_authenticate(user=create_user)
    url = reverse('dish-list')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Dish'

# Test for current-day menu
@pytest.mark.django_db
def test_get_current_day_menu(api_client, create_user, create_menu):
    api_client.force_authenticate(user=create_user)
    url = reverse('menu-get-current-day-menu')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['date'] == str(date.today())

# Test for current-day results
@pytest.mark.django_db
def test_get_current_day_results(api_client, create_user, create_vote):
    api_client.force_authenticate(user=create_user)
    url = reverse('menu-get-current-day-results')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['vote_count'] == 1

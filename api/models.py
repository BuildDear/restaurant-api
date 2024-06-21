from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    build_version = models.CharField(max_length=10)
    role = models.CharField(max_length=20, choices=[('employee', 'Employee'), ('restaurant_admin', 'Restaurant Admin')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_info = models.TextField()


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')


class Menu(models.Model):
    date = models.DateField()
    dishes = models.ManyToManyField(Dish)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='votes')
    vote_date = models.DateTimeField(auto_now_add=True)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

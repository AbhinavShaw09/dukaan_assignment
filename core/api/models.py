from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, mobile_number, password=None):
        if not mobile_number:
            raise ValueError("Users must have a mobile number")

        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    mobile_number = models.CharField(max_length=15, unique=True)
    USERNAME_FIELD = "mobile_number"
    objects = AccountManager()


class Store(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    link = models.CharField(max_length=100, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    MRP = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Customer(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    session_id = models.CharField(
        max_length=255, unique=True
    )  


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

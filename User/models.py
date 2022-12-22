from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# Customer Models are:
#
# class Customer(AbstractUser):
# class Customer_orders(models.Model):

# Here we are using User class to have only one AbstractUser class
# which includes the four user types 

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        CUSTOMER = "CUSTOMER", 'Customer'
        STORE = "STORE", 'Store'
        WORKSHOP = "WORKSHOP", 'Workshop'

    base_role = Role.ADMIN

    role = models.CharField(max_length= 50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


##-- Customer User Type --##

# This class defines the Customer for query statements

class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)

class Customer(User):
    
    base_role = User.Role.CUSTOMER

    customer = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only For Customers"

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user=instance)


# Here the Customer profile is created and invoked
# from the User(AbstractUser) for Authentication

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    C_id = models.IntegerField(primary_key=True)
    C_name = models.CharField(max_length=50, null=True)
    C_email = models.EmailField(max_length=50, null=True)
    C_pass = models.CharField(max_length=30, null=True)
    C_phone = models.CharField(max_length=12)
    C_city = models.CharField(max_length=50, null=True)


##-- Store User Type --##

# This class defines the Store for query statements

class StoreManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STORE)

class Store(User):
    
    base_role = User.Role.STORE

    store = StoreManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only For Stores"

@receiver(post_save, sender=Store)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STORE":
        StoreProfile.objects.create(user=instance)

# Here the Store profile is created and invoked
# from the User(AbstractUser) for Authentication

class StoreProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    S_id = models.IntegerField(primary_key=True)
    S_name = models.CharField(max_length=50, null=True)
    S_email = models.EmailField(max_length=50, null=True)
    S_pass = models.CharField(max_length=30, null=True)
    S_city = models.CharField(max_length=50, null=True)


##-- Workshop User Type --##

# This class defines the Workshop for query statements

class WorkshopManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.WORKSHOP)

class Workshop(User):
    
    base_role = User.Role.WORKSHOP

    workshop = WorkshopManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only For Workshops"

@receiver(post_save, sender=Workshop)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "WORKSHOP":
        WorkshopProfile.objects.create(user=instance)

# Here the Workshop profile is created and invoked
# from the User(AbstractUser) for Authentication

class WorkshopProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    W_id = models.IntegerField(primary_key=True)
    W_name = models.CharField(max_length=50, null=True)
    W_email = models.EmailField(max_length=50, null=True)
    W_pass = models.CharField(max_length=30, null=True)
    W_city = models.CharField(max_length=50, null=True)




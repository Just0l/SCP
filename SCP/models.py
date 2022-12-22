from django.db import models
from User.models import CustomerProfile, StoreProfile, WorkshopProfile
from time import gmtime, strftime


# Create your models here.


# Store Models are:
#
# class StoreProfile(models.Model):
# class Parts(models.Model):
# class Part_Image(models.Model):
# class Store_parts(models.Model):
# class Ordered_parts(models.Model):
# class Store_Image(models.Model):


class Parts(models.Model):
    part_no = models.IntegerField(primary_key=True)
    P_name = models.CharField(max_length=100)

   
class Part_Image(models.Model):
    P_id = models.ForeignKey(Parts, on_delete=models.CASCADE)
    image_field = models.ImageField(
        upload_to= 'static/images/profile/{0}'.format(strftime('%Y%m%d-%H%M%S',gmtime())) ,
        default='no-image.jpg' ,
        width_field='imagewidth' ,
        height_field='imageheight' ,
        )
    imagewidth = models.PositiveIntegerField(editable = False, default = 65)
    imageheight = models.PositiveIntegerField(editable = False, default = 65)


class Store_parts(models.Model):
    sp_id = models.IntegerField(primary_key=True)
    S_id = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    part_no = models.ForeignKey(Parts, on_delete=models.CASCADE)
    P_name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    car_make = models.CharField(max_length=50)


class Ordered_parts(models.Model):
    op_id = models.IntegerField(primary_key=True)
    sp_id = models.ForeignKey(Store_parts, on_delete=models.CASCADE)


class Store_Image(models.Model):
    S_id = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    image_field = models.ImageField(
        upload_to= 'static/images/profile/{0}'.format(strftime('%Y%m%d-%H%M%S',gmtime())) ,
        default='no-image.jpg' ,
        width_field='imagewidth' ,
        height_field='imageheight' ,
        )
    imagewidth = models.PositiveIntegerField(editable = False, default = 50)
    imageheight = models.PositiveIntegerField(editable = False, default = 50)


# Customer Models are:
#
# class CustomerProfile(models.Model):
# class Customer_orders(models.Model):


class Customer_orders(models.Model):
    co_id = models.IntegerField(primary_key=True)
    S_id = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    C_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    op_id = models.ForeignKey(Ordered_parts, on_delete=models.CASCADE)


# Workshop Models are:
#
# class WorkshopProfile(models.Model):
# class Workshop_orders(models.Model):
# class Workshop_Image(models.Model):
# class Services(models.Model):
# class Appointment(models.Model):
# class Offers(models.Model):


class Workshop_orders(models.Model):
    wo_id = models.IntegerField(primary_key=True)
    W_id = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    op_id = models.ForeignKey(Ordered_parts, on_delete=models.CASCADE)


class Workshop_Image(models.Model):
    W_id = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    image_field = models.ImageField(
        upload_to= 'static/images/profile/{0}'.format(strftime('%Y%m%d-%H%M%S',gmtime())) ,
        default='no-image.jpg' ,
        width_field='imagewidth' ,
        height_field='imageheight' ,
        )
    imagewidth = models.PositiveIntegerField(editable = False, default = 50)
    imageheight = models.PositiveIntegerField(editable = False, default = 50)


class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    W_id = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=75)


class Appointment(models.Model):
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    W_id = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    C_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()


class Offers(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    W_id = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    offer_desc = models.CharField(max_length=200)
    offer_price = models.IntegerField()
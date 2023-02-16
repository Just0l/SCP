from operator import index
from django.db import models
from User.models import Customer, Store, Workshop
from time import gmtime, strftime


class Categories(models.Model):
    category_name = models.CharField(max_length=100)


class Parts(models.Model):
    part_no = models.CharField(primary_key=True, max_length=20)
    P_name = models.CharField(max_length=100)
    car_manu = models.CharField(max_length=150)
    car_name = models.CharField(max_length=150)
    manufacture_year = models.CharField(max_length=10)
    original = models.BooleanField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    desc = models.TextField()


class Part_Image(models.Model):
    P_id = models.ForeignKey(Parts, on_delete=models.CASCADE)
    image_field = models.ImageField(
        upload_to="media/part_images/",
        default="no-image.jpg",
        width_field="imagewidth",
        height_field="imageheight",
    )
    imagewidth = models.PositiveIntegerField(editable=False, default=65)
    imageheight = models.PositiveIntegerField(editable=False, default=65)


class Store_parts(models.Model):
    S_id = models.ForeignKey(Store, on_delete=models.CASCADE,  related_name='StoreParts')
    Price = models.FloatField()
    p_id =  models.ForeignKey(Parts, on_delete=models.CASCADE, related_name='parts')
    quantity = models.IntegerField()


class Cart(models.Model):
    C_id = models.ForeignKey(Customer, on_delete=models.CASCADE,  related_name='CustomerCart')
    p_id =  models.ForeignKey(Store_parts, on_delete=models.CASCADE, related_name='Cart')
    Q = models.IntegerField(default=1)


class Ordered_parts(models.Model):
    op_id = models.IntegerField(primary_key=True)
    sp_id = models.ForeignKey(
        Store_parts, on_delete=models.CASCADE, related_name="StoreParts"
    )


class Store_Image(models.Model):
    S_id = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="StoreInformation"
    )
    image_field = models.ImageField(
        upload_to="images/part/{0}".format(strftime("%Y%m%d-%H%M%S", gmtime())),
        default="no-image.jpg",
        width_field="imagewidth",
        height_field="imageheight",
    )
    imagewidth = models.PositiveIntegerField(editable=False, default=50)
    imageheight = models.PositiveIntegerField(editable=False, default=50)




class Customer_orders(models.Model):
    S_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="StoreOders")
    C_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="CustomerOders"
    )
    op_id = models.ForeignKey(Ordered_parts, on_delete=models.CASCADE)
    Date = models.DateField()
    quantity = models.IntegerField()




class Workshop_orders(models.Model):
    wo_id = models.IntegerField(primary_key=True)
    W_id = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="Workshoporders"
    )
    op_id = models.ForeignKey(Ordered_parts, on_delete=models.CASCADE)


class Workshop_Image(models.Model):
    W_id = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="WorkshopImg"
    )
    image_field = models.ImageField(
        upload_to="static/images/profile/{0}".format(
            strftime("%Y%m%d-%H%M%S", gmtime())
        ),
        default="no-image.jpg",
        width_field="imagewidth",
        height_field="imageheight",
    )
    imagewidth = models.PositiveIntegerField(editable=False, default=50)
    imageheight = models.PositiveIntegerField(editable=False, default=50)



class Services(models.Model):
    W_id = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="WorkshopServices"
    )
    name = models.CharField(max_length=75)
    price = models.IntegerField()
    DESCRIPTION = models.TextField()
    image_field = models.ImageField(
        upload_to="static/images/Services/{0}".format(
            strftime("%Y%m%d-%H%M%S", gmtime())
        ),
        default="no-image.jpg",
        width_field="imagewidth",
        height_field="imageheight",
    )
    imagewidth = models.PositiveIntegerField(editable=False, default=50)
    imageheight = models.PositiveIntegerField(editable=False, default=50)


class Appointment(models.Model):
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    W_id = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="WorkshopAppointment"
    )
    C_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="CustomerAppointment"
    )
    Date = models.DateField()
    Time = models.TimeField()


class Offers(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    W_id = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="WorkshopOffers"
    )
    offer_desc = models.CharField(max_length=200)
    offer_price = models.IntegerField()








class DabrhaRequest(models.Model):
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    part_no = models.CharField(max_length=20, null=True)
    P_name = models.CharField(max_length=100)
    car_manu = models.CharField(max_length=150)
    car_name = models.CharField(max_length=150)
    manufacture_year = models.CharField(max_length=10)
    original = models.BooleanField()
    desc = models.TextField()
    img = models.ImageField(
        upload_to="media/part_images/",
        default="no-image.jpg",
    )



class DabrhaOrders(models.Model):
    Request = models.ForeignKey(DabrhaRequest, related_name='store', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='store', on_delete=models.CASCADE)
    Date = models.DateField()
    price = models.FloatField()



class dabrha_offers(models.Model):
    offer_price = models.FloatField()
    store = models.ForeignKey(Store, related_name='store_made_offer', on_delete=models.CASCADE)
    dabrha_request = models.ForeignKey(DabrhaRequest, related_name='d_request', on_delete=models.CASCADE)
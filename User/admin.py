from django.contrib import admin
from .models import Customer, Workshop, Store, Admin
# Register your models here.
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(Workshop)
admin.site.register(Admin)

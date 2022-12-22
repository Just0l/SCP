from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import UserAccount
# # Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = UserAccount
#     list_display = ['U_email', 'U_name', 'U_id',] # new
#     fieldsets = UserAdmin.fieldsets + ( # new
#     (None, {'fields': ('U_id',)}),
# )

# add_fieldsets = UserAdmin.add_fieldsets + ( # new
# (None, {'fields': ('U_id',)}),
# )

# admin.site.register(UserAccount, CustomUserAdmin)
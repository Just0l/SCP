from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'scp'

urlpatterns = [
    path('register/', views.register, name='registerUser'),
    path('login/', auth_views.LoginView.as_view(template_name='SCP/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='logout'),
    path('', views.home_page, name='home-page'),
    path('account/', views.customer_account, name='account'),
    path('products/<int:category_id>/', views.category_products, name='products'),
    path('store/', views.store_main_page, name='store-home'),
    path('workshop/', views.workshop_main_page, name='workshop-home'),
    path('store/register', views.register_store, name='registerStore'),
    path('ws/register', views.register_workshop, name='registerWs'),
    path('store/login', auth_views.LoginView.as_view(template_name='SCP/login.html'), name='store-login'),
    path('store/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='store-logout'),
    path('ws/login', auth_views.LoginView.as_view(template_name='SCP/login.html'), name='ws-login'),
    path('ws/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='ws-logout'),
    path('store/add-parts/', views.add_parts, name='add-parts'),
    path('store/store-parts', views.store_parts, name='store-parts'),
    path('store/customers-orders', views.customers_orders, name='customers-orders'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'scp'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('register/', views.register, name='registerUser'),
    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='logout'),
    path('account/', views.customer_account, name='account'),
    path('products/<int:category_id>/', views.all_products, name='products'),
    path('store/', views.store_main_page, name='store-home'),
    path('Workshop/', views.workshop_main_page, name='workshop-home'),
    path('store/register', views.register_store, name='registerStore'),
    path('ws/register', views.register_workshop, name='registerWs'),
    path('store/login', auth_views.LoginView.as_view(template_name='SCP/login.html'), name='store-login'),
    path('store/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='store-logout'),
    path('ws/login', views.WsLogin.as_view(), name='ws-login'),
    path('ws/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='ws-logout'),
    path('store/add-parts/', views.add_parts, name='add-parts'),
    path('store/store-parts', views.store_parts, name='store-parts'),
    path('store/customers-orders', views.customers_orders, name='customers-orders'),
    path('Workshop/Addservice/', views.Addservice, name='add-service'),
    path('Workshop/ShowServices/', views.ShowServices, name='show-services'),
    path('Workshop/Delete/', views.Delete, name='delete-service'),
    path('Workshop/Update/', views.Update, name='update-service'),
    path('Workshop/Appointment/', views.ShowAppointment, name='make-app'),
    path('product-details/<int:SP>/<str:partNo>/', views.Product_Details, name='product-details'),
    path('Cart/', views.CartPage, name='CartPage'),
    path('Delete/', views.DeleteCart, name='DeleteCart'),
    path('WSLogin/', views.LoginWSo, name='LoginWSo'),
    path('Cart/<int:CartID>/', views.CartUpdate, name='CartUpdate'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
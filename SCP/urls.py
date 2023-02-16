from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'scp'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('register/', views.register, name='registerUser'),
    path('login/', views.CustomerLogin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='logout'),
    path('account/', views.customer_account, name='account'),
    path('products/<int:category_id>/', views.all_products, name='products'),
    path('store/', views.store_main_page, name='store-home'),
    path('Workshop/', views.workshop_main_page, name='workshop-home'),
    path('store/register', views.register_store, name='registerStore'),
    path('ws/register', views.register_workshop, name='registerWs'),
   
    path('store/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='store-logout'),

    path('ws/logout', auth_views.LogoutView.as_view(template_name='SCP/logout.html'), name='ws-logout'),
    path('store/add-parts/', views.add_parts, name='add-parts'),
    path('store/store-parts', views.store_parts, name='store-parts'),
    path('store/customers-orders', views.customers_orders, name='customers-orders'),
    path('Workshop/Addservice/', views.Addservice, name='add-service'),
    path('Workshop/ShowServices/', views.ShowServices, name='show-services'),
    path('Workshop/Delete/', views.Delete, name='delete-service'),
    path('Workshop/Appointment/', views.ShowAppointment, name='make-app'),
    path('product-details/<int:SP>/<str:partNo>/', views.Product_Details, name='product-details'),
    path('Cart/', views.CartPage, name='CartPage'),
    path('Delete/', views.DeleteCart, name='DeleteCart'),
    path('LLogin/', views.LoginWSo, name='LoginWSo'),
    path('LLogout/', views.LogoutPage, name='LogoutPage'),
    path('Cart/<int:CartID>/', views.CartUpdate, name='CartUpdate'),
    path('Payment/', views.Payment, name='Payment'),
    path('Pay/', views.Pay, name='Pay'),
    path('Orders/', views.ShowOrder, name='Orders'),
    path('ShowServices/', views.ShowServicesForCustomer, name='ShServices'),
    path('ShowServices/<int:SID>/', views.ShowServicesForCustomerDetails, name='Services-details'),
    path('Appointment/<int:SID>/', views.PaymentForService, name='PaymentForService'),
    path('ShowAppointmentForCustomer/', views.ShowAppointmentForCustomer, name='ShowAppointmentForCustomer'),
    path('dabrha/', views.dabrha_service, name='dabrha'),
    path('dabrha/delete/<int:request_id>', views.cancel_dabrha_request, name='delete-dabrha-request'),
    path('request/', views.dabrha_request, name='dabrhaRequest'),
    path('store/dabrha-orders', views.dabrha_orders, name='dabrha-orders'),
    path('store/dabrha-orders/<int:request_id>', views.make_offers_for_dabrha, name='dabrha-orders-with-id'),
    path('store/dabrha-Checkout/<int:request_id>/<int:Offer_id>', views.dabrha_Checkout, name='dabrha-Checkout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
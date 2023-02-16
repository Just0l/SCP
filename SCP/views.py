# ------------------------------------------------------------------------------------------------#
# ------------------------------------IMPORTS-----------------------------------------------------#
# ------------------------------------------------------------------------------------------------#
from django.forms import ImageField
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from SCP.models import *
from .forms import *
from django.contrib import messages
from User.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
import datetime





def is_customer(user):
    return user.is_authenticated and user.role == "CUSTOMER"


def is_store(user):
    return user.is_authenticated and user.role == "STORE"


def is_workshop(user):
    return user.is_authenticated and user.role == "WORKSHOP"


def CustomerLogin(request):
    form=LoginForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user is not None)
        if user is not None:
            login(request, user)
            if request.user.role=="CUSTOMER":
                return redirect("scp:home-page")
            elif request.user.role=="STORE":
                return redirect("scp:store-home")
            elif request.user.role=="WORKSHOP":
                return redirect("scp:workshop-home")
            # Redirect to a success page.
            ...
        else:
            # Return an 'invalid login' error message.
            ...
    context={"form":form}
    return render(request, "SCP/login.html",context)
    





def home_page(request):
    parts_categories = Categories.objects.all()
    context = {"categories": parts_categories}
    return render(request, "SCP/index.html", context)


def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}")
            return redirect("scp:home-page")
        else:
            messages.info(request, "try another username")
            return redirect("scp:registerUser")

    else:
        form = CustomUserCreationForm()
        context = {"form": form}

        return render(request, "SCP/registration.html", context)



def register_store(request):
    form = StoreCreationForm()
    if request.method == "POST":
        form = StoreCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}")
            return redirect("scp:home-page")

        else:
            messages.info(request, "try another username")
            return redirect("scp:registerStore")

    else:
        
        context = {"form": form}

        return render(request, "SCP/store/auth-register-basic.html", context)


def register_workshop(request):
    form = WorkshopUserCreationForm()
    if request.method == "POST":
        form = WorkshopUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("scp:login")
        else:
            messages.info(request, "try another username")
            return redirect("scp:registerWs")


    else:
        form = WorkshopUserCreationForm()
        context = {"form": form}

        return render(request, "SCP/ws/auth-register-basic.html", context)



def customer_account(request):

    return render(request, "SCP/my-account.html")


def all_products(request, category_id):

   categories = Categories.objects.all()
   Prodects=Parts.objects.all().filter(category=category_id)

   parts = []   
   for part in Prodects:
    parts.append({
        "part_obj":part,
         "part_img":Part_Image.objects.get(P_id=part),
         "SP":Store_parts.objects.all().filter(p_id=part).order_by('Price').first()
         })


   context = {
        'parts': parts,
        'categories': categories
        }

   return render(request, "SCP/products.html", context)






def store_main_page(request):
    if request.user.is_authenticated:
        if request.user.role == "STORE":

            return render(request, "SCP/store/Dashboard.html")
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response



def Product_Details(request, SP ,partNo):
    
    Image = Part_Image.objects.get(P_id=partNo)
    part_details = Parts.objects.get(part_no=partNo)
    store_parts = Store_parts.objects.get(id=SP)

    other_stores_with_the_same_products = Store_parts.objects.all().filter(p_id=partNo)
    img = [Part_Image.objects.get(P_id=part.p_id) for part in other_stores_with_the_same_products]

    context={
        "part":part_details,
        "image": Image,
        "store":store_parts,
        "others":other_stores_with_the_same_products,
        "img":img
    }
    for p in img:
        print(p.image_field)

    if request.method =="POST":
        Quantity=request.POST['Quantity']
        if request.user.is_authenticated:
            if request.user.role == "CUSTOMER":
                if Cart.objects.all().filter(C_id=request.user).exists():
                    cart=Cart.objects.get(p_id=store_parts)
                    Q=int(cart.Q)
                    print(Q)
                    Q+=int(Quantity)
                    print(Q)
                    cart.Q=Q
                    cart.save()

        else:
            Cart.objects.create(C_id=request.user,p_id=store_parts,Q=Quantity)
        response = redirect('/Cart/')
        return response
       

    return render(request, 'SCP/product-details.html', context)



def DeleteCart(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            ID=request.GET['DeleteID']
            if Cart.objects.all().filter(id=ID).exists():
                obj = Cart.objects.all().filter(id=ID)
                obj.delete()
            response = redirect('/Cart/')
            return response
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response


def CartPage(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            cart = Cart.objects.all().filter(C_id=request.user)
            form=UpdateCart()
            parts = []
            total=0
            for n in cart:
                parts.append({"part_obj":Parts.objects.get(part_no=n.p_id.p_id.part_no), "part_img":Part_Image.objects.get(P_id=Parts.objects.get(part_no=n.p_id.p_id.part_no)),"cart":n,"price":Store_parts.objects.get(id=n.p_id.id)})
                total+=Store_parts.objects.get(id=n.p_id.id).Price*n.Q
            

            context={
                "parts":parts,
                "total":total,
                "form":form
            }
            
            return render(request, 'SCP/cart.html', context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response




def CartUpdate(request,CartID):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            if request.POST:
                print(CartID)
                cart=Cart.objects.get(id=CartID)
                cart.Q=request.POST['Quantity']
                cart.save()
            response = redirect('/Cart/')
            return response
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response





@user_passes_test(is_workshop, login_url="ws/login")
def workshop_main_page(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":

    
            return render(request, "SCP/ws/Dashboard.html")
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response

# Creating new Store Account







def add_parts(request):
    if request.user.is_authenticated:
        if request.user.role == "STORE":
            image=PartsImages()
            if request.method == "POST":
                imageForm = PartsImages(request.POST, request.FILES)
                if imageForm.is_valid():
                    if not Parts.objects.all().filter(part_no=request.POST['part_no']).exists():
                        added_part = Parts.objects.create(part_no=request.POST['part_no'],
                        P_name=request.POST['P_name'],
                        car_manu=request.POST['car_manu'],
                        car_name=request.POST['car_name'],
                        manufacture_year=request.POST['P_name'],
                        original=True,
                        category=Categories.objects.get(id=request.POST['category']),
                        desc=request.POST['desc'])
                        store_part=Store_parts.objects.create(S_id=request.user,p_id=added_part,Price=request.POST['price'],quantity=1,)
                        store_part.save()

                        image = imageForm.cleaned_data.get("image_field")
                        Part_Image.objects.create(P_id=added_part, image_field=image)
                        messages.success(request, "part added to your store !")
                        return redirect("scp:add-parts")
                    else:
                        if not Store_parts.objects.all().filter(S_id=request.user,p_id=Parts.objects.get(part_no=request.POST['part_no'])).exists():
                            store_part=Store_parts.objects.create(S_id=request.user,p_id=Parts.objects.get(part_no=request.POST['part_no']),Price=request.POST['price'],quantity=request.POST['quantity'])
                            store_part.save()
                            messages.warning(request, "part is already exist and it will be in your store !")
                            return redirect("scp:add-parts")
                        else:
                            messages.error(request, "part is already exist !")
                            return redirect("scp:add-parts")




            else:
                category_types = {"categories": Categories.objects.all()}
                form = AddPartsForm()
                imageForm = PartsImages()
                context = {"imageForm": imageForm, "categories": Categories.objects.all(),"image":image}
                return render(request, "SCP/store/add-parts.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response




def store_parts(request):
    if request.user.is_authenticated:
        if request.user.role == "STORE":
            all_parts = Store_parts.objects.all().filter(S_id=request.user)
            parts_pks = all_parts.values_list("pk", flat=True)
            parts = []
            print(type(all_parts))
            # images= Part_Image.objects.filter(P_id__in=parts_pks).select_related('P_id')
            for n in all_parts:

                parts.append(
                    {"part_obj": n.p_id, "part_img": Part_Image.objects.get(P_id=n.p_id.part_no)}
                )

            print(parts)

            return render(request, "SCP/store/show-parts.html", {"parts": parts})
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response


def customers_orders(request):
    if request.user.is_authenticated:
        if request.user.role == "STORE":
            orders = Customer_orders.objects.all().filter(S_id=request.user)


            return render(request, "SCP/store/orders.html",{"orders":orders})
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response


def Payment(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            cart = Cart.objects.all().filter(C_id=request.user.id)
            total=0
            for item in cart:
                total=total+(item.Q*item.p_id.Price)
            context = {
                "Cart":cart,
                "total":total

            }
            return render(request, "SCP/checkout.html",context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response




def Pay(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            cart=Cart.objects.all().filter(C_id=request.user.id)
            for item in cart:
                temp=int(Ordered_parts.objects.all().count())
                Ordered=Ordered_parts.objects.create(op_id=temp,sp_id=item.p_id)
                Customer_orders.objects.create(S_id=item.p_id.S_id,C_id=request.user,op_id=Ordered,Date=datetime.datetime.now().date(),quantity=item.Q)
                Part=Store_parts.objects.get(id=item.p_id.id)
                Part.quantity=Part.quantity-item.Q
                Part.save()
                item.delete()
            response = redirect("/Orders/")
            return response
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response



def ShowOrder(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            orders = Customer_orders.objects.all().filter(C_id=request.user)
            show=[]
            for i in orders:
                show.append({"orders":i,"image":Part_Image.objects.get(P_id=i.op_id.sp_id.p_id)})
            context={"obj":show}
            return render(request, "SCP/Showorders.html",context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response



def ShowServicesForCustomer(request):
    
    services = Services.objects.all()
    context={"Services":services}
    return render(request, "SCP/Showservices.html", context)
        



def ShowServicesForCustomerDetails(request,SID):

    service = Services.objects.get(id=SID)
    context={"Services":service}
    return render(request, "SCP/ServicesDetails.html", context)
       



def PaymentForService(request,SID):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            service = Services.objects.get(id=SID)
            date=Dateandtime()
            if request.method =='POST':
                Appointment.objects.create(service_id=service,W_id=service.W_id,C_id=request.user,Date=request.POST['Date'],Time=request.POST['Time'])
                response = redirect("/ShowAppointmentForCustomer/")
                return response
            context={"Services":service,
            "Date":date
            }
            return render(request, "SCP/Servicecheckout.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response



def ShowAppointmentForCustomer(request):
    if request.user.is_authenticated:
        if request.user.role == "CUSTOMER":
            appointment=Appointment.objects.all().filter(C_id=request.user)
            context={"appointments":appointment}
            return render(request, "SCP/ShowAppointmentForCustomer.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response





def ShowServices(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":
            obj = Services.objects.all().filter(W_id=request.user.id)



            context = {
                "obj": obj,

            }
            return render(request, "SCP/ws/Showservices.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response










def ShowAppointment(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":
            datenow = datetime.datetime.now().date() + datetime.timedelta(days=3)
            print(datenow)
            obj = Appointment.objects.all().filter(
                W_id=request.user.id,
                Date__range=[datetime.datetime.now().date(), datenow],
            )
            CID = []
            for n in obj:
                CID.append(
                    [
                        User.objects.get(id=n.C_id.id),
                        n,
                        Services.objects.get(id=n.service_id.id),
                    ]
                )
            context = {"obj": obj, "obj1": CID}

            return render(request, "SCP/ws/Appointment.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response


def Addservice(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":
            Add_form = AddserviceForm()
            imageForm = ServiceImage()

            if request.method == "POST":
                Add_form = AddserviceForm(request.POST)
                imageForm = ServiceImage(request.POST, request.FILES)
                print(Add_form.is_valid())
                print(imageForm.is_valid())
                if Add_form.is_valid() and imageForm.is_valid():
                    image=imageForm.cleaned_data.get("image_field")
                    Services.objects.create(
                        W_id=User.objects.get(id=request.user.id, role="WORKSHOP"),
                        name=Add_form.cleaned_data["name"],
                        price=Add_form.cleaned_data["price"],
                        DESCRIPTION=Add_form.cleaned_data["des"],
                        image_field=image
                    )
                    response = redirect("/Workshop/ShowServices/")
                    return response
            context = {"form": Add_form,"image":imageForm}

            return render(request, "SCP/ws/Addservice.html", context)
        else:
            response = redirect("/home/")
            return response
    else:
        response = redirect("/home/")
        return response


def Delete(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":
            a = request.GET.get("DeleteID")
            if Services.objects.all().filter(id=a, W_id=request.user.id).exists():
                obj = Services.objects.get(id=a, W_id=request.user.id)

                obj.delete()
            response = redirect("/Workshop/")
            return response
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response




def dabrha_Checkout(request,request_id,Offer_id):
    dabrha=DabrhaRequest.objects.get(id=request_id)
    offer=dabrha_offers.objects.get(id=Offer_id)
    if request.method == "POST":
        DabrhaOrders.objects.create(
            customer=dabrha.customer,
            Request=dabrha,
            store=offer.store,
            Date=datetime.datetime.now().date(),
            price=offer.offer_price
        )
        
        response = redirect("/home/")
        return response

    context = {
        "dabrha": dabrha,"offer":offer

    }
    return render(request, "SCP/dabrhacheckout.html", context)






def dabrha_service(request):
    if request.method == "GET":
        customer = request.user
        if customer.customers is not None:
            all_requests = DabrhaRequest.objects.filter(customer=customer)
            dabrha_requests=[]
            for requests in all_requests:
                offer=dabrha_offers.objects.all().filter(dabrha_request=requests).order_by("offer_price").first()
                dabrha_requests.append({"request":requests,"offer":offer})


            context = {
                'requests': dabrha_requests,
            }        

        else:
            messages.info = (request, "You do Not Have Any Request")
        

        return render(
            request, "SCP/dabrha.html", context
        )


def dabrha_request(request):
    if request.method == "POST":
    

        customer = Customer.objects.get(pk=request.user.id)
        add_customer = dict(request.POST)
        add_customer["customer"] = customer
        form = DabrhaRequestForm(data=add_customer)


        if form.is_valid():
            try:
                if request.POST['img']:
                    save_data_with_image=form.save(commit=False)
                    save_data_with_image.img = request.POST['img']
                    save_data_with_image.save()
                else:
                    form.save()

                messages.success(request, "Your request has been sent")
                return redirect("scp:dabrha")

            except ValueError:
                error
                messages.error(request, "error")
                return redirect("scp:dabrha")

        else:
            print(form.errors.items())
            return redirect("scp:dabrha")

    else:
        form = DabrhaRequestForm()
        return render(request, "SCP/dabrhaForm.html", context={"form": form})


def dabrha_orders(request):

    requests = DabrhaRequest.objects.all()

    return render(
        request, "SCP/store/dabrha-orders.html", context={"requests": requests}
    )


def make_offers_for_dabrha(request, request_id):

    if request.method == "POST":
        print(request.user)
        offer = {
            'offer_price': request.POST['offer_price'],
            'store': request.user.id,
            'dabrha_request':request_id
        }
        form = DabrhaRequestFormForStores(data=offer)

        if form.is_valid():
            # price = form.cleaned_data["offer_price"]
            # request_object = DabrhaRequest.objects.filter(pk=request_id)
            # request_object.update(offer_price=price, has_an_offer=True)
            # print(f"{price}, {request_object}")

            form.save()
            print('validated')
            return redirect("scp:dabrha-orders")

        else:
            print('not validated')
            print(form.errors.items())
            return redirect("scp:dabrha-orders")

    else:
        return redirect("scp:dabrha_orders")



def cancel_dabrha_request(request, request_id):

    canceled_request = DabrhaRequest.objects.filter(pk=request_id)
    print('here')
    
    try:
        canceled_request.delete()

        messages.success(request, f"Request number:{request_id} deleted successfully")

        return redirect('scp:dabrha')

    except:
        return HttpResponseForbidden()










def LoginWSo(request):
  user=User.objects.get(id=4)
  login(request, user)

  response = redirect('/workshop/')
  return response


def LogoutPage(request):
  logout(request)
  response = redirect('/Workshop/')
  return response

# ------------------------------------------------------------------------------------------------#
# ------------------------------------IMPORTS-----------------------------------------------------#
# ------------------------------------------------------------------------------------------------#
from django.forms import ImageField
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from SCP.models import *
from .forms import (
    CustomUserCreationForm,
    StoreCreationForm,
    WorkshopUserCreationForm,
    AddPartsForm,
    PartsImages,
    AddserviceForm
)
from django.contrib import messages
from User.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

import datetime


from django.views.generic import TemplateView, CreateView


def is_customer(user):
    return user.is_authenticated and user.role == "CUSTOMER"


def is_store(user):
    return user.is_authenticated and user.role == "STORE"


def is_workshop(user):
    return user.is_authenticated and user.role == "WORKSHOP"


class CustomerLogin(LoginView):
    template_name = "SCP/login.html"


class WsLogin(LoginView):
    template_name = "SCP/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return self.redirec_ws()

    def redirec_ws(self):
        return redirect("scp:workshop-home")


def home_page(request):
    parts_categories = Categories.objects.all()
    context = {"categories": parts_categories}
    return render(request, "SCP/index.html", context)


def register(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}")
            return redirect("scp:home-page")

    else:
        form = CustomUserCreationForm()
        context = {"form": form}

        return render(request, "SCP/registration.html", context)


def customer_account(request):

    return render(request, "SCP/my-account.html")


def all_products(request, category_id):

   categories = Categories.objects.all()


   parts_relted_to_sotre = Store_parts.objects.all()
   parts = []   
   for part in parts_relted_to_sotre:
    parts.append({
        "part_obj":part.p_id,
         "part_img":Part_Image.objects.get(P_id=part.p_id),
         "price":part.Price,
         "store": part.S_id
         })


   context = {
        'parts': parts,
        'categories': categories
        }

   return render(request, "SCP/products.html", context)


def store_main_page(request):

    return render(request, "SCP/store/Dashboard.html")




def Product_Details(request, store_id ,partNo):

    Image = Part_Image.objects.get(P_id=partNo)
    part_details = Parts.objects.get(part_no=partNo)
    store_parts = Store_parts.objects.get(p_id=partNo ,S_id=store_id)

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
        # print(p.p_id)
        print(p.image_field)

    if request.method =="POST":
        Quantity=request.POST['Quantity']
        if Cart.objects.all().filter(C_id=User.objects.get(id=request.user.id),p_id=other_stores_with_the_same_products.p_id).exists():
            cart=Cart.objects.get(p_id=other_stores_with_the_same_products.p_id)
            Q=int(cart.Q)
            print(Q)
            Q+=int(Quantity)
            print(Q)
            cart.Q=Q
            cart.save()

        else:
            Cart.objects.create(C_id=User.objects.get(id=request.user.id),p_id=other_stores_with_the_same_products.p_id,Q=Quantity)
        response = redirect('/Cart/')
        return response
       

    return render(request, 'SCP/product-details.html', context)



def DeleteCart(request):
    ID=request.GET['DeleteID']
    if Cart.objects.all().filter(id=ID).exists():
        obj = Cart.objects.all().filter(id=ID)
        obj.delete()
    response = redirect('/Cart/')
    return response


def CartPage(request):
    cart = Cart.objects.all().filter(C_id=request.user.id)
    parts = []
    total=0
    for n in cart:
        parts.append({"part_obj":Parts.objects.get(part_no=n.p_id.p_id.part_no), "part_img":Part_Image.objects.get(P_id=Parts.objects.get(part_no=n.p_id.p_id.part_no)),"cart":n,"price":Store_parts.objects.get(id=n.p_id.id)})
        total+=Store_parts.objects.get(id=n.p_id.id).Price*n.Q
    

    context={
        "parts":parts,
        "total":total
    }
    
    return render(request, 'SCP/cart.html', context)




@user_passes_test(is_workshop, login_url="ws/login")
def workshop_main_page(request):

    obj = Services.objects.all().filter(W_id=request.user.id)

    obj1 = Workshop_Image.objects.get(W_id=User.objects.get(id=request.user.id))

    context = {
        "obj": obj,
        "obj1": obj1,
    }

    return render(request, "SCP/ws/ws.html", context)


# Creating new Store Account


def register_store(request):

    if request.method == "POST":
        form = StoreCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("scp:store-home")

        else:
            messages.info(request, "try another username")
            return redirect("scp:registerStore")

    else:
        form = StoreCreationForm()
        context = {"form": form}

        return render(request, "SCP/store/auth-register-basic.html", context)


def register_workshop(request):

    if request.method == "POST":
        form = WorkshopUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("scp:login")

    else:
        form = WorkshopUserCreationForm()
        context = {"form": form}

        return render(request, "SCP/ws/workshop-registration.html", context)


def add_parts(request):

    if request.method == "POST":
        form = AddPartsForm(request.POST)
        imageForm = PartsImages(request.POST, request.FILES)
        if form.is_valid() and imageForm.is_valid():
            added_part = form.save()
            part = Parts.objects.get(pk=added_part.part_no)
            image = imageForm.cleaned_data["image_field"]
            Part_Image.objects.create(P_id=part, image_field=image)
            messages.success(request, "part added to your store !")
            return redirect("scp:add-parts")

        else:
            messages.info(request, "add correct information")
            return redirect("scp:add-parts")

    else:
        category_types = {"categories": Categories.objects.all()}
        form = AddPartsForm()
        imageForm = PartsImages()
        context = {"imageForm": imageForm, "categories": Categories.objects.all()}
        return render(request, "SCP/store/add-parts.html", context)


def store_parts(request):

    all_parts = Parts.objects.all()
    parts_pks = all_parts.values_list("pk", flat=True)
    parts = []
    print(type(all_parts))
    # images= Part_Image.objects.filter(P_id__in=parts_pks).select_related('P_id')
    for n in all_parts:

        parts.append(
            {"part_obj": n, "part_img": Part_Image.objects.get(P_id=n.part_no)}
        )

    print(parts)

    return render(request, "SCP/store/show-parts.html", {"parts": parts})


def customers_orders(request):

    return render(request, "SCP/store/orders.html")




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
                        Services.objects.get(id=n.S_id.id),
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

            if request.method == "POST":
                Add_form = AddserviceForm(request.POST)
                if Add_form.is_valid():
                    Services.objects.create(
                        W_id=User.objects.get(id=request.user.id, role="WORKSHOP"),
                        name=Add_form.cleaned_data["name"],
                        price=Add_form.cleaned_data["price"],
                    )
                    response = redirect("/Workshop/")
                    return response
            context = {"form": Add_form}

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


def Update(request):
    if request.user.is_authenticated:
        if request.user.role == "WORKSHOP":
            Add_form = AddserviceForm()

            if request.method == "POST":
                Add_form = AddserviceForm(request.POST)
                if Add_form.is_valid():
                    service = Services.objects.get(
                        id=request.GET.get("UpdateID"), W_id=request.user.id
                    )
                    service.name = Add_form.cleaned_data["name"]
                    service.price = Add_form.cleaned_data["price"]
                    service.save()
                    response = redirect("/Workshop/")
                    return response
            context = {"form": Add_form}
            return render(request, "SCP/ws/Updateservice.html", context)
        else:
            response = redirect("/home/")
            return response

    else:
        response = redirect("/home/")
        return response
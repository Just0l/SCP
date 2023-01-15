#------------------------------------------------------------------------------------------------#
#------------------------------------IMPORTS-----------------------------------------------------#
#------------------------------------------------------------------------------------------------#
from django.forms import ImageField
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from SCP.models import *
from . forms import CustomUserCreationForm, StoreCreationForm, WorkshopUserCreationForm, AddPartsForm, PartsImages
from django.contrib import messages

from django.views.generic import TemplateView, CreateView




def home_page(request):
    parts_categories = Categories.objects.all()
    context = {'categories': parts_categories}
    return render(request, 'SCP/index.html', context)




def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('scp:home-page')

    else:
        form = CustomUserCreationForm()
        context = {'form':form}

        return render(request, 'SCP/registration.html', context) 



def customer_account(request):

    return render(request, 'SCP/my-account.html')



def category_products(request, category_id):

    category = get_object_or_404(Categories, pk=category_id)
    categories = Categories.objects.all()
    parts = Parts.objects.filter(category=category)
    parts_pks = parts.values_list('pk', flat=True)
    images= [Part_Image.objects.filter(P_id=pk) for pk in parts_pks]

    context = {
        'parts': parts,
        'categories': categories,
        'images': images
        }

    return render(request, 'SCP/shop-grid-sidebar-left.html', context)




def store_main_page(request):


    return render(request, 'SCP/store/Dashboard.html')


def workshop_main_page(request):


    return render(request, 'SCP/index-2.html')

# Creating new Store Account 

def register_store(request):

    if request.method == 'POST':
        form = StoreCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scp:store-home')

        else:
            messages.info(request, 'try another username')
            return redirect('scp:registerStore')

    else:
        form = StoreCreationForm()
        context = {'form': form}

        return render(request, 'SCP/store/auth-register-basic.html', context)



def register_workshop(request):

    if request.method == 'POST':
        form = WorkshopUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scp: workshop-home')
        


    else:
        form = WorkshopUserCreationForm()
        context = {'form': form}

        return render(request, 'SCP/workshop-registration.html', context)



def add_parts(request):
    
    if request.method == 'POST':
        form = AddPartsForm(request.POST)
        imageForm = PartsImages(request.POST, request.FILES)
        if form.is_valid() and imageForm.is_valid():
            added_part=form.save()
            part = Parts.objects.get(pk=added_part.part_no)
            print(part)
            image=imageForm.cleaned_data['image_field']
            Part_Image.objects.create(P_id=part, image_field=image)
            messages.success(request, 'part added to your store !')
            return redirect('scp:add-parts')

        else:
            print(form.errors)
            print(f'image field error :{imageForm.errors}')
            messages.info(request,'add correct information')
            return redirect('scp:add-parts')




    else:
        category_types = {'categories':Categories.objects.all()}
        form = AddPartsForm()
        imageForm = PartsImages()
        context = {
            'imageForm': imageForm,
            'categories':Categories.objects.all()
        }
        return render(request, 'SCP/store/add-parts.html', context)





def store_parts(request):

    all_parts = Parts.objects.all()
    parts_pks = all_parts.values_list('pk', flat=True)
    parts = []
    print(type(all_parts))
    # images= Part_Image.objects.filter(P_id__in=parts_pks).select_related('P_id')
    for n in all_parts:

        parts.append({"part_obj":n, "part_img":Part_Image.objects.get(P_id=n.part_no)})

    print(parts)        

    return render(request, 'SCP/store/show-parts.html', {'parts':parts})



def customers_orders(request):


    return render(request, 'SCP/store/orders.html')
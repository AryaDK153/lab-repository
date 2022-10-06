#LAB01
from django.shortcuts import render
from wishlist.models import BarangWishlist
#LAB02
from django.http import HttpResponse
from django.core import serializers
#LAB03
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# LAB 03: Cookies & Session
# Registration Form
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

# Login Function
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
            # login(request, user)
            # return redirect('wishlist:show_wishlist')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

# Logout Function
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response
    # logout(request)
    # return redirect('wishlist:login')

# Access-Limited Wishlist Page
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Arya',
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist.html", context)

# Access-Limited Wishlist Page
def show_wishlist_ajax(request):
    return render(request, "wishlist_ajax.html")

def submit_wishlist_ajax(request):
    return


# # LAB 01: Create your views here.
# def show_wishlist(request):
#     data_barang_wishlist = BarangWishlist.objects.all()
#     context = {
#         'list_barang': data_barang_wishlist,
#         'nama': 'Arya'
#     }
#     return render(request, "wishlist.html", context)





# LAB 02: view json/xml
def show_wishlist_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_wishlist_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# view json/xml + id
def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
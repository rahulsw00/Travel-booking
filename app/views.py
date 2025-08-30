from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def index(request):

    if request.method == 'POST':
        sourceCity = request.POST.get('sourceCities')
        destinationCity = request.POST.get('destinationCities')
        mode = request.POST.get('modeOfTransport')
        print(sourceCity)
        if sourceCity == "0" or destinationCity == "0":
            availableOptions = travelOptions.objects.all()
        elif mode == "All":
            availableOptions = travelOptions.objects.filter(source=sourceCity, destination=destinationCity)
        else:
            availableOptions = travelOptions.objects.filter(source=sourceCity, destination=destinationCity, travelType=mode)
    else:
        availableOptions = travelOptions.objects.all()
    cities = city.objects.all()
    return render(request, "index.html", {"availableOptions": availableOptions, "cities":cities})

@login_required(login_url='login')
def book(request, id):
    selectedOption = travelOptions.objects.filter(id=id)
    if request.method == "POST":
        user = request.user
        print(user)
        if user:
            user = User.objects.get(username=user)
            travelOption = travelOptions.objects.get(id=id)
            numberOfSeats = request.POST.get("quantity")
            totalPrice = request.POST.get("total")
            status = "Confirmed"
            print(user, travelOption, numberOfSeats, totalPrice, status)
            booking.objects.create(user=user, travelOption=travelOption, numberOfSeats=numberOfSeats, totalPrice=totalPrice, status=status)
            return redirect('profile')

    return render(request, 'book.html', {"selectedOption": selectedOption, "travelOptionId":id})

def confirmCancel(request,id):
    bookings = booking.objects.all()
    return render(request, 'profile.html', {'bookings':bookings, 'cancel':True, 'id':int(id)})

def cancel(request,id):
    item = booking.objects.get(id=id)
    item.delete()
    return redirect('profile')

@login_required(login_url='login')
def profile(request):
    userBookings = booking.objects.filter(user=request.user)
    return render(request, "profile.html", {"bookings": userBookings})

@login_required(login_url='login')
def editProfile(request, id):
   user = get_object_or_404(User, id=id)
   
   if request.method == 'POST':
       user.first_name = request.POST.get('first_name')
       user.last_name = request.POST.get('last_name')
       user.email = request.POST.get('email')
       user.username = request.POST.get('username')
       user.save()
       
       messages.success(request, 'Profile updated successfully!')
   
   return render(request, "edit_profile.html", {'user': user})
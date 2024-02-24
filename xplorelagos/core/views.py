import os
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth import authenticate,login

from .models import user_info_extend, User
from .forms import CustomerUserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from random import randint

secret_key = os.getenv('SECRET_KEY')
public_key = os.getenv('PUBLIC_KEY')

def logout_view(request):
    auth.logout(request)
    return redirect(login_view)

def login_view(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists():
            user = authenticate(request,
                username=User.objects.get(email=request.POST["email"]).username,
                password=request.POST["password"]
            )

            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect email or password')
                return redirect('login')
        else:
            messages.error(request, "User doesn't exist. If you don't have an account please create one")
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'Sign.html')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        qwer = email.split('@', 1)[0]
        print(qwer)
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'SignUp.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'SignUp.html')

        form_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": qwer,
            "email": email,
            "password1": password,
            "password2": confirm_password
        }
        form = CustomerUserCreationForm(form_data)

        if form.is_valid():
            print('its valid')
            new_user = form.save()
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # new_user = User.objects.create(username=username, email=email, password=password)

            user_extra = user_info_extend.objects.create(
                user=new_user,
                phone_number=phone,
                country=country
            )

            login(request, new_user)
            print(f"${new_user} user logged in")
            return redirect('dashboard')
        
        else:
            errors = form.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"{error}")
            return render(request, 'SignUp.html')

    return render(request, 'SignUp.html')

def landingpage(request):
    return render(request, 'Home.html')

def aboutpage(request):
    return render(request, 'AboutUs.html')

def experience(request):
    return render(request, 'Experience.html')

def adventure(request):
    return render(request, 'Select-adventure.html')

def culinary(request):
    return render(request, 'Select-culinary.html')

def cultural(request):
    return render(request, 'Select-cultural.html')

def luxury(request):
    return render(request, 'Select-luxury.html')

def TandD(request):
    if request.method == 'POST':
        post_data = request.POST
        selected_activities_json = post_data.get('selected_activities')
        selected_activities = json.loads(selected_activities_json)

        prices = {}

        for activity in selected_activities:
            activity_name = activity['name']
            activity_price = activity['price']
            prices[activity_name] = activity_price
            
        request.session['selected_activities'] = selected_activities
        request.session['prices'] = prices

        context = {
            'selected_activities': selected_activities,
            'prices': prices,
        }
        
        return render(request, 'TimeAndDate.html', context)
    else:
        return render(request, 'TimeAndDate.html')

def schedule_trip(request):
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated:
            selected_date = request.POST.get('date')
            selected_startTime = request.POST.get('start-time')
            selected_endTime = request.POST.get('end-time')
            selected_noPeople = request.POST.get('people')
            selected_location = request.POST.get('locationDisplay')

            request.session['selected_date'] = request.POST.get('date')
            request.session['selected_startTime'] = request.POST.get('time')
            request.session['selected_endTime'] = request.POST.get('end-time')
            request.session['selected_noPeople'] = request.POST.get('people')
            request.session['selected_location'] = request.POST.get('selectedLocation')

            return redirect('dashboard')
        else:
            request.session['selected_date'] = request.POST.get('date')
            request.session['selected_startTime'] = request.POST.get('time')
            request.session['selected_endTime'] = request.POST.get('end-time')
            request.session['selected_noPeople'] = request.POST.get('people')  
            request.session['selected_location'] = request.POST.get('selectedLocation')
          
            return redirect('sign_up')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        
        context = {
            'user_name': user.first_name + ' ' + user.last_name,
            'user_email': user.email
        }
        if request.session:
            selected_options = request.session.get('selected_options', [])
            selected_date = request.session.get('selected_date')
            selected_startTime = request.session.get('selected_startTime')
            selected_endTime = request.session.get('selected_endTime')
            selected_noPeople = request.session.get('selected_noPeople')
            selected_location = request.session.get('selected_location')
            prices = request.session.get('prices', {})

            context = {
                        'user_name': user.first_name + ' ' + user.last_name,
                        'user_email': user.email,
                        'selected_options': selected_options,
                        'selected_date': selected_date,
                        'selected_startTime': selected_startTime,
                        'selected_endTime': selected_endTime,
                        'selected_noPeople': selected_noPeople,
                        'selected_location': selected_location,
                        'prices': prices
                        }
            return render(request, 'Dashboard.html', context)

        return render(request, 'Dashboard.html', context)
    else:
        return render(request, 'Sign.html')

def callback_view(request):
    return HttpResponse("Callback received successfully.")

def handle_payment(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')

        total_amount, orders = calculate_total_amount_and_orders(request.POST)
        
        # if token:
        #     order_response = order(token, full_name, email, mobile_number, total_amount, orders)
        #     print("Order response:", order_response)
        # else:
        #     print("Authentication failure")

        return redirect('review')

def calculate_total_amount_and_orders(request, post_data):
    total_amount = 0
    orders = []
    
    selected_options = request.session.get('selected_options', [])
    prices = request.session.get('prices', {})
    
    for idx, activity in enumerate(selected_options, start=101):
        if activity in prices:
            price = float(prices[activity])
            total_amount += price
            order_id = str(idx)
            orders.append({
                "orderId": order_id,
                "currency": "USD",
                "amount": "{:.2f}".format(price),
                "productId": activity.lower().replace(' ', '_'),
                "productDescription": activity
            })

    return total_amount, orders

def review(request):
     if request.user.is_authenticated:
        user = request.user
        
        context = {
            'user_name': user.first_name + ' ' + user.last_name,
            'user_email': user.email
        }
        if request.session:
            selected_options = request.session.get('selected_options', [])
            selected_date = request.session.get('selected_date')
            selected_startTime = request.session.get('selected_startTime')
            selected_endTime = request.session.get('selected_endTime')
            selected_noPeople = request.session.get('selected_noPeople')
            selected_location = request.session.get('selected_location')
            prices = request.session.get('prices', {})

            context = {
                        'user_name': user.first_name + ' ' + user.last_name,
                        'user_email': user.email,
                        'selected_options': selected_options,
                        'selected_date': selected_date,
                        'selected_startTime': selected_startTime,
                        'selected_endTime': selected_endTime,
                        'selected_noPeople': selected_noPeople,
                        'selected_location': selected_location,
                        'prices': prices
                        }
    
        return render(request, 'Dashboard2.html', context)


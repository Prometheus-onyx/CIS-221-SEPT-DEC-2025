from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Product, Category, SaleOffers
from .forms import SignupForm, LoginForm


def index(request: HttpRequest):
    categories = Category.objects.all()
    products = Product.objects.all()
    sale_offers = SaleOffers.objects.all()

    context = { 
        'categories': categories,
        'products': products,
        'sale_offers': sale_offers,
    }

    return render(request, 'index.html', context)


def login(request: HttpRequest):
    # The template uses the same action for both forms. Distinguish by presence of fields.
    if request.method == 'POST':
        # If signup fields are present we'll treat this as signup
        if 'firstName' in request.POST or 'confirm_password' in request.POST:
            # create a form instance and populate it with data from the request:
            form = SignupForm(request.POST)
            login_form = LoginForm()
            if form.is_valid():
                name = form.cleaned_data['firstName'] + ' ' + form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Choose a username - use the email local part or full email to keep unique
                ### safe: handles None/empty and stops after the first split
                username = (name or '').split(maxsplit=1)[0]
    
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                # If you want to store full name, split into first/last
                parts = name.strip().split(None, 1)
                if parts:
                    user.first_name = parts[0]
                    if len(parts) > 1:
                        user.last_name = parts[1]
                user.save()

                # Authenticate and log in
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Signup successful. You are now logged in.')
                    return redirect('index')
                else:
                    messages.error(request, 'There was a problem logging in after signup.')
            else:
                # form errors will be rendered
                return render(request, 'login.html', {'signup_form': form, 'login_form': login_form})

        else:
            # Handle login
            login_form = LoginForm(request.POST)
            signup_form = SignupForm()
            if login_form.is_valid():
                username = login_form.cleaned_data['name']
                password = login_form.cleaned_data['password']

                # We stored usernames as email in signup; authenticate with username=email
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Logged in successfully.')
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid email or password.')
                    return render(request, 'login.html', {'login_form': login_form, 'signup_form': signup_form})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'signup_form': signup_form})

    # GET request
    return render(request, 'login.html', {'login_form': LoginForm(), 'signup_form': SignupForm()})

#def register(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already used')
                return redirect('register.html')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('index')
        else:
            messages.info(request, 'Password not the same')
            return redirect('register')


    return render(request, 'register.html', {})        
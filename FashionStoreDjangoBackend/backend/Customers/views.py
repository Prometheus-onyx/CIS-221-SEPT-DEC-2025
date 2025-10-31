from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Product, Category, SaleOffers
from .forms import SignupForm, LoginForm


def home(request: HttpRequest):
    categories = Category.objects.all()
    products = Product.objects.all()
    sale_offers = SaleOffers.objects.all()

    context = { 
        'categories': categories,
        'products': products,
        'sale_offers': sale_offers,
    }

    return render(request, 'home.html', context)

def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, f'Invalid Username "{username}"')
            return redirect('login')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, f"Invalid Password '{password}'")
            return redirect('login')
        else:
            # Log in the user and redirect to the home page upon successful login
            auth_login(request, user)
            return redirect('home')
    
    # Render the login page template (GET request)
    return render(request, 'login.html')

def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, f"Username '{username}' already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save();
        
        # Display an information message indicating successful account creation
        messages.info(request, f"Welcome {user} your account is created Successfully!")
        return redirect('home')
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')
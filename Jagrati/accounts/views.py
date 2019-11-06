from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import User, UserManager

# Create your views here.
def login_signup(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(username = email, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {
                    'login_error' : "Invalid Username or Password",
                }
                return render(request, 'accounts/login_signup.html', context)

            # form = LoginForm(request.POST)
            # if form.is_valid():
            #     email = form.cleaned_data.get('email')
            #     raw_password = form.cleaned_data.get('password')
            #     user = authenticate(username = email, password = raw_password)
            #     if user is not None:
            #         login(request, user)
            #         redirect('home')
        if request.POST.get('submit') == 'sign_up':
            email = request.POST['email']
            desig = request.POST['desig']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            error = ''
            obj = User.objects.filter(email=email)
            if obj.exists():
                error = "Account with entered email already exists"
                return render(request, "accounts/login_signup.html", {'signup_error' : error})
            if password1 and password2 and password1 != password2:
                error = "Passwords don't match"
                return render(request, "accounts/login_signup.html", {'signup_error' : error})
            
            obj = User(email = email, desig = desig) #ADD IS_ACTIVE=FALSE AT TIME OF EMAIL CONFIRMATION
            obj.set_password(password1) # To save password as hash
            obj.save()
            user = authenticate(username=email, password=password1)
            login(request, user)
            return redirect('home')

            # form = SignUpForm(request.POST)
            # if form.is_valid():
            #     form.save()
            #     email = form.cleaned_data.get('email')
            #     raw_password = form.cleaned_data.get('password')
            #     user = authenticate(username=username, password=raw_password)
            #     login(request, user)
            #     return redirect('home')

    return render(request, 'accounts/login_signup.html')

def logout_fun(request):
    logout(request)
    return redirect('home')

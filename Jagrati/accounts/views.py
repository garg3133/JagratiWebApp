from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import User, UserManager
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

# Create your views here.
def login_signup(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            email = request.POST['email']
            password = request.POST['password']
            
            obj = User.objects.filter(email=email)
            if obj.exists() and not obj[0].is_active:
                context = {
                    'login_error' : "Confirm your mail first.",
                }
                return render(request, 'accounts/login_signup.html', context)  # Must open other html page with option to resend mail

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
            
            obj = User(email = email, desig = desig, is_active = False) #ADD IS_ACTIVE=FALSE AT TIME OF EMAIL CONFIRMATION
            obj.set_password(password1) # To save password as hash
            obj.save()

            current_site = get_current_site(request)
            html_message = render_to_string('accounts/account_activation_email.html', {
                'user': obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
                'token': account_activation_token.make_token(obj),
            })
            send_mail(
                'Acount Activation',
                'Activate your account',
                'jagrati123321@gmail.com',
                [email],
                fail_silently=False,
                html_message = html_message,
            )
            return render(request, 'accounts/activation_mail_sent.html', {'user' : obj,})
            # user = authenticate(username=email, password=password1)
            # login(request, user)
            # return redirect('home')



            # form = SignUpForm(request.POST)
            # if form.is_valid():
            #     form.save()
            #     email = form.cleaned_data.get('email')
            #     raw_password = form.cleaned_data.get('password')
            #     user = authenticate(username=username, password=raw_password)
            #     login(request, user)
            #     return redirect('home')

    return render(request, 'accounts/login_signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


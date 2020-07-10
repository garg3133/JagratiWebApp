from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import User, UserManager
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

from home.models import Volunteer

# from django.contrib.auth.views import PasswordResetConfirmView
# from .forms import CustomSetPasswordForm

# Create your views here.

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     form_class = CustomSetPasswordForm

def login_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    # next_site = 'dashboard'
    # if request.GET.get('next') is not None:
    #     next_site = request.GET['next']
    #     print(next_site)
    next_site = request.GET.get('next', 'dashboard')

    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            email = request.POST['email']
            password = request.POST['password']

            context = {}
            user = authenticate(username = email, password = password)

            if user is not None:
                volun = Volunteer.objects.filter(email=user)
                if not user.auth and volun.exists():
                    # If User has already completed the profile
                    # but is not yet verified by the admin
                    context['login_error'] = 'User is not yet authenticated by the Admin. Kindly contact Admin.'
                    return render(request, 'accounts/login_signup.html', context)

                login(request, user)

                if not user.auth:
                    return redirect('set_profile')
                else:
                    return redirect(next_site)
            else:
                user = User.objects.filter(email=email)
                if user.exists() and user[0].check_password(password) and not user[0].is_active:
                    # Authentication failed because user is not active
                    context['login_error'] = 'Account not Activated.<br><a href="#">Resend Activation Email?</a>'
                else:
                    context['login_error'] = 'Invalid credentials'
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
            user = User.objects.filter(email=email)
            if user.exists():
                error = "Account with entered email already exists"
                return render(request, "accounts/login_signup.html", {'signup_error' : error})
            if password1 and password2 and password1 != password2:
                error = "Passwords don't match"
                return render(request, "accounts/login_signup.html", {'signup_error' : error})

            user = User(email=email, desig=desig, is_active=False)
            user.set_password(password1) # To save password as hash
            user.save()

            # Send Account Activation Email
            current_site = get_current_site(request)

            from_email = settings.DEFAULT_FROM_EMAIL
            to = [email]
            subject = 'Jagrati Acount Activation'
            html_message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            plain_message = strip_tags(html_message)
            send_mail(
                subject, plain_message, from_email, to,
                fail_silently=False, html_message=html_message,
            )

            return render(request, 'accounts/activation_mail_sent.html', {'user' : user,})
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
    next_site = request.GET.get('next', 'home')
    logout(request)
    return redirect(next_site)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        # For activation link to work only once
        if user.is_active:
            user = None
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # Was required in cpanel...
        user.is_admin = False
        user.is_staff = False
        user.is_superuser = False
        user.auth = False
        # ...till here
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


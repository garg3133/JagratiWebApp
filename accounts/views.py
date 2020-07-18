# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# local Django
from home.models import Volunteer
from .models import User, UserManager, Profile
from .tokens import account_activation_token

# Create your views here.

def login_signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_site = request.GET.get('next', 'dashboard')

    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            email = request.POST['email']
            password = request.POST['password']

            context = {}
            user = authenticate(username=email, password=password)

            if user is not None:
                # For cpanel...
                if not user.is_active:
                    context['login_error'] = 'Account not Activated.<br><a href="#">Resend Activation Email?</a>'
                    return render(request, 'accounts/login_signup.html', context)
                # ...till here.

                volun = Volunteer.objects.filter(email=user)
                if not user.auth and volun.exists():
                    # If User has already completed the profile
                    # but is not yet verified by the admin
                    context['login_error'] = 'User is not yet authenticated by the Admin. Kindly contact Admin.'
                    return render(request, 'accounts/login_signup.html', context)

                login(request, user)
                messages.success(request, "Logged in Successfully!")
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
            # desig = request.POST['desig']
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

            user = User(email=email, is_active=False)
            user.set_password(password1) # To save password as hash
            user.save()

            # Send Account Activation Email
            current_site = get_current_site(request)

            from_email = settings.DEFAULT_FROM_EMAIL
            to = [email]
            subject = '[noreply] Jagrati Acount Activation'
            html_message = render_to_string('accounts/email/account_activation_email.html', {
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

            return redirect('signup_success')


            # form = SignUpForm(request.POST)
            # if form.is_valid():
            #     form.save()
            #     email = form.cleaned_data.get('email')
            #     raw_password = form.cleaned_data.get('password')
            #     user = authenticate(username=username, password=raw_password)
            #     login(request, user)
            #     return redirect('home')

    return render(request, 'accounts/login_signup.html')

def complete_profile(request):
    """ For completing the Profile after successful signup and activation of account.
        Mandatory before accessing the Dashboard."""
    user = request.user

    # Redirect to Dashboard if Profile is already complete
    if Profile.objects.filter(user=user).exists():
        return redirect('dashboard')

    # if user.desig == 'v':
    if request.method == 'POST':
        roll_no = request.POST['roll_no']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        alt_email = request.POST['alt_email']
        batch = request.POST['batch']
        programme = request.POST['programme']
        street_address1 = request.POST['street_address1']
        street_address2 = request.POST['street_address2']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        dob = request.POST['dob']
        contact_no = request.POST['contact_no']
        profile_image = request.FILES.get('profile_image')

        profile = Profile(
            user=user, first_name=first_name, last_name=last_name,
            profile_image=profile_image, gender=gender, alt_email=alt_email,
            contact_no=contact_no, street_address1=street_address1,
            street_address2=street_address2, city=city, state=state,
            pincode=pincode,
        )
        profile.save()

        volun = Volunteer(
            email=user, roll_no=roll_no, dob=dob, batch=batch,
            programme=programme,
        )
        volun.save()

        # Notify Admin for New User Sign Up
        current_site = get_current_site(request)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = settings.ADMINS_EMAIL
        subject = '[noreply] New User Signed Up'
        html_message = render_to_string('accounts/email/account_authentication_email.html', {
            'profile': profile,
            'volun': volun,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(volun.email.pk)),
            'token':account_activation_token.make_token(volun.email),
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject, plain_message, from_email, to,
            fail_silently=False, html_message=html_message,
        )

        logout(request)
        return redirect('profile_completed')

    return render(request, 'accounts/volunteer_profile.html')


def logout_view(request):
    next_site = request.GET.get('next', 'home')
    logout(request)
    return redirect(next_site)

def account_activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, "Account Activated Successfully!")
        return redirect('set_profile')
    else:
        msg = "You have either entered a wrong link or your account has already been activated."
        return render(request, 'accounts/token_expired.html', {'msg': msg, 'act_token': True})

def account_authentication(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.auth = True
        user.save()

        # Notify User of Account Authenticated
        current_site = get_current_site(request)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]
        subject = '[noreply] Account Authenticated'
        html_message = render_to_string('accounts/email/account_authenticated_email.html', {
            'volun': user.volunteer,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject, plain_message, from_email, to,
            fail_silently=False, html_message=html_message,
        )

        return redirect('account_authenticated')
    else:
        msg = "You have either entered a wrong link or some admin has already authenticated this account."
        return render(request, 'accounts/token_expired.html', {'msg': msg})

def signup_success(request):
    return render(request,'accounts/signup_success.html')

def profile_completed(request):
    return render(request,'accounts/profile_completed.html')

def account_authenticated(request):
    return render(request,'accounts/account_authenticated.html')


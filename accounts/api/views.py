from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import RegistrationSerializer, CreateProfileSerializer
from accounts.tokens import account_activation_token
from accounts.models import User, Profile, AuthorisedDevice
from apps.volunteers.api.serializers import CreateVolunteerSerializer


# NON-VIEWS FUNCTIONS

def validate_email(email):
    """Returns None if User with 'email' does not exists."""
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user != None:
        return email


# VIEWS FUNCTIONS

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

    if request.method == 'POST':
        data = {}
        # Validate Email (Password Validation in serializers.py)
        email = request.data.get('email', '0')
        if validate_email(email) != None:
            data['response'] = 'Error'
            data['error_message'] = 'That email is already in use.'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully Registered!'
            data['email'] = user.email

            # Send Account Activation Email
            current_site = get_current_site(request)

            from_email = settings.DEFAULT_FROM_EMAIL
            to = [user.email]
            subject = 'Jagrati Acount Activation'
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

        else:
            data = serializer.errors
        return Response(data)


class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}

        email = request.POST.get('email')
        password = request.POST.get('password')
        device_id = request.POST.get('device_id')

        if device_id is None:
            data['response'] = 'Error'
            data['error_message'] = 'Device id is missing.'
            return Response(data, status=400)

        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            # For cpanel...
            if not user.is_active:
                data['response'] = 'Error'
                data['error_message'] = 'User Account not Activated. Please check your inbox/spam for an Account Activation Email.'
                return Response(data, status=403)
            # ...till here.

            profile = Profile.objects.filter(user=user)
            if profile.exists() and not user.auth:
                # If User has already completed the profile
                # but is not yet verified by the admin
                data['response'] = 'Error'
                data['error_message'] = 'User is not yet authenticated by the Admin. Kindly contact Admin.'
                return Response(data, status=403)

            # Save the device_id of the user
            device_info = AuthorisedDevice.objects.filter(user=user, device_id=device_id)
            if device_info.exists():
                device_info = device_info[0]
                device_info.active = True
                device_info.save()
            else:
                AuthorisedDevice.objects.create(user=user, device_id=device_id)

            data['response'] = 'Successfully Authenticated!'
            data['auth'] = (user.auth is True)
            data['email'] = email
            data['token'] = token.key

            if user.auth:
                # Send additional information/permissions required.
                pass

        else:
            data['response'] = 'Error'

            user = User.objects.filter(email=email)
            if user.exists() and user[0].check_password(password) and not user[0].is_active:
                # Authentication failed because user is not active
                data['error_message'] = 'User Account not Activated. Please check your inbox/spam for an Account Activation Email.'
            else:
                data['error_message'] = 'Invalid credentials'

        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def complete_profile_view(request):
    user = request.user
    profile = Profile.objects.filter(user=user)
    if profile.exists():
        data = {
            'response': 'Error',
            'error_message': 'Profile already exists.'
        }
        return Response(data, status=400)

    # Additional data will automatically be ignored
    profile_serializer = CreateProfileSerializer(data=request.data)
    volun_serializer = CreateVolunteerSerializer(data=request.data)

    data = {}
    if profile_serializer.is_valid() and volun_serializer.is_valid():
        # Save Profile
        profile = profile_serializer.save(user=user)
        # Save Volunteer
        volun = volun_serializer.save(profile=profile)
        data['response'] = "Profile Created Successfully!"

        # Notify Admin for New User Sign Up
        current_site = get_current_site(request)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = settings.ADMINS_EMAIL
        subject = '[noreply] New User Signed Up'
        html_message = render_to_string('accounts/email/account_authentication_email.html', {
            'profile': profile,
            'volun': volun,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject, plain_message, from_email, to,
            fail_silently=False, html_message=html_message,
        )
        return Response(data, status=201)

    # Both .is_valid() must be called before accessing errors
    # profile_serializer.is_valid() is surely called before
    errors = profile_serializer.errors.copy()
    # Not sure if volun_serializer.is_valid() has been called before
    if not volun_serializer.is_valid():
        errors.update(volun_serializer.errors)
    return Response(errors, status=400)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}

        device_id = request.POST.get('device_id')
        if device_id is None:
            data['response'] = 'Error'
            data['error_message'] = 'Device id is missing.'
            return Response(data, status=400)
        else:
            AuthorisedDevice.objects.filter(
                user=request.user, device_id=device_id).update(active=False)
            data['response'] = "Logged out successfully"
            return Response(data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def check_login_status(request):
    data = {}

    device_id = request.POST.get('device_id')
    if device_id is None:
        data['response'] = 'Error'
        data['error_message'] = 'Device id is missing.'
        return Response(data, status=400)
    else:
        device_info = AuthorisedDevice.objects.filter(user=request.user, device_id=device_id)
        if device_info.exists() and device_info[0].active:
            data['login_status'] = True
        else:
            data['login_status'] = False
        return Response(data, status=200)

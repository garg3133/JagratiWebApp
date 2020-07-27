from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.tokens import account_activation_token
from home.api.serializers import UpdateProfileSerializer
from accounts.models import Profile


# VIEWS FUNCTIONS

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_profile_view(request):
    profile = Profile.objects.filter(user=request.user)
    if profile.exists():
        data = {
            'response': 'Error',
            'error_message': 'Profile already exists.'
        }
        return Response(data, status=400)
    else:
        profile = Profile(user=request.user)

    serializer = UpdateProfileSerializer(profile, data=request.data)
    # print(repr(serializer))
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['response'] = "Profile Created Successfully!"

        # Notify Admin for New User Sign Up
        volun = Profile.objects.get(user=request.user)
        current_site = get_current_site(request)

        from_email = settings.DEFAULT_FROM_EMAIL
        to = settings.ADMINS_EMAIL
        subject = '[noreply] New User Signed Up'
        html_message = render_to_string('accounts/email/account_authentication_email.html', {
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
        return Response(data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_profile_view(request):

    try:
        volun = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UpdateProfileSerializer(volun)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UpdateProfileSerializer(volun, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Profile Updated Successfully!"
            data['data'] = serializer.data
            return Response(data)
        return Response(serializer.errors, status=400)

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import RegistrationSerializer
from accounts.tokens import account_activation_token
from accounts.models import User
from home.models import Volunteer


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
		user = authenticate(email=email, password=password)
		if user is not None:
			try:
				token = Token.objects.get(user=user)
			except Token.DoesNotExist:
				token = Token.objects.create(user=user)

			volun = Volunteer.objects.filter(email=user)
			if not user.auth and volun.exists():
				# If User has already completed the profile
				# but is not yet verified by the admin
				data['response'] = 'Error'
				data['error_message'] = 'User is not yet authenticated by the Admin. Kindly contact Admin.'
				return Response(data)

			data['response'] = 'Successfully Authenticated!'
			data['auth'] = user.auth
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


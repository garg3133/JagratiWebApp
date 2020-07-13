from rest_framework import serializers

from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only': True},
		}	

	def	save(self):
		user = User(
			email=self.validated_data['email'],
			is_active=False,
		)
		# Validate Password
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			data = {
				'response': 'Error',
				'error_message': 'Passwords must match.',
			}
			# This data is sent directly to the caller
			raise serializers.ValidationError(data)

		user.set_password(password)
		user.save()
		return user
from rest_framework import serializers

from accounts.models import User, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self):
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


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'gender', 'contact_no', 'alt_email',
            'street_address1', 'street_address2', 'city', 'state', 'pincode',
            'profile_image'
        ]

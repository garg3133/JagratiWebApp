from rest_framework import serializers

from accounts.models import Profile


class UpdateProfileSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(max_length=350, required=False)

    class Meta:
        model = Profile
        fields = [
            "id",
            "roll_no",
            "first_name",
            "last_name",
            "gender",
            "batch",
            "programme",
            "dob",
            "contact_no",
            "alt_email",
            "street_address1",
            "street_address2",
            "city",
            "state",
            "pincode",
            "profile_image",
        ]

from rest_framework import serializers

from apps.volunteers.models import Volunteer

class CreateVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['roll_no', 'batch', 'programme', 'dob']

        def validate_roll_no(self, value):
            volun = Volunteer.objects.filter(roll_no=roll_no)
            if volun.exists():
                raise serializers.ValidationError('Volunteer with entered roll no. already exists.')
            return value

# WE CAN USE NESTED REPRESENTATION FOR PROFILE AND UPDATE_PROFILE
# AS THEY NEED TO BE CREATED IN THIS APP
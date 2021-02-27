from rest_framework import serializers

from apps.students.models import Student



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'gender', 'school_class', 'village', 'contact_no', 'guardian_name', 'restricted']
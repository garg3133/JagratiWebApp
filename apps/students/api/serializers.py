from rest_framework import serializers

from apps.students.models import Student



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
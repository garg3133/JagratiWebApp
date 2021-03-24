from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    feedback = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=400)
    
    def __str__(self):
        return self.email

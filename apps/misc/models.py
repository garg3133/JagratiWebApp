from django.db import models

# Create your models here.

class Initiative(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    thumbnail = models.ImageField(upload_to='../media/images/') 

    def __str__(self):
        return self.title

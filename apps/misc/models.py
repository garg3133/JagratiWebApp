from django.db import models

# Create your models here.

class Initiative(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    thumb_url = models.URLField(max_length=200,blank=True) 
    thumbnail = models.ImageField(upload_to='misc/initiatives',blank=True)

    def __str__(self):
        return self.title
    
          

    

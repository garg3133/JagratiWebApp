from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Initiative(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    thumb_url = models.URLField(max_length=200,blank=True) 
    thumbnail = models.ImageField(upload_to='misc/initiatives',blank=True)
    
    def save(self,*args, **kwargs): # if both thumbnail and thumb_url are absent, raise a validation error
        if not self.thumb_url  and not self.thumbnail:
            raise ValidationError('Atleast one field should be filled')   
        else:
            super(Initiative, self).save(*args, **kwargs) 
        

    def __str__(self):
        return self.title

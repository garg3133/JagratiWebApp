from django.db import models
from PIL import Image

# Create your models here.
class Initiative(models.Model):

	title = models.CharField(max_length = 20, verbose_name = 'Initiative Name')
	description = models.CharField(max_length = 200, verbose_name = 'Initiative Discription')
	thumbnail = models.ImageField(null = True, upload_to = 'initiative/')

	def __str__(self):
		return self.title
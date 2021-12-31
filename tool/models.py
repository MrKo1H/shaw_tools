from django.db import models

# Create your models here.

class Tool(models.Model):
	name = 	models.CharField(max_length=200, primary_key = True)
	cost =  models.IntegerField(default=0, null=False)
	describe = models.CharField(max_length=300)
	
	def __str__(self):
		return self.name
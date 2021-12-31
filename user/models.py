from django.db import models
# Create your models here.


class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	user_id  = models.AutoField(primary_key=True,editable=False)
	credit   = models.IntegerField(default=0)
	create   = models.DateTimeField(auto_now_add=True, null=True)
	last_use = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username


class Bill(models.Model):
	bill_id = models.CharField(max_length=30)
	user_id = models.CharField(max_length=30)
	payment = models.IntegerField(null=False)	
	date 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.bill_id
from django.db import models

# Create your models here.

class TargetUser(models.Model):
	fbid = models.CharField(max_length=40)
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name

class SentUser(models.Model):
	fbid = models.CharField(max_length=40)
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name

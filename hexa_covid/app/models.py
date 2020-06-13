from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Hexlandcell(models.Model):
	row = models.IntegerField()
	col = models.IntegerField()
	name = models.CharField(max_length=40)
	is_affected = models.BooleanField(default=False)
	# country = []
	# name_to_idx = {}
	def __str__(self):
		return self.name
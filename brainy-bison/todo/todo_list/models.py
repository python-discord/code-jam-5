"""Create your models here."""

from django.db import models


class List(models.Model):
	"""docstring for ClassName."""

    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    def __str__(self):
		return (self.item + ' | ' + str(self.completed))

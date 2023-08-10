from django.db import models
from .topics import *

# Create your models here.
class Exam(models.Model):
  
    name = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.ForeignKey(Topics,on_delete=models.CASCADE,null=True)

    premium_content = models.BooleanField(default=True)

    arrangement = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['arrangement']
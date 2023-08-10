from django.db import models
from .topics import *

# Create your models here.
# from .exam import *

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(default=None)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True)
    premium_content = models.BooleanField(default=True)

    arrangement = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Topic Lessons"
        verbose_name = "Lesson"
        ordering = ['arrangement']
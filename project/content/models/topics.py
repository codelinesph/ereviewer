from django.db import models
from .subject import *

# Create your models here.
# from .exam import *

class Topics(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(default=None)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    premium_content = models.BooleanField(default=True)

    assessment_limit = models.PositiveSmallIntegerField(default=0, null=True)

    arrangement = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subject Topics"
        verbose_name = "Topic"
        ordering = ['arrangement']
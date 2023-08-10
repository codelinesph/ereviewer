from django.db import models

from .question import *

# Create your models here.
class Answer(models.Model):
    answer = models.CharField(max_length=2000)
    is_correct_answer = models.BooleanField(default=False)
    reasons = models.CharField(null=True, max_length=1000, blank=True)
    links = models.CharField(null=True, max_length=1000, blank=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
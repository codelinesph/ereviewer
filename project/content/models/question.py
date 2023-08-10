from django.db import models
from .exam import *
# Create your models here.

class Question(models.Model):
    question = models.TextField()

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    premium_content = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    def correct_answers(self):
        return self.answer_set.filter(is_correct_answer=True)
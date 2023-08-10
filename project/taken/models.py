from django.db import models
from django.contrib.auth.models import User

from content.models import answer
from content.models import question
from content.models import exam

from content.models import course
from content.models import subject
from content.models import topics

# Create your models here.

class AttemptExam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    max_score = models.IntegerField()
    my_score = models.FloatField()

    original_exam = models.ForeignKey(exam.Exam, on_delete=models.CASCADE, null=True)
    course_exam = models.ForeignKey(course.Course, on_delete=models.CASCADE, null=True)
    subject_exam = models.ForeignKey(subject.Subject, on_delete=models.CASCADE, null=True)
    topic_exam = models.ForeignKey(topics.Topics, on_delete=models.CASCADE, null=True)
    
    attempted_at = models.DateTimeField(auto_now_add=True)

    def score_percentage(self):
        return (self.my_score / self.attemptquestion_set.count())*100

    class Meta:
        ordering = ['pk']

class AttemptQuestion(models.Model):
    attempt_exam = models.ForeignKey(AttemptExam, on_delete=models.CASCADE, null=True)
    original_question = models.ForeignKey(question.Question, on_delete=models.CASCADE, null=True)
    points = models.FloatField(default=0, null=True, blank=True)

class AttemptAnswer(models.Model):
    my_answer = models.BooleanField(default=False)
    attempt_question = models.ForeignKey(AttemptQuestion, on_delete=models.CASCADE, null=True)
    original_answer = models.ForeignKey(answer.Answer, on_delete=models.CASCADE, null=True)
    correct = models.BooleanField(default=False)

    def is_correct(self):
        if self.correct:
            return '<i class="fas fa-check text-success"></i>'
        else:
            return '<i class="fas fa-times text-danger"></i>'

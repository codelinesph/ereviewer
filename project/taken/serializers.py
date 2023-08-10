from .models import *
from rest_framework import serializers

from content.models import answer
from content.models import question
from content.models import exam

from content.models import course
from content.models import subject

class AttemptAnswerSerializer(serializers.ModelSerializer):
    attempt_question = serializers.PrimaryKeyRelatedField(queryset=AttemptQuestion.objects.all())
    original_answer = serializers.PrimaryKeyRelatedField(queryset=answer.Answer.objects.all())
    my_answer = serializers.BooleanField(default=False)
    correct = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = AttemptAnswer
        fields = ('id','my_answer','attempt_question','original_answer','correct',)

class AttemptQuestionSerializer(serializers.ModelSerializer):
    attempt_exam = serializers.PrimaryKeyRelatedField(queryset=AttemptExam.objects.all())
    original_question = serializers.PrimaryKeyRelatedField(queryset=question.Question.objects.all())
    attempt_answers = AttemptAnswerSerializer(source='attemptanswer_set', many=True, allow_null=True, read_only=True)
    points = serializers.FloatField()
    class Meta:
        model = AttemptQuestion
        fields = ('id','attempt_exam','original_question','attempt_answers','points',)

class AttemptExamSerializer(serializers.ModelSerializer):
    original_exam = serializers.PrimaryKeyRelatedField(queryset=exam.Exam.objects.all(),required=False)
    course_exam = serializers.PrimaryKeyRelatedField(queryset=course.Course.objects.all(),required=False)
    subject_exam = serializers.PrimaryKeyRelatedField(queryset=subject.Subject.objects.all(),required=False)
    topic_exam = serializers.PrimaryKeyRelatedField(queryset=topics.Topics.objects.all(),required=False)
    
    max_score = serializers.IntegerField()
    my_score = serializers.FloatField()
    attempt_questions = AttemptQuestionSerializer(source='attemptquestion_set', many=True, read_only=True)
    class Meta:
        model = AttemptExam
        fields = ('id','owner','max_score','my_score','attempt_questions','original_exam','course_exam','subject_exam','topic_exam',)



#
# SPECIALIZED FOR READ-ONLY
#
class AttemptQuestionSerializerROnly(serializers.ModelSerializer):
    attempt_answers = AttemptAnswerSerializer(source='attemptanswer_set', many=True, allow_null=True, read_only=True)
    class Meta:
        model = AttemptQuestion
        fields = ('id','attempt_exam','original_question','attempt_answers',)

class AttemptExamSerializerROnly(serializers.ModelSerializer):
    attempt_questions = AttemptQuestionSerializerROnly(source='attemptquestion_set', many=True, read_only=True)
    class Meta:
        model = AttemptExam
        fields = ('id','owner','max_score','my_score','original_exam','attempt_questions',)
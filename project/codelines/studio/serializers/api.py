from rest_framework import serializers

from content.models.exam import Exam
from content.models.question import Question
from content.models.answer import Answer

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all(),required=False)
    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source="answer_set",many=True,read_only=True)
    exam = serializers.PrimaryKeyRelatedField(queryset = Exam.objects.all())
    class Meta:
        model = Question
        fields = '__all__'
class CompleteExamDataSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(source='question_set',many=True, read_only=True)
    class Meta:
        model = Exam
        fields = '__all__'

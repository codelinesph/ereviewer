from rest_framework import serializers

from content.models import answer, course, exam, question, subject, topics

class answerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer.Answer
        fields = ('id','answer','question',)

class correctAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer.Answer
        fields = ('id','is_correct_answer','reasons','links',)

class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = course.Course
        fields = '__all__'
    
class examSerializer(serializers.ModelSerializer):
    class Meta:
        model = exam.Exam
        fields = '__all__'

class questionSerializer(serializers.ModelSerializer):
    choices = answerSerializer(source='answer_set', many=True, read_only=True)
    expected_answers = serializers.SerializerMethodField()
    class Meta:
        model = question.Question
        fields = ('id','question','choices','expected_answers',)

    def get_expected_answers(self, obj):
        return obj.answer_set.exclude(is_correct_answer=False).count()


class answeredQuestionsSerializer(serializers.ModelSerializer):
    choices = correctAnswersSerializer(source='answer_set', many=True, read_only=True)
    expected_answers = serializers.SerializerMethodField()
    class Meta:
        model = question.Question
        fields = ('id','choices','expected_answers',)

    def get_expected_answers(self, obj):
        return obj.answer_set.exclude(is_correct_answer=False).count()

class subjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = subject.Subject
        fields = '__all__'

class topicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = topics.Topics
        fields = '__all__'
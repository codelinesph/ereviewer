from django.shortcuts import get_object_or_404

from rest_framework import status,viewsets
from rest_framework.response import Response

from content.models.exam import Exam
from content.models.question import Question
from content.models.answer import Answer

from codelines.studio.serializers import api as ApiSerializers

class ExamViewset(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ApiSerializers.ExamSerializer

class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = ApiSerializers.QuestionSerializer

    def create(self, request):
        rq = request.data
        serializer = ApiSerializers.QuestionSerializer(data=rq)
        if serializer.is_valid():
            question = serializer.save()
            for answer in request.data['answers']:
                answerserializer = ApiSerializers.AnswerSerializer(data=answer)
                if answerserializer.is_valid():
                    Answer.objects.create(question=question,**answerserializer.data)
                else:
                    return Response(answerserializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk=None):
        rq = request.data
        serializer = ApiSerializers.QuestionSerializer(data=rq)
        if serializer.is_valid():
            question = Question.objects.filter(pk=pk)
            instance = question.get(pk=pk)
            question.update(**serializer.data)
            for answer in request.data['answers']:
                answerserializer = ApiSerializers.AnswerSerializer(data=answer)
                if answerserializer.is_valid():
                    if('id' in answer):
                        answer = Answer.objects.filter(pk=answer['id'])
                        answer.update(**answerserializer.data)
                    else:
                        Answer.objects.create(question=instance,**answerserializer.data)
                else:
                    return Response(answerserializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(ApiSerializers.QuestionSerializer(instance).data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = ApiSerializers.AnswerSerializer

class CompleteExamDataViewset(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ApiSerializers.CompleteExamDataSerializer
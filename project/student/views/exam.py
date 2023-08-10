import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views import View

from django.conf import settings

from rest_framework.parsers import JSONParser


from student import serializers as contentSerializers
from content import models as contentModels 
from users import models as userModels

from taken import serializers as takenSerializers
from users.models import *

from content.methods import takeexam

from django.db.models import Q


class examView(LoginRequiredMixin, View):
    login_url = 'main_home'
    http_method_names = ['options','post','get']
    def get(self,request,id,action=None):
        if action is None:
            qset = contentModels.exam.Exam.objects.all()
            info = get_object_or_404(qset, id=id)
            subscriptions = userModels.UserSubscriptions.objects.filter(
                owner=request.user.id, 
                subscription_date__lte=datetime.now(),
                subscription_expiration_date__gte=datetime.now(),
            )
            course_info = subscriptions.get(course_id=info.topic.subject.course.id)
            data = {
                "info":info,
                "subscriptions":subscriptions,
                "course_info":course_info,
                "mode":"exam",
            }
            return render(request, 'acad/takeexam.html', data)
        elif(action == 'getquestions'):
            qset = contentModels.question.Question.objects.filter(exam_id=id).order_by('?')
            serializer = contentSerializers.questionSerializer(qset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            raise Http404()
    def post(self, request, id, action=None):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        if action is not None:
            if(action=='submitexam'):
                ids = []
                for x in data:
                    ids.append(x["id"])

                qset = contentModels.question.Question.objects.filter(pk__in=ids)
                serializer = contentSerializers.answeredQuestionsSerializer(qset, many=True)
                correct_answers = serializer.data

                #
                # BEGINS DATA INGESTION
                #

                # constructs ingest parameters
                # score evaluation routine
                # @refactor: this block of code is subject for refactoring for upcoming versions

                evaulated_data = takeexam.checkAnswers(data,correct_answers)
                data = evaulated_data.get('data')

                attempt_exam_ingest_data = {
                    "owner": request.user.id,
                    "max_score": 0,
                    "my_score": evaulated_data.get('points_earned'),
                    "original_exam": id,
                }

                # serialize exam ingest data
                attempt_exam_ingest_serializer = takenSerializers.AttemptExamSerializer(data=attempt_exam_ingest_data)
                counter = 0
                # checks if exam ingest is valid
                if (attempt_exam_ingest_serializer.is_valid()):

                    # save exam ingest data
                    attempt_exam = attempt_exam_ingest_serializer.save()

                    # now, iterate though the questions
                    for ingest_question in data:
                        # constructs question ingest parameters
                        attempt_question_ingest_data = {
                            "attempt_exam": attempt_exam.id,
                            "original_question": ingest_question['id'],
                            "points": ingest_question['points']
                        }
                        # then passes it to its serializer
                        attempt_question_ingest_serializer = takenSerializers.AttemptQuestionSerializer(data=attempt_question_ingest_data)
                        # is it valid?
                        if(attempt_question_ingest_serializer.is_valid()):
                            # if yes, then save it
                            saved_question = attempt_question_ingest_serializer.save()

                            # now we are at choices
                            for choice in ingest_question.get('choices'):
                                # again, construct ingest parameters
                                attempt_answer_ingest_data = {
                                    'attempt_question':saved_question.id,
                                    'original_answer':choice.get('id'),
                                    'my_answer':choice.get('my_answer'),
                                    'correct':choice.get('correct'),
                                }
                                # then pass it to the serializer
                                attempt_answer_ingest_serializer = takenSerializers.AttemptAnswerSerializer(data = attempt_answer_ingest_data)
                                # and finally saves it to the database if valid
                                counter+=1
                                if(attempt_answer_ingest_serializer.is_valid()):
                                    attempt_answer_ingest_serializer.save()
                          

                return JsonResponse(correct_answers, safe=False)
            else:
                raise Http404()
        else:
            raise Http404()

class courseExamView(LoginRequiredMixin, View):
    login_url = 'main_home'
    http_method_names = ['options','post','get']
    def get(self,request,id,action=None):
        subscriptions = userModels.UserSubscriptions.objects.filter(
            owner=request.user.id, 
            subscription_date__lte=datetime.now(),
            subscription_expiration_date__gte=datetime.now(),
        )
        course_info = get_object_or_404(subscriptions, course_id=id)
        info = course_info.course
        if action is None:
            data = {
                "info":info,
                "subscriptions":subscriptions,
                "course_info":course_info,
                "mode":"course",
            }
            return render(request, 'acad/takeexam.html', data)
        elif(action == 'getquestions'):
            qset = contentModels.question.Question.objects.filter(exam__topic__subject__course_id=id).order_by('?')[:info.assessment_limit]
            serializer = contentSerializers.questionSerializer(qset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            raise Http404()
    def post(self, request, id, action=None):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        if action is not None:
            if(action=='submitexam'):
                ids = []
                for x in data:
                    ids.append(x["id"])

                qset = contentModels.question.Question.objects.filter(pk__in=ids)
                serializer = contentSerializers.answeredQuestionsSerializer(qset, many=True)
                correct_answers = serializer.data

                #
                # BEGINS DATA INGESTION
                #

                # constructs ingest parameters
                # score evaluation routine
                # @refactor: this block of code is subject for refactoring for upcoming versions

                evaulated_data = takeexam.checkAnswers(data,correct_answers)
                data = evaulated_data.get('data')

                attempt_exam_ingest_data = {
                    "owner": request.user.id,
                    "max_score": 0,
                    "my_score": evaulated_data.get('points_earned'),
                    "course_exam": id,
                }

                # serialize exam ingest data
                attempt_exam_ingest_serializer = takenSerializers.AttemptExamSerializer(data=attempt_exam_ingest_data)
                counter = 0
                # checks if exam ingest is valid
                if (attempt_exam_ingest_serializer.is_valid()):

                    # save exam ingest data
                    attempt_exam = attempt_exam_ingest_serializer.save()

                    # now, iterate though the questions
                    for ingest_question in data:
                        # constructs question ingest parameters
                        attempt_question_ingest_data = {
                            "attempt_exam": attempt_exam.id,
                            "original_question": ingest_question['id'],
                            "points": ingest_question['points']
                        }
                        # then passes it to its serializer
                        attempt_question_ingest_serializer = takenSerializers.AttemptQuestionSerializer(data=attempt_question_ingest_data)
                        # is it valid?
                        if(attempt_question_ingest_serializer.is_valid()):
                            # if yes, then save it
                            saved_question = attempt_question_ingest_serializer.save()

                            # now we are at choices
                            for choice in ingest_question.get('choices'):
                                # again, construct ingest parameters
                                attempt_answer_ingest_data = {
                                    'attempt_question':saved_question.id,
                                    'original_answer':choice.get('id'),
                                    'my_answer':choice.get('my_answer'),
                                    'correct':choice.get('correct'),
                                }
                                # then pass it to the serializer
                                attempt_answer_ingest_serializer = takenSerializers.AttemptAnswerSerializer(data = attempt_answer_ingest_data)
                                # and finally saves it to the database if valid
                                counter+=1
                                if(attempt_answer_ingest_serializer.is_valid()):
                                    attempt_answer_ingest_serializer.save()
                          

                return JsonResponse(correct_answers, safe=False)
            else:
                raise Http404()
        else:
            raise Http404()

class subjectExamView(LoginRequiredMixin, View):
    login_url = 'main_home'
    http_method_names = ['options','post','get']
    def get(self,request,id,action=None):

        qset = contentModels.subject.Subject.objects.all()
        info = get_object_or_404(qset, id=id)

        subscriptions = userModels.UserSubscriptions.objects.filter(
            owner=request.user.id, 
            subscription_date__lte=datetime.now(),
            subscription_expiration_date__gte=datetime.now(),
        )
        course_info = get_object_or_404(subscriptions, course_id=info.course.id)

        if action is None:
            data = {
                "info":info,
                "subscriptions":subscriptions,
                "course_info":course_info,
                "mode":"subject",
            }
            return render(request, 'acad/takeexam.html', data)
        elif(action == 'getquestions'):
            qset = contentModels.question.Question.objects.filter(exam__topic__subject_id=id).order_by('?')[:info.assessment_limit]
            serializer = contentSerializers.questionSerializer(qset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            raise Http404()
    def post(self, request, id, action=None):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        if action is not None:
            if(action=='submitexam'):
                ids = []
                for x in data:
                    ids.append(x["id"])

                qset = contentModels.question.Question.objects.filter(pk__in=ids)
                serializer = contentSerializers.answeredQuestionsSerializer(qset, many=True)
                correct_answers = serializer.data

                #
                # BEGINS DATA INGESTION
                #

                # constructs ingest parameters
                # score evaluation routine
                # @refactor: this block of code is subject for refactoring for upcoming versions

                evaulated_data = takeexam.checkAnswers(data,correct_answers)
                data = evaulated_data.get('data')

                attempt_exam_ingest_data = {
                    "owner": request.user.id,
                    "max_score": 0,
                    "my_score": evaulated_data.get('points_earned'),
                    "subject_exam": id,
                }

                # serialize exam ingest data
                attempt_exam_ingest_serializer = takenSerializers.AttemptExamSerializer(data=attempt_exam_ingest_data)
                counter = 0
                # checks if exam ingest is valid
                if (attempt_exam_ingest_serializer.is_valid()):

                    # save exam ingest data
                    attempt_exam = attempt_exam_ingest_serializer.save()

                    # now, iterate though the questions
                    for ingest_question in data:
                        # constructs question ingest parameters
                        attempt_question_ingest_data = {
                            "attempt_exam": attempt_exam.id,
                            "original_question": ingest_question['id'],
                            "points": ingest_question['points']
                        }
                        # then passes it to its serializer
                        attempt_question_ingest_serializer = takenSerializers.AttemptQuestionSerializer(data=attempt_question_ingest_data)
                        # is it valid?
                        if(attempt_question_ingest_serializer.is_valid()):
                            # if yes, then save it
                            saved_question = attempt_question_ingest_serializer.save()

                            # now we are at choices
                            for choice in ingest_question.get('choices'):
                                # again, construct ingest parameters
                                attempt_answer_ingest_data = {
                                    'attempt_question':saved_question.id,
                                    'original_answer':choice.get('id'),
                                    'my_answer':choice.get('my_answer'),
                                    'correct':choice.get('correct'),
                                }
                                # then pass it to the serializer
                                attempt_answer_ingest_serializer = takenSerializers.AttemptAnswerSerializer(data = attempt_answer_ingest_data)
                                # and finally saves it to the database if valid
                                counter+=1
                                if(attempt_answer_ingest_serializer.is_valid()):
                                    attempt_answer_ingest_serializer.save()
                          

                return JsonResponse(correct_answers, safe=False)
            else:
                raise Http404()
        else:
            raise Http404()
from django.forms import (
    TextInput, Textarea
)
from django.utils.translation import gettext, gettext_lazy as _

from django import forms

from content.models.course import Course
from content.models.subject import Subject
from content.models.topics import Topics
from content.models.lesson import Lesson
from content.models.exam import Exam
from content.models.question import Question

class CourseForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Course Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )
    description = forms.CharField(
        label=_("Course Description"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":5,
            "style":"resize:none"
        }),
    )
    content = forms.CharField(
        label=_("Course Content"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":5,
            "style":"resize:none"
        }),
    )
    banner = forms.FileField(required=False)
    logo = forms.FileField(required=False)
    # required=False
    arrangement = forms.IntegerField(
        label=("Custom Arrangement(default is by id)"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    assessment_limit = forms.IntegerField(
        label=("General Assessment Query Limit"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    in_public = forms.BooleanField(
        label=("This course is publicly available"),
        required=False,
    )
    class Meta:
        fields = ['name','in_public','description','content','banner','logo','arrangement','assessment_limit',]
        model = Course

class SubjectForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Subject Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )
    course = forms.ModelChoiceField(
        label=_("Subject Course"),
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    description = forms.CharField(
        label=("Subject Description"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":5,
            "style":"resize:none"
        }),
    )
    arrangement = forms.IntegerField(
        label=("Custom Arrangement(default is by id)"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    assessment_limit = forms.IntegerField(
        label=("General Assessment Query Limit"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    banner = forms.FileField(required=False)
    logo = forms.FileField(required=False)
    class Meta:
        fields = ['course','name','description','banner','logo','arrangement','assessment_limit',]
        model = Subject

class TopicsForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Topic Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )
    subject = forms.ModelChoiceField(
        label=_("This Topic Belongs to Subject:"),
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    arrangement = forms.IntegerField(
        label=("Custom Arrangement(default is by id)"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    description = forms.CharField(
        label=("Description"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":1,
            "style":"resize:none"
        }),
    )
    content = forms.CharField(
        label=("Content"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":10,
            "style":"resize:none"
        }),
    )
    assessment_limit = forms.IntegerField(
        label=("General Assessment Query Limit"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    class Meta:
        fields = ['subject','name','arrangement','description','content','premium_content','assessment_limit',]
        model = Topics

class LessonForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Lesson Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )
    topic = forms.ModelChoiceField(
        label=_("This Lesson Belongs to Topic:"),
        queryset=Topics.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    arrangement = forms.IntegerField(
        label=("Custom Arrangement(default is by id)"),
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control rounded-0",
        })
    )
    description = forms.CharField(
        label=("Short Description"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":1,
            "style":"resize:none"
        }),
    )
    content = forms.CharField(
        label=("Content"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":10,
            "style":"resize:none"
        }),
    )
    class Meta:
        fields = ['topic','name','arrangement','description','content','premium_content',]
        model = Lesson


class ExamForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Exam Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )
    description = forms.CharField(
        label=("Short Description"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":1,
            "style":"resize:none"
        }),
    )
    topic = forms.ModelChoiceField(
        label=_("This Lesson Belongs to Topic:"),
        queryset=Topics.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    class Meta:
        fields = ['name','description','topic','premium_content']
        model = Exam

class QuestionForm(forms.ModelForm):
    question = forms.CharField(
        label=("Question"),
        strip=False,
        widget=forms.Textarea(attrs={
            "class":"form-control rounded-0",
            "rows":1,
            "style":"resize:none"
        }),
    )
    class Meta:
        fields = ['question','premium_content']
        model = Question
from django import forms
from .models import Poll, Answer
from django.utils.translation import ugettext_lazy as _


class StartPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['topic', 'answers_amount']
        labels = {
            'topic': _("Topic or question"),
            'answers_amount': _("Amount of answers")
        }


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['option']

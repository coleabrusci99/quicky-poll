import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from textwrap import wrap
from django.shortcuts import render, redirect
from django.conf import settings
from django.templatetags.static import static
from .forms import StartPollForm, AnswerOptionForm
from .models import Poll, Answer

app_name = 'PollApp'

# Create your views here.


def index(request):
    form = StartPollForm()
    context = {'form': form, 'answer_prompts': []}

    if request.method == 'POST':
        form = StartPollForm(request.POST)

        if form.is_valid():
            # Checks if the prompts for defining answers is on screen
            if 'option' not in request.POST:
                form.fields['topic'].widget.attrs['readonly'] = True
                form.fields['answers_amount'].widget.attrs['readonly'] = True
                context['form'] = form
                # Adds prompts to screen if they aren't there and refreshes the page
                for i in range(form.cleaned_data['answers_amount']):
                    option_form = AnswerOptionForm()
                    option_form.fields['option'].label = "Option {}:".format(
                        i+1)
                    context['answer_prompts'].append(option_form)
            else:
                # Generates a database entry for the poll
                top = form.cleaned_data['topic']
                amount = form.cleaned_data['answers_amount']
                answers = request.POST.getlist('option')

                poll = Poll.objects.get_or_create(
                    topic=top, answers_amount=amount)[0]
                for i in range(len(answers)):
                    answer = Answer.objects.get_or_create(
                        poll=poll, option=answers[i])[0]
                return redirect(voting_page, url=poll.url)

    return render(request, 'PollApp/index.html', context)


def voting_page(request, url):
    context = {}
    poll_info = Poll.objects.filter(url=url)[0]
    poll_answers = [ans for ans in Answer.objects.filter(poll=poll_info)]
    context['poll_info'] = poll_info
    context['poll_answers'] = poll_answers

    if request.method == 'POST':
        for ans in poll_answers:
            if request.POST['options'] == ans.option:
                ans.tally += 1
                ans.save()
                return redirect(results_page, url)

    return render(request, 'PollApp/poll.html', context)


def results_page(request, url):
    context = {}
    poll_info = Poll.objects.filter(url=url)[0]
    poll_answers = [ans for ans in Answer.objects.filter(poll=poll_info)]
    context['poll_title'] = poll_info.topic

    labels = []
    values = []
    for ans in poll_answers:
        if ans.tally > 0:
            labels.append('\n'.join(wrap(ans.option, 20)))
            values.append(ans.tally)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')
    img_name = '{}.png'.format(poll_info.url)
    
    plt.savefig('media/{}'.format(img_name), transparent=True, dpi=150)
    
    img_path = os.path.join(settings.MEDIA_ROOT, img_name)
    
    poll_info.chart = img_path
    poll_info.save()

    context['poll_chart'] = poll_info.chart

    return render(request, 'PollApp/results.html', context=context)

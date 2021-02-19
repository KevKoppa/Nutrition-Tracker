from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Choice

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect


# generic ListView requires the list and template_name as well as the function for making the list
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    # shortcut for above is get_object_or_404(model_name, attribute for get function)
    return render(request, 'polls/detail.html', {'question': question})
    '''
    model = Question
    template_name = 'polls/detail.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except KeyError:
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class QuestionCreate(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['question_text']


class ChoiceCreate(LoginRequiredMixin, generic.CreateView):
    model = Choice
    fields = ['question', 'choice_text']


class QuestionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Question
    fields = ['question_text']


class ChoiceUpdate(LoginRequiredMixin, generic.CreateView):
    model = Choice
    fields = ['question', 'choice_text']

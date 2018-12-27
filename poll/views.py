from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404, HttpResponse
# Create your views here.
from .decoretors import role_required, admin_only
from .models import *


from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.db.models import Q

from .forms import PollForm, ChoiceForm
from .models import *


@login_required(login_url="/login/")
def index(request):
    context ={}
    questions = Question.objects.all()
    context['title'] = 'polls'
    context['questions'] = questions
    return render(request, 'polls/index.html', context)

@login_required(login_url="/login/")
def details(request, id=None):
    context ={}
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404
    context['title'] = 'polls'
    context['question'] = question
    return render(request,'polls/details.html', context)

@login_required(login_url="/login/")
def poll(request, id= None ):
    if request.method == "GET":
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404
        context = {}
        context['question'] = question
        return render(request, 'polls/poll.html', context)

    if request.method=="POST":
        user_id = 1
        data = request.POST
        ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
        if ret:
            return HttpResponse("Your Vote is Done Submitted Successfully...!!")
        else:
            return HttpResponse("Your Vote is not Submitted Successfully...!!")


class PollView(View):
    decorators = [login_required, role_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/list/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question)
        question.delete()

        return redirect('polls_list')














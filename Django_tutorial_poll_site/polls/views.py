from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
from .forms import NewQuestionForm, ChoiceFormSet


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 5

    def get_queryset(self):
        """Return the last five published questions
        (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # セッションからエラーメッセージを取得し、それをコンテキストに追加してからセッションをクリア
        error_message = self.request.session.pop('error_message', None)
        if error_message:
            context['error_message'] = error_message
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests on the question detail page for voting on a choice.
        """
        question = self.get_object()
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form with an error message.
            context = {"question": question, "error_message": "You didn't select a choice"}
            return render(request, self.template_name, context)
        else:
            selected_choice.votes = F('votes') + 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

def add_question(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            # まずQuestionを保存します。
            new_question = form.save()
            # Questionに紐づくChoiceのフォームセットを処理します。
            formset = ChoiceFormSet(request.POST, instance=new_question)
            if formset.is_valid():
                formset.save()
                return redirect('polls:index')
    else:
        form = NewQuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'polls/add_question.html', {'form': form, 'formset': formset})

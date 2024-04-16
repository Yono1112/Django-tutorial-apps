from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice


def index(request):
    # django.shortcuts.render関数を使用して
    # 内部的にテンプレートのロード、コンテキストのレンダリング、およびレンダリングされた内容を
    # HttpResponseオブジェクトに包んで返す一連の処理を自動的に行います
    latest_question_list = Question.objects.order_by("-pub_date")[
        :5
    ]  # マイナス記号(-)が降順を示す
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

    # 別の書き方: テンプレートのロードとレンダリング、HTTP応答の作成が明示的に分けて書かれています。
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    # context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context, request))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # detail.htmlファイルのinput属性で送信しているvalue属性(今回はChoiceのid)を受け取る
        # request.POSTにキーを指定すると、送信したデータにアクセスできる
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {"question": question, "error_message": "You didin't select a choice"}
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # POST データが成功した後は常に HttpResponseRedirect を返す必要がある
        # reverse()　はビュー関数中での URL のハードコードを防ぐ
        # 引数には制御を渡したいビューの名前と、そのビューに与える URL パターンの位置引数を与える
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

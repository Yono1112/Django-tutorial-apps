from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    # django.shortcuts.render関数を使用して
    # 内部的にテンプレートのロード、コンテキストのレンダリング、およびレンダリングされた内容を
    # HttpResponseオブジェクトに包んで返す一連の処理を自動的に行います
    latest_question_list = Question.objects.order_by("-pub_date")[:5] #マイナス記号(-)が降順を示す
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

    # 別の書き方: テンプレートのロードとレンダリング、HTTP応答の作成が明示的に分けて書かれています。
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    # context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

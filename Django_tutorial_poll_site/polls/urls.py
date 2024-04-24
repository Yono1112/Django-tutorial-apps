from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/add_question/
    path("add_question/", views.add_question, name="add_question"),
]

# as_view()関数は、クラス定義をビュー関数(ウェブアプリケーションがクライアントからのリクエストを受け取った際に呼び出される関数)に変換する

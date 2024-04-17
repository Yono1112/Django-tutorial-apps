import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # __str__ は Django の管理サイトでオブジェクトを表示するときや
    #   テンプレートでオブジェクトを表示するときに挿入される値として使われます。
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Determine if the question was published within the last 24 hours"""
        return (
            timezone.now()
            >= self.pub_date
            >= timezone.now() - datetime.timedelta(days=1)
        )


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

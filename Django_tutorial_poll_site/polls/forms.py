from django.forms import ModelForm, inlineformset_factory
from .models import Question, Choice


class NewQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]


ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), extra=3, can_delete=False)
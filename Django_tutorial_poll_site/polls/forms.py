from django.forms import ModelForm, inlineformset_factory, TextInput
from .models import Question, Choice


class NewQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]
        widgets = {
            'question_text': TextInput(attrs={'autofocus': 'autofocus'}),
        }


ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), extra=3, can_delete=False)
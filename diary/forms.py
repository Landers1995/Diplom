from django import forms
from users.forms import StyleFormMixin
from diary.models import Diary


class DiaryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Diary
        exclude = ('user',)

from django import forms
from users.forms import StyleFormMixin
from diary.models import Diary


class DiaryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Diary
        exclude = ('user',)


class DiarySearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))


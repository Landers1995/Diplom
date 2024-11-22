from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.management import call_command
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from diary.forms import DiaryForm, DiaryDateForm, DiarySearchForm
from diary.models import Diary
import datetime

class DiaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    permission_required = 'diary.add_diary'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save()
        user = self.request.user
        diary.user = user
        diary.save()
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    permission_required = 'diary.change_diary'
    success_url = reverse_lazy('diary:diary_list')


class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    #permission_required = 'diary.view_diary'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = Diary

    pk_url_kwarg = 'create_date'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

    # def get_object(self, queryset=None):
    #     queryset = self.get_queryset()
    #     date = self.kwargs.get('create_date')
    #     create_date = datetime.datetime.strftime(date, '%Y.%m.%d')
    #     diary = queryset.filter(create_date=create_date)
    #     return diary


class DiaryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Diary
    permission_required = 'diary.delete_diary'
    success_url = reverse_lazy('diary:diary_list')


# def diary_view(request):
#     form = DiaryDateForm()
#     if request.method == "POST":
#         form = DiaryDateForm(request.POST)
#         if form.is_valid():
#             selected_date = form.cleaned_data['create_date']
#             # Здесь можно обработать выбранную дату (например, сохранить, вывести и т.д.)
#             return render(request, 'diary/diary_detail.html', {'selected_date': selected_date})
#
#     return render(request, 'diary/diary_list.html', {'form': form})



def diary_list(request):
    form = DiarySearchForm()
    diaries = Diary.objects.all()

    if 'query' in request.GET:
        form = DiarySearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            diaries = diaries.filter(title__icontains=query) | diaries.filter(body__icontains=query)

    return render(request, 'dairy_list.html', {'form': form, 'diaries': diaries})

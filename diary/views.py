from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.management import call_command
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from diary.forms import DiaryForm, DiarySearchForm
from diary.models import Diary
import datetime
from django.db.utils import IntegrityError


class DiaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    permission_required = 'diary.add_diary'
    success_url = reverse_lazy('diary:diary_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        date = super().get_context_data(object_list=object_list, **kwargs)
        date['date_list'] = Diary.objects.values_list('create_date').distinct()
        return date

    def form_valid(self, form):
        # diary = form.save()
        # user = self.request.user
        # diary.user = user
        # diary.save()
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, f'Запись уже существует')
            return self.form_invalid(form)



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

    def get_context_data(self, *, object_list=None, **kwargs):
        date = super().get_context_data(object_list=object_list, **kwargs)
        date['date_list'] = Diary.objects.filter(user=self.request.user).values_list('create_date', flat=True).distinct()
        return date


class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = Diary

    slug_url_kwarg = 'create_date'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        date = super().get_context_data(object_list=object_list, **kwargs)
        date['date_list'] = sorted(Diary.objects.filter(user=self.request.user).values_list('create_date', flat=True).distinct())
        return date

    def get_slug_field(self):
        return 'create_date'

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

    def get_context_data(self, *, object_list=None, **kwargs):
        date = super().get_context_data(object_list=object_list, **kwargs)
        date['date_list'] = Diary.objects.values_list('create_date').distinct()
        return date


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

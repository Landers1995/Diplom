from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from diary.forms import DiaryForm, DiarySearchForm
from diary.models import Diary
import datetime
from django.db.utils import IntegrityError
from django.db.models import Q


class DairyListMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        ct = super().get_context_data(object_list=object_list, **kwargs)
        qs = Diary.objects.filter(user=self.request.user)
        ct['date_list'] = qs.values_list('create_date', flat=True).distinct()
        return ct


class DiaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, DairyListMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    permission_required = 'diary.add_diary'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, f'Запись уже существует')
            return self.form_invalid(form)


class DiaryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, DairyListMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    permission_required = 'diary.change_diary'
    success_url = reverse_lazy('diary:diary_list')


class DiaryListView(LoginRequiredMixin, DairyListMixin, ListView):
    model = Diary
    paginate_by = 2

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryDetailView(LoginRequiredMixin, DairyListMixin, DetailView):
    model = Diary

    slug_url_kwarg = 'create_date'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

    def get_slug_field(self):
        return 'create_date'


class DiaryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DairyListMixin, DeleteView):
    model = Diary
    permission_required = 'diary.delete_diary'
    success_url = reverse_lazy('diary:diary_list')


def diary_search(request):
    form = DiarySearchForm()
    diaries = []
    if request.method == 'GET':
        form = DiarySearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            diaries = Diary.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    return render(request, 'diary/search.html', {'form': form, 'object_list': diaries})


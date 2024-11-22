from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from diary.apps import DiaryConfig
from diary.views import DiaryListView, DiaryDetailView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView, diary_list
#diary_view

app_name = DiaryConfig.name

urlpatterns = [
    path("", DiaryListView.as_view(), name="diary_list"),
    path("diary/<str:create_date>/", DiaryDetailView.as_view(), name="diary_detail"),
    path("diary_create/", DiaryCreateView.as_view(), name="diary_create"),
    path("diary_edit/<int:pk>/", DiaryUpdateView.as_view(), name="diary_edit"),
    path("diary_delete/<int:pk>/", DiaryDeleteView.as_view(), name="diary_delete"),
    #path('diary/', diary_view, name='diary_view'),
    path('', diary_list, name='diary_list'),

 ]

# path("diary/<str:create_date>/", DiaryDetailView.as_view(), name="diary_detail")

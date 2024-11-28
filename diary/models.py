from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Diary(models.Model):

    title = models.CharField(max_length=50, verbose_name='Заголовок', help_text='Введите заголовок')
    body = models.TextField(verbose_name='Текст', help_text='Введите текст')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи")

    class Meta:
        verbose_name = "Запись в дневнике"
        verbose_name_plural = "Записи в дневнике"
        unique_together = ["user", "create_date"]
        ordering = ("create_date",)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.CharField(max_length=100, verbose_name='Автор')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']  # сначала новые
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    is_approved = models.BooleanField(default=True, verbose_name='Одобрен')

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.news.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
from django.db import models

from conf import settings

NULLABLE = {'blank': True, 'null': True}

class Blog(models.Model):

    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст поста')
    avatar = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='аватар')
    created = models.DateField(auto_now_add=True, verbose_name='дата создания')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
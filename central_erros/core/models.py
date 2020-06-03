from django.db import models
from django.core.validators import MinValueValidator


class ErrorLog(models.Model):
    source = models.CharField('origem', max_length=128)
    events = models.PositiveIntegerField('eventos', default=1, 
                                         validators=[MinValueValidator(1),])
    details = models.TextField('detalhes')
    description = models.CharField('descrição', max_length=256)
    raised_at = models.DateTimeField('data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'log de erro'
        verbose_name_plural = 'logs de erro'

    def __str__(self):
        return f'{description}, {source}, {raised_at}'

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class ErrorLog(models.Model):
    LOG_LEVELS = (
        ('CRITICAL', 'CRITICAL'),
        ('DEBUG', 'DEBUG'),
        ('ERROR', 'ERROR'),
        ('WARNING', 'WARNING'), 
        ('INFO', 'INFO'),
    )

    LOG_ENVIRONMENTS = (
        ('PRODUCTION', 'PRODUCTION'),
        ('HOMOLOGATION', 'HOMOLOGATION'),
        ('DEV', 'DEV'),
    )

    user = models.ForeignKey(
                User, on_delete=models.CASCADE, related_name='logs')
    description = models.CharField('Descrição', max_length=256)
    source = models.GenericIPAddressField('Origem')
    details = models.TextField('Detalhes')
    events = models.PositiveIntegerField(
                'Eventos', default=1, validators=[MinValueValidator(1)])
    date = models.DateTimeField('Data')
    level = models.CharField('Level', max_length=16, choices=LOG_LEVELS)
    env = models.CharField('Ambiene', max_length=16, choices=LOG_ENVIRONMENTS)
    archived = models.BooleanField('Arquivado', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Error Log'
        ordering = ['-created_at']

    @property
    def owner(self):
        return self.user
    
    def archive(self):
        self.archived = True

    def __str__(self):
        return self.description

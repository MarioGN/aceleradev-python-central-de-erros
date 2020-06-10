from django.db import models
from django.core.validators import MinValueValidator


class ErrorLog(models.Model):
    LOG_LEVELS = (
        ('CRITICAL', 'CRITICAL'),
        ('DEBUG', 'DEBUG'),
        ('ERROR', 'ERROR'),
        ('WARNING', 'WARNING'), 
        ('INFO', 'INFO'),
    )

    LOG_ENVIRONMENTS = (
        ('PRODUÇÃO', 'PRODUÇÃO'),
        ('HOMOLOGAÇÃO', 'HOMOLOGAÇÃO'),
        ('DEV', 'DEV'),
    )

    description = models.CharField('Descrição', max_length=256)
    source = models.GenericIPAddressField('Origem')
    details = models.TextField('Detalhes')
    events = models.PositiveIntegerField(
                'Eventos', default=1, validators=[MinValueValidator(1)])
    date = models.DateTimeField('Data')
    level = models.CharField('Level', max_length=16, choices=LOG_LEVELS)
    env = models.CharField('Ambiene', max_length=16, choices=LOG_ENVIRONMENTS)
    arquivado = models.BooleanField('Arquivado', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def archive(self):
        self.arquivado = True

    class Meta:
        verbose_name = 'Error Log'

    def __str__(self):
        return self.description

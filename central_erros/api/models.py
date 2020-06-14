from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()

class ErrorLogModelManager(models.Manager):
    search_fields = ('level', 'description', 'source')
    ordering_fields = ('level', '-level', 'events', '-events')

    def filter_logs(self, query_params):
        queryset = ErrorLog.objects.all()

        env = query_params.get('env', None)
        ordering = query_params.get('ordering', None)
        search_field = query_params.get('field', None)
        search = query_params.get('search', None)

        if env is not None:
            queryset = queryset.filter(env__iexact=env)
        if ordering is not None and ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        if search_field is not None and search_field in self.search_fields and search is not None:
            field_query = {f'{search_field}__icontains': search}
            queryset = queryset.filter(**field_query)

        return queryset


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

    objects = ErrorLogModelManager()
    
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

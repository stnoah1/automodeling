from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField("생성일", auto_now_add=timezone.now)
    updated = models.DateTimeField("수정일", auto_now=timezone.now)


class UpdateParamsMixin(object):
    def update_params(self, params={}):
        self.__dict__.update(params)
        self.__class__.objects.filter(id=self.id).update(**params)

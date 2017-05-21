from django.contrib.postgres.fields import JSONField
from django.db import models

from automodeling.models import TimeStampedModel

CHOICES = {
    "classes": [
        (0, "아무거나"), (1, "적어봄")
    ]
}


class Project(TimeStampedModel):
    class Meta:
        verbose_name = "프로젝트"

    ip = models.GenericIPAddressField('IP주소', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)


class Convert(TimeStampedModel):
    class Meta:
        verbose_name = "3D 모델 변환"

    project = models.ForeignKey(Project, verbose_name='프로젝트')
    input_data = JSONField('인풋데이터')
    results = JSONField('결과데이터')

    def __str__(self):
        return '{0.id}: {0.project}번 프로젝트'.format(self)


class ModelNet(TimeStampedModel):
    class Meta:
        verbose_name = "ModelNet 데이터"

    modelnet_id = models.CharField('ModelNetID', max_length=30)
    class_info = models.PositiveSmallIntegerField("클래스", choices=CHOICES['classes'])

    def __str__(self):
        return '{0.modelnet_id} 모델: 클래스-{0.class_info}'.format(self)

from django.db import models
from .querysets import PatientQuerySet

class PatientManager(models.Manager):
    def get_queryset(self):
        return PatientQuerySet(self.model)



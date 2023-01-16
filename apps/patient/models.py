from uuid import uuid4
from django.db import models
from .managers import PatientManager
from simple_history.models import HistoricalRecords


class Patient(models.Model):

    """
    A "Patient" connects a user to a study.
    """

    class Status(models.IntegerChoices):
        NEW = 0, 'New'
        ENGAGED = 10, 'Engaged'
        CONSENTED = 20, 'Consented'
        COMPLETE = 30, 'Complete'

    class Cancelled(models.IntegerChoices):
        NOT_CANCELLED = 0, '-'
        NOT_ELIGIBLE = 10, 'Not Eligible'
        NOT_CONSENTED = 20, 'Not Consented'
        OPTED_OUT = 30, 'Opted out'
        NOT_CONTACTABLE = 40, 'Not contactable'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    study = models.ForeignKey('study.Study', on_delete=models.PROTECT)
    status = models.IntegerField(choices=Status.choices, default=Status.NEW)
    cancelled = models.IntegerField(choices=Cancelled.choices, default=Cancelled.NOT_CANCELLED)
    care_provider = models.ForeignKey('care_provider.CareProvider', on_delete=models.PROTECT)

    objects = PatientManager()
    records = HistoricalRecords()

    class Meta:
        constraints = (
                models.constraints.UniqueConstraint(
                fields=["study", "user"],
                name="unique_patient_per_study"
            ),
        )
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return str(self.id)


class PatientDocument(models.Model):
    """
    Records documents that have been sent to patients.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    file = models.FileField(upload_to='patient_documents/')

    class Meta:
        verbose_name = "Patient document"
        verbose_name_plural = "Patient documents"

    def __str__(self):
        return str(self.id)
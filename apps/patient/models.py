from uuid import uuid4
from django.db import models


class Patient(models.Model):

    """
    A "Patient" connects a user to a study.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    study = models.ForeignKey('study.Study', on_delete=models.PROTECT)
    status = models.IntegerField(choices=(
        (0, "New"),
        (10, "Engaged"),
        (20, "Consented"),
        (30, "Complete"),
    ), default=0)
    cancelled = models.IntegerField(choices=(
        (0, "-"),
        (10, "Not Eligible"),
        (20, "Not Consented"),
        (30, "Opted out"),
        (40, "Not contactable"),
    ), default=0)

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

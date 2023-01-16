from django.db import models
from .emails import PatientEnrolmentEmail

class PatientQuerySet(models.QuerySet):

    def _check_can_send_enrolment_emails(self):
        '''
        Patients may only be sent enrolment emails if they
        - are not 'cancelled', and
        - have a status of 'New'.
        '''
        from .models import Patient

        allowed_patient_ids = self.filter(
            cancelled=Patient.Cancelled.NOT_CANCELLED,
            status=Patient.Status.NEW
        ).values_list("id", flat=True)
        disallowed_patient_ids = self.exclude(id__in=allowed_patient_ids).values_list("id", flat=True)
        if disallowed_patient_ids:
            raise PermissionError(f'Cannot send enrolment emails to patients {list(disallowed_patient_ids)}')

    def send_enrolment_emails(self):
        self._check_can_send_enrolment_emails()
        for patient in self.select_related('user'):
            PatientEnrolmentEmail(patient).send()
        


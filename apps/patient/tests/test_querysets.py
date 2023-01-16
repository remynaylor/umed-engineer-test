from ..models import Patient
from libs.factories import PatientFactory
from django.test import TestCase


class TestPatientQuerySet(TestCase):
    def test__check_can_send_enrolment_emails_when_allowed(self):
        for _ in range(2):
            PatientFactory(
                status=Patient.Status.NEW,
                cancelled=Patient.Cancelled.NOT_CANCELLED
            )
        Patient.objects.all()._check_can_send_enrolment_emails()

    def test__can_send_enrolment_emails_errors_for_incorrect_status(self):
        PatientFactory(
            status=Patient.Status.ENGAGED,
            cancelled=Patient.Cancelled.NOT_CANCELLED
        )
        with self.assertRaises(PermissionError):
            Patient.objects.all()._check_can_send_enrolment_emails()
        
    def test__can_send_enrolment_emails_errors_for_cancelled_patient(self):
        PatientFactory(
            status=Patient.Status.ENGAGED,
            cancelled=Patient.Cancelled.NOT_CONSENTED
        )
        with self.assertRaises(PermissionError):
            Patient.objects.all()._check_can_send_enrolment_emails()
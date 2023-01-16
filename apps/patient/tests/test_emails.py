from ..emails import PatientEnrolmentEmail
from unittest.mock import patch, MagicMock
from ..querysets import PatientQuerySet
from ..models import Patient, PatientDocument
from libs.factories import PatientFactory
from django.test import TestCase

class TestPatientEnrolmentEmail(TestCase):
    def test_send(self):
        patient = PatientFactory(
            status=Patient.Status.NEW,
            cancelled=Patient.Cancelled.NOT_CANCELLED
        )
        patient_enrolment_email = PatientEnrolmentEmail(patient)
        mock_send_mail = MagicMock()
        mock_send_mail.return_value = 1

        with patch('apps.patient.emails.send_mail', mock_send_mail):
            patient_enrolment_email.send()

        # As the email was sucessfully sent, the patient's status should
        # have changed and a record of the email should have been saved
        assert patient.status == Patient.Status.ENGAGED
        assert PatientDocument.objects.filter(patient=patient).count() == 1
        # TODO: test the content of the email and patient document

    def test_send_when_email_fails(self):
        patient = PatientFactory(
            status=Patient.Status.NEW,
            cancelled=Patient.Cancelled.NOT_CANCELLED
        )
        patient_enrolment_email = PatientEnrolmentEmail(patient)
        mock_send_mail = MagicMock()
        mock_send_mail.side_effect = Exception()

        with patch('apps.patient.emails.send_mail', mock_send_mail), \
            self.assertRaises(Exception):
            patient_enrolment_email.send()

        # As the email failed to send, no changes should occur to the patient
        # and no record needs to be kept
        assert patient.status == Patient.Status.NEW
        assert PatientDocument.objects.filter(patient=patient).count() == 0

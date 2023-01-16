from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db import transaction
from django.core.files.base import ContentFile


class PatientEnrolmentEmail:
    def __init__(self, patient):
        self.patient = patient
        super().__init__()

    @transaction.atomic
    def send(self):
        from .models import Patient, PatientDocument

        context = {
            "username": self.patient.user.username,
            "contact_name": self.patient.care_provider.contact,
            "provider_name": self.patient.care_provider.name
        }
        plaintext_message = render_to_string('patient_enrolment_email_plain.html', context)
        html_message = render_to_string('patient_enrolment_email.html', context)
        send_mail(
            subject="uMed - Patient Enrolment",
            message=plaintext_message,
            from_email="noreply@umed.io",
            recipient_list=[self.patient.user.email],
            html_message=html_message
        )

        # Set the patient's status to engaged and record the email they were sent
        self.patient.status = Patient.Status.ENGAGED
        self.patient.save()
        patient_document = PatientDocument(
            patient=self.patient
        )
        patient_document.save()
        patient_document.file.save('Enrolment email', ContentFile(html_message))

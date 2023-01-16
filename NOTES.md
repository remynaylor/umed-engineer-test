# Notes

## Summary

I've opted for a hybrid approach here - in this PR, I've implemented a rough draft version of the bulk email feature that satisfies most of the requirements stated, but has some limitations. I'll discuss the requirements one by one and explain how this PR could be improved where appropriate, and at the end of these notes I'll then suggest a possible better implementation. Hopefully this will give you some idea of my approach to concretely tackling this sort of task, as well as how I think at a broader level!

### How to send bulk emails

- With the server running, open the admin and go to the Patients page
- Select any patients you wish to email
- Choose the 'Send enrolment emails' in the actions dropdown

An email will be 'sent' to each patient (the email will be printed to the console as there's no SMTP server), and each patient's status will change to Engaged. A 'patient document' will also be saved, keeping a record of the email sent alongside the patient ID and timestamp.

You can also run some tests with `python manage.py test`.

## Implementation components

The main parts of this implementation are:
- An action in the Django admin to trigger the bulk email send
- `PatientQuerySet`, which is responsible for validating whether the given set of patients can be sent the enrolment emails
- `PatientEnrolmentEmail`, which contains the business logic around sending the email (e.g. setting the patient's status etc.) and actually performs the send, using Django's built-in `send_mail` function.

## Discussion of requirements

The task asks for the following to be considered:

> Only patients that have no cancelled status should ever be sent an email.

Implemented.

> Only patients in the "New" status should ever receive an email.

Implemented.

> When an email is successfully sent to a patient their status must be changed to "Engaged".

This is tricky as we have no guarantee, once the SMTP server has been told to send the email, that it actually succeeded. Here I've changed the status if the `send_mail` function succeeds but that's not strictly correct.

> The full rendered content of the email should be stored, related to the Patient, along with the datetime it was sent. All system datetimes should be TZ aware, in UTC. 

Implemented - a new `PatientDocument` model stores these records. For the same reason as above though, we don't know exactly whether the patient actually received the email.

The timestamp requirement is a little confusing but I've interpreted it as meaning server timestamps of the form '...+00:00'.

> Audit trails are important so add appropriate logging but do not leak identifiable data into the logs.

I've added some rudimentary logging to the status of the Patient using the django-simple-history library, but this could definitely be improved. To make sure PII data doesn't reach the logs a combination of filters and formatters could be added to the log handler. I'd also need to know more about what data counts as identifiable here.

> The email must be sent as html, and plain text for those email clients that don't accept html.

Implemented. Annoyingly, the builtin Django bulk email functionality doesn't allow for this, so I've gone with sending emails one by one for now. This is likely to be a performance bottleneck since establishing SMTP connections is expensive.

> Use libs and apps appropriately, apply good naming.

Done.

> SMTP settings will be required. Think about how you will manage those values.

I haven't dealt with this since I've used the console backend for emails. In production, any sensitive config values should be stored using an external secrets provider (e.g. AWS Secrets Manager) and they can be then injected into the container as environment variables at runtime.

> Use the "from" email "noreply@umed.io"

Done. (If this email was to be reused elsewhere I'd move it to a centrally defined constants file, or it could be provided as an env variable if it's likely to change per environment.)

> The email needs to be signed off using the string in CareProvider.contact

Implemented - though originally there was no link between a Patient and a CareProvider, so this is impossible! I've added in this as a foreign key from Patient to CareProvider, but this could be an incorrect assumption.

> The email needs to be addressed to the user using their username. The email will contain the name of the study.

The email is addressed to the user as stated, but there's no indication of where the name of the study should go so I've left that out.

### Other questions about the requirements

- How should the bulk emails be triggered? Who should be allowed to do so? I went with a Django admin action that anyone can trigger for now.
- The email field on a User can be blank - what should we do in this case?
- What should be done if sending an email to one or more patients fails? Do we need alerting in this case?
- What should the email subject be? I've put a placeholder in for now.

## Proposed improved implementation

The biggest problem for scaling here is that the emails are being sent in series by the main web worker, which means that the other parts of the app could be badly affected by a heavy load. By separating out the `PatientEnrolmentEmail` class though, it's straighforward to swap out the `send_mail` call for something that can run asynchronously by another process instead - two options come to mind:

- Run Celery alongside the webserver, and make sending the emails a Celery task (using a suitable queue and backend). Then we can scale the number of workers independently of the number of webserver processes.
- Or, we could put a message on an SQS queue that can an entirely separate system could read from (e.g. a Lambda which makes a call to SES). Then we could add an endpoint to the Django app that allows the Lambda to set the patient's status correctly once the email has been sent. Scaling this only requires increasing the provisioned concurrency of the Lambda.

Both of these options will also improve error handling and retries (either through marking the task as retryable in Celery, or by adding a DLQ for SQS).
# Boilerplate Django Test Code

This repo contains a basic, minimal Django application that can be used as a starting point for the software engineering
technical assessment.

It requires:

* python 3.9
* poetry

To get started clone the respository then run:

```bash
poetry install
poetry shell
python manage.py loaddata care_providers.yaml users.yaml studies.yaml patients.yaml
pytest  # runs tests
```

* It uses sqlite for convenience, but feel free to change it to another relational database if you'd rather use that.
* By default tests will be collected in apps/*/tests directories.
* There is a superuser in the fixtures with username: superadmin, and password: Password8080
* `libs/factories.py` contains factory boy factory classes the models in the apps.
* Fixtures are provided purely to give you an example of what the data in system looks like.

# The Test

Use Django's email functionality to send emails to users in a study. Users are filtered by care provider.


## Requirements

* Only patients that have no cancelled status should ever be sent an email.
* Only patients in the "New" status should ever receive an email.
* When an email is successfully sent to a patient their status must be changed to "Engaged".
* The full rendered content of the email should be stored, related to the the `Patient`, along with the datetime 
  it was sent. All system datetimes should be TZ aware, in UTC. You will need to create models for this.
* Audit trails are important so add appropriate logging but do not leak identifiable data into the logs.
* The email must be sent as html, and plain text for those email clients that don't accept html.
* Use the django admin to avoid building a specific UI for any new models you require.
* Use libs and apps appropriately, apply good naming.
* Your code/functionality should be fully tested.
* You will need to add dummy SMTP settings to the app, and think about how you will manage those values.
* Use the "from" email "noreply@umed.io"
* The email needs to be signed off using the string in `CareProvider.contact`. The email needs to be addresses to the 
  user using their username. The email will contain the name of the study. Example:

```
Dear <patient.username>,

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

Click here <link to https://umed.io> (or plain text for non html emails)

<care_provider.contact>
<care_provider.name>
```

A User story for this feature would read like this:

```
As a member of the uMed operations team
I need to be able to configure an email to be sent to patients on a study.
Also, the full content of any emails sent must be attached to the patient so we know who has received a communication and when.
```

## Things to think about

* How might this scale to many thousands or millions of emails
* Are there any gaps in the requirements that you'd need further information for?
* What exceptions could occur and how might they be handled
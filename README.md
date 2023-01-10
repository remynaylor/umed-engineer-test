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

* It uses sqlite for convenience
* By default tests will be collected in apps/*/tests directories.
* There is a superuser in the fixtures with username: superadmin, and password: Password8080
* `libs/factories.py` contains factory boy factory classes the models in the apps.
* Fixtures are provided purely to give you an example of what the data in system looks like.



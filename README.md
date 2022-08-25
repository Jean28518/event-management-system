# event-management-system
Open Source Event Management System written in django

## Installation
First you have to install the requirements stored in the requirements.txt
```bash
pip install -r requirements.txt
```

### debain based
```bash
sudo apt install libpq-dev python3-tk
```

### arch based
```bash
sudo pacman -S tk
```

## Setup
This command will create the database with the given models.
```bash
python3 src/event_management_system/manage.py migrate
```
Run this command if you want to create the admin user of the local server.
```bash
python3 src/event_management_system/manage.py createsuperuser
```

### Email configuration
This section is intended for the configuration of the email host.
Please keep this access data confidential.
Keep in mind that other apps can also see these environment variables.

#### Linux
```bash
EMAIL_HOST="<EMAIL_HOST>"
EMAIL_PORT="<EMAIL_PORT>"
EMAIL_HOST_USER="<EMAIL_HOST_USER>"
EMAIL_HOST_PASSWORD="<EMAIL_HOST_PASSWORD>"
```

#### Windows
```bash
set EMAIL_HOST="<EMAIL_HOST>"
set EMAIL_PORT="<EMAIL_PORT>"
set EMAIL_HOST_USER="<EMAIL_HOST_USER>"
set EMAIL_HOST_PASSWORD="<EMAIL_HOST_PASSWORD>"
```

## Development
Run this collection to start a local server instance under linux
```bash
python3 src/event_management_system/manage.py runserver
```

### More Commands
If you make any kind of changes to your database class models
```bash
python3 manage.py makemigrations
```
Creating a new django app
```bash
python3 manage.py startapp <app_name>
```
Change a user password
```bash
python manage.py changepassword <username>
```

### Language
Django comes with the feature to build in multilingualism.
For this we use the standard PO (GetText Portable Object) for multilingualism.
You can find the related files under the following path:

`locale/<language abbreviation>/LC_MESSAGES/django.po`

The first time you start the program or make a change in the files,
you must first run the following command to load the translation.

```bash
django-admin compilemessages --ignore=venv
```
*The `--ignore=venv` excludes the Python virtual environment. If the name of your directory is different from venv,
you should adjust this parameter if necessary.
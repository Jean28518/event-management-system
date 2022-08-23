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

## Development
Run this collection to start a local server instanz under linux
```bash
python3 src/event_management_system/manage.py runserver
```
Click [HERE](http://127.0.0.1:8000/users/) to open a new browser tab.

### Links
- [Users](http://127.0.0.1:8000/users/)
- Events
  - [event](http://127.0.0.1:8000/events/event/)
  - [room](http://127.0.0.1:8000/events/event/)
- [Email](http://127.0.0.1:8000/emails/)


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
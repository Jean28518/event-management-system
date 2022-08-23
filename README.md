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
Run this command if you want to build or change the database structure.
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

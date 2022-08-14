# event-management-system
Open Source Event Management System written in django

## Run
Ensure that django is installed. (https://www.djangoproject.com/download/)
```bash
sudo apt install libpq-dev python3-tk
pip3 install psycopg2
cd src/event_management_system/
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

# Event Management System

## Organize. Communicate. Automate.
**Manage your summits, conferences, seminar days or similar with your team and speakers.**
**Keep control of lectures, rooms, events, call for papers and communicate fast with speakers via automated and easy mass mail integration.**

Homepage: https://event-management-system.org/

# Run with docker
```bash
sudo apt install docker docker-compose git # Or similar for your linux distribution
git clone https://github.com/Jean28518/event-management-system.git
cd event-management-system
bash build_flutter.sh
nano .env # Create environment file
```

Insert the following content and change it to your needs:

```bash
DJANGO_SETTINGS_MODULE=event_management_system.settings

# Change these for production use!
SECRET_KEY=k=x2nhy8#(&lt1&$*g%382fpa8kymrl7_$rvk=d=eg_moof=8z

# Comment this line out to deactivate Debug
DEBUG=True

# To deactivate csrf protection uncomment this line:
#DISABLE_CSRF_PROTECTION=True

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=xhdsajshds

# only activate (uncomment) one of these:
#EMAIL_USE_TLS=True
#EMAIL_USE_SSL=True

# To set a custom time zone uncomment this line and adjust it to your timezone:
#TIME_ZONE=Europe/Berlin
```

If you want to activate https://, change http:// to your server domain (e.g. www.example.com) in ``src/caddy/Caddyfile``.
If you don't change this file the event managment system will be reachable under `localhost`.

```bash
sudo docker-compose up -d --build
bash build_flutter.sh
sudo docker-compose up --build # For debugging, if something goes wrong.
```

You are done! You can reach now your event management system at port 80.

## Update running production instance:
Because the sql data is stored in a separate docker volume we can easily rebuild our docker image. A stop of the containers is not needed.
```
git pull
bash build_flutter.sh
sudo docker-compose up -d --build
```

# Run manually (development only)


## Installation
First you have to install the requirements stored in the requirements.txt
```bash
pip install -r requirements.txt
```

### debain based
```bash
sudo apt install libpq-dev python3-tk gettext
```

### arch based
```bash
sudo pacman -S tk gettext
```

## Build flutter parts
```bash
bash build_flutter.sh
```

## Setup
This command will create the database with the given models.
```bash
mkdir src/event_management_system/db
```


### Configuration
This section is intended for the configuration of the email host.
Please keep this access data confidential.
Keep in mind that other apps can also see these environment variables.

paste these e.g. in your .bashrc file or execute these lines in every new terminal session:
```bash
# Change these for production use!
export SECRET_KEY="k=x2nhy8#(&lt1&g*g%382fpa8kymrl7_jrvk=d=eg_moof=8z"
export DEBUG=True

export EMAIL_HOST="smtp.gmail.com"                         
export EMAIL_PORT="587"                                   
export EMAIL_HOST_USER="example@gmail.com"                 
export EMAIL_HOST_PASSWORD="xhdsajshds"   

# only activate (uncomment) one of these:
#export EMAIL_USE_TLS=True
#export EMAIL_USE_SSL=True

# To set a custom time zone uncomment this line and adjust it to your timezone:
#export TIME_ZONE="Europe/Berlin"
```

**After changing the bashrc file you have to restart your terminal!**

```bash
python3 src/event_management_system/manage.py migrate
python3 src/event_management_system/manage.py compilemessages
```

Run this command if you want to create the admin user of the local server.
```
python3 src/event_management_system/manage.py createsuperuser # (This is optional)
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

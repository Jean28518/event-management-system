# event-management-system
Open Source Event Management System written in django

# Run with docker (Production or Development): 
```bash
sudo apt install docker docker-compose git # Or similar for your linux distribution
git clone https://github.com/Jean28518/event-management-system.git
cd event-management-system
nano .env
```

Insert the following content and change it to your needs:

```bash
DJANGO_SETTINGS_MODULE="event_management_system.settings"

# Change these for production use!
SECRET_KEY="k=x2nhy8#(&lt1&$*g%382fpa8kymrl7_$rvk=d=eg_moof=8z"
DEBUG=True

EMAIL_HOST="smtp.gmail.com"                         
EMAIL_PORT="587"                                   
EMAIL_HOST_USER="example@gmail.com"                 
EMAIL_HOST_PASSWORD="xhdsajshds"   
EMAIL_USE_TLS=True

# Initial Data
FIRET_USER_MAIL="user@example.com"
FIRST_USER_PASSWORD="Oomahohj8ootoosiph3i"
```

If you want to activate https://, change http:// to your server domain (e.g. www.example.com) in ``src/caddy/Caddyfile``.

```bash
sudo docker-compose up -d
sudo docker-compose up  # For debugging, if something goes wrong.
```

# Run manually (development only)


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

paste these e.g. in your .bashrc file or execute these lines in every new terminal session:
```bash
# Change these for production use!
export SECRET_KEY="k=x2nhy8#(&lt1&g*g%382fpa8kymrl7_jrvk=d=eg_moof=8z"
export DEBUG=True

export EMAIL_HOST="smtp.gmail.com"                         
export EMAIL_PORT="587"                                   
export EMAIL_HOST_USER="example@gmail.com"                 
export EMAIL_HOST_PASSWORD="xhdsajshds"   
export EMAIL_USE_TLS=True
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
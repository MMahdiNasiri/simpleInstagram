# SimpleInstagram
this project is a small API that act like Instagram

## Installation
first you need to install python and pip.
we use 
- python 3.8.0
- pip 21.3.1

after cloning the project,
now you must create virtual env and install requirements
>pip install requirements.txt

for creating tables on database you should migrate models of project.
for this you must enter to project in terminal and be on the root of project and run these two commands
```bash
python manage.py makemigrations
python manage.py migrate
```
lets create superuser
> Note: email does not matter and password can be everything even simple
```bash
python manage.py createsuperuser
```
project is ready. just run it:
```bash
python manage.py runserver
```

> Note: for running on linux you need to configure firewall and webserver

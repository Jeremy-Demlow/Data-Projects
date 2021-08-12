# Easy Migration - ETL for the Average Joe

## Setting up Django

### Pre-Requirement
1. Dedicated Pyton Environment
2. `pip install django`

### Starting a Project

Once the environment is set up, create the project with the following command

```
django-admin startproject mysite
```

The command will create a new directory called `mysite` with the following files in the directory.

![](./pics/django-setup.png)

Once the project has been created, start up the app with the following command.

```
cd mysite
python manage.py startapp etl
```

This will create another nested directory with the database objects shown below.

![](./pics/django-db.png)

Once the database files are available, start up the webserver to make sure all is well with the base configuration.

```
python manage.py runserver
```

The first page should look something like this...

![](./pics/django-server.png)

Once the app is running, we can begin to start customizing the website. First, add the name of the application into the "installed apps" section of djago settings (`./mysite/mysite/settings.py`)

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'etl',
]
```

Once the installed app has been added, a view inside the `etl` application can be created to display to the user. The easiest way to do this is to simply display html code to the user. Use the code below inside the file `./mysite/etl/views.py`. This code will display a landing page to the user when they hit the website.

```
from django.shortcuts import render

def index(request):
    return render(request, 'landing.html', {})
```

Now create the html template that is referenced in the django render function.

```
cd mysite
mkdir templates
cd templates/
touch landing_page.html
```

The contents of the html are shown below.

```
<h1>Welcome to Easy Migration!</h1>
<h2>Democratizing and Simplying ETL</h2>
```

Now modify the `./mysite/url.py` file to be able to point to the html template we just created for the app we named `etl`. 

```
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('etl.urls')),
]
```

This will point to a file in the directory: `./mysite/etl/url.py`. Create this file and add the following code.

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

Run the server again `python manage.py runserver` and navigate to the link localhost:8000/etl to view the app.

### Bootstrap Connection for Formating

As you might imagine, the HTML rendering doesn't look to nice. To fix that, we can use bootstrap to quickly get a better looking website.

First, create a template folder in the base of the site similar to the template folder in the etl application directory. Also, add a `base.html` file and add the following code.

```
mkdir mysite/templates/
touch mysite/templates/base.html
echo {% block page_content %}{% endblock %} > mysite/templates/base.html
```

Make sure to install bootstrap into the `base.html` file as well. This can be done by copying the source code link [here](https://github.com/realpython/materials/blob/1ea78b8bb71e685c476d6fd98e829b6ad0a42123/rp-portfolio/personal_portfolio/templates/base.html).

Now modify the `landing.html` document to have the following code as well.

```
{% extends "base.html" %}

{% block page_content %}
<h1>Welcome to Easy Migration</h1>
<h2>Democratizing and Simplifying the ETL Process</h2>
{% endblock %}
```

Now we tell django that the `base.html` file exists and where to look for it. In mysite/settings.py, update the TEMPLATES dictionary item called `DIRS` as shown below.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['mysite/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

The rendering sould look a bit better at this point. Now let's move on to making real functionality to the application.

### Adding Functionality - Models

Django uses object oriented programming (oop) in order to display information to the user of the website. The base way this is done is by creating a "model" inside a django application. The first model we will be creating is the csv model where the user can upload a csv file into snowflake directly. Inside the `etl/models.py` section of the code, create the following model for the etl application. This model will have three objects which are also listed below in the doc string.

```
from django.db import models

class functionality(models.Model):
    """Creates three objects which will be used by the website.

    * title: what the functionality is
    * description: short description of the functionality
    * image: catchy picture :)

    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FilePathField(path="/img")
```

Once the model is created, an associated view has to be created as well. Do this in the `etl/views.py` file.

```
def function_index(request):
    functions = Functionality.objects.all()
    context = {
        'functions': functions
    }
    return render(request, 'functionality_index.html', context)
```

Similar to last time, the information associated with the view inside of `etl/url.py` also has to be changed.

```
urlpatterns = [
    path('', views.function_index, name='function_index'),
]
```

Note: functionality_index.html has all the html to map the model to a custom html view. With the new changes, migrate the project by doing the following commands.

```
python manage.py makemigration
python manage.py migrate
```

Lastly, all we have to do is create the funtionality object inside the SQL database with a python ORM command. We will execute this command in the django CLI with the command below as well.

```
from projects.models import Functionality

f1 = Functionality(
    title='Upload CSV',
    description='Take a local csv file and upload this into a snowflake table.',
    image='img/uploadcsv.png'
)
f1.save()
```

```
python manage.py shell < etl/app_functionality.py
```

### Adding Nested/OOP Models

Now that one model is working, lets add the next step to the process which would be to follow the etl link in the model. 

*Learning Links*
* [Setting up a djago project](https://realpython.com/django-setup/#tutorial-requirements)
* [Django w Postgres](https://medium.com/@stackpython/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8)
* [Designing a Website With Django](https://realpython.com/get-started-with-django-1/)
* [Djago Documentation Tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

## Docker Running Django

Step to ensure the container is built properly.

1. Pull the base python 3 image
2. Install libraries with pip (including django)
3. Install easy migration code
4. Expose port 8000 (where django runs by default)
5. On the entrypoint, run the django server
6. At runtime, map ports with `-p 8000:8000`

## Deploying to an Heroku

### Locally deploying

First make sure you have a [heroku account](https://www.heroku.com/) and the heroku CLI installed. Once you have this, login to heroku and heroku container registry from the CLI.

```
heroku login
heroku container:login

OUT:
(sf) Clays-MacBook-Pro:snowflake-etl-gui ClayElmore$ heroku login
 ›   Warning: heroku update available from 7.42.1 to 7.46.0.
heroku: Press any key to open up the browser to login or q to exit: 
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/<token>
Logging in... done
Logged in as celmore25@gmail.com
(sf) Clays-MacBook-Pro:snowflake-etl-gui ClayElmore$ heroku container:login
 ›   Warning: heroku update available from 7.42.1 to 7.46.0.
Login Succeeded
```

Create an app and make sure you copy the app name - it will be weird.

```
(sf) Clays-MacBook-Pro:snowflake-etl-gui ClayElmore$ heroku create
Creating app... done, ⬢ sheltered-oasis-33303
https://sheltered-oasis-33303.herokuapp.com/ | https://git.heroku.com/sheltered-oasis-33303.git
```

To be able to specify run time pieces to heroku you have to use the port which is randomly generated by heroku which is saved as an environment variable called `$PORT`. This is done in the dockerfile with the following command on entry.

```
# start the server on entry point
WORKDIR /snowflake-etl-gui/mysite/
CMD python manage.py runserver 0.0.0.0:$PORT
```

The host url that heroku allocates to your website also needs to be specified in the settings python file for django. This is located at `/mysite/mysite/settings.py`. This change is shown below.

```
ALLOWED_HOSTS = ['sheltered-oasis-33303.herokuapp.com']
```

Now build and push the image to heroku. You should see the below output.

```
heroku container:push web

OUT: 
Successfully built d857188606d7
Successfully tagged registry.heroku.com/sheltered-oasis-33303/web:latest
=== Pushing web (~/snowflake-etl-gui/Dockerfile)
...
Your image has been successfully pushed. You can now release it with the 'container:release' command
```

Once the container has been pushed, the container has to be released to the web. This is done via the heroku CLI.

```
heroku container:release web
```

The app can then be viewed with `heroku open`.

### CICD with GitHub Actions


First, get a heroku api token for the project and store it in github actions settings as `HEROKU_API_KEY`. Create the token with the following command. **Make sure to save the token!**

```
heroku authorizations:create
```

There is an open source action that allows you to deploy docker images to heroku. The documentation can be found [here](https://github.com/marketplace/actions/deploy-to-heroku). The action looks like the following.

```
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: akhileshns/heroku-deploy@v3.5.7 # This is the action
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "sheltered-oasis-33303"
          heroku_email: "celmore25@gmail.com"
          usedocker: true
```

## Celery with django

### Installation

First set up celery in the project main directory with a new file (mysite/mysite/celery.py) and add the following code.

```
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

This code will instantiate a celery "app" for whatever app we determine. In this case it will be "mysite". Next add the input statement into the file `mysite/mysite/__init__.py`

```
from .celery import app as celery_app
__all__ = ('celery_app',)
```

The most important part of all of this is that celery will search the django file strucuture for any installed apps. In this case it is "etl". Celery will search the directory structure for these two default files.

```
mysite/
    etl/
        tasks.py
        models.py
```

Inside the tasks.py files, I will add a very simple task.

```
from celery import shared_task
from time import sleep

@shared_task(bind=True)
def go_to_sleep(self, duration):
    sleep(duration)
    return 'done'
```

In order to store celery results and eventually display them to a website we will use the package called `pip install django-celery-results`. Pip install this library then add the following code into the installed apps section of the settings file.

```
INSTALLED_APPS = (
    ...,
    'django_celery_results',
)
```

Now create the celery database via a migration similar to earlier in the process. 

```
python manage.py migrate django_celery_results
```

Now all the following code the mysite/settings.py file to make sure django is using the correct backends.

```
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
```

### Example with a sleeping function

Create a view inside of etl with the following code.

```
from time import sleep


def progress(request):
    sleep(5)
    return render(request, 'progress.html', {})
```

And an associated html template called progress at `mysite/etl/templates/progress.html` that really just displays anything. Also, inside `etl/urls.py` include the following code.

```
from django.urls import path
from . import views
urlpatterns = [
    ...
    path('progress/', views.progress, name='progress'),
]
```

Also add the associated url into the project url file as well `mysite/mysite/urls.py`. This was done before but just wanted to make sure :) 

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('etl.urls')),
    path('admin/', admin.site.urls),
]
```

If you start the server with `python manage.py runserver` and navigate to localhost:8000/progress, you will notice it took about 5 seconds to load because of the sleep input. Nice! but not nice... Now let's get to celery. 

We need to install redis as the broker with `pip install redis` along with the installations in the previous sections. We also need to start a redis server. We can do that via Heroku by install the "heroku redis" add on into the application. Once that has been added, click on the add on and go to settings and view credentials. Grab the URI string and place this in the settings.py file in the root project like so.

```
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = 'redis://h:pf669622878255a8a9eed94f07bb933d822609c97bf73c47f8a1f1ab93a4d6e11@ec2-184-72-183-246.compute-1.amazonaws.com:29079'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

And migrate again... If you did this before for the celery results install, this won't do anything.

```
python manage.py migrate
```

Now lets create a super user who can see the celetry results. Do this by executing the code below then navigating to localhost:8000/admin.

```
IN:
python manage.py createsuperuser

OUT:
Username (leave blank to use 'clayelmore'): 
Email address: clayelmorenot@gmail.com
Password: 
Password (again): 
Superuser created successfully.
```

You should see the following result with the celery results available in the admin portal.

![celery db](../snowflake-etl-gui/pics/celery_admin.png)

At this point, make sure all the code has been added from the previous celery section! Now we are going to implement the celery function inside the views.py file like so.

```
from .tasks import go_to_sleep

def progress(request):
    go_to_sleep.delay(5)
    return render(request, 'progress.html', {})
```

Once this is done, open up a new terminal and start a celery server with the following code. Make sure to execute this in the `/mysite/` directory. You should see a message confirming connection to the redis server and the two tasks we created.

```
IN:
celery -A mysite worker -l info

OUT:
[tasks]
  . etl.tasks.go_to_sleep
  . mysite.celery.debug_task

[2020-10-15 20:55:31,007: INFO/MainProcess] Connected to redis://h:**@ec2-184-72-183-246.compute-1.amazonaws.com:29079//
```

Now with the celery server running, lets go to the localhost:8000/progress site again. You will notice that it loads pretty much immediately. This is because the celery task is running in the background. Amazing. You can also go back to the admin protal of the website and you can see that the task of going to sleep is now available in the database.

![task](../snowflake-etl-gui/pics/celery_task.png)

Now that we have a task that can run in the background, let's mock a simple etl status generator. First modify the task to look like this.

```
@shared_task(bind=True)
def go_to_sleep(self, duration):
    status_vec = ['uploading file', 'loading file to cloud storage', 'loading data to snowflake']

    status = status_vec[0]
    sleep(duration)
    status = status_vec[1]
    sleep(duration)
    status = status_vec[2]
    sleep(duration)

    return status
```

Also, change the view to include the task id in the rendering view function.

```
def progress(request):
    task = go_to_sleep.delay(2)
    context = {'task': task}
    return render(request, 'progress.html', context)
```

Lastly, change the html template to print out the job status as it moves along.

```
{% extends "base.html" %}
{% load static %}
{% block page_content %}
<h2 style="padding-top: 20px; padding-right: 20px; padding-left: 20px">Process Done</h2>
<p>{% task.task_id %}</p>
{% endblock %}
```

Run the server at the localhost:8000/progress location and we will see this (you probably have to restart the celery server because it caches in tasks as well).

![](../snowflake-etl-gui/pics/celery_id.png)

Now lets figure out how to display a live status.

### CORS

Need this to allow for ajax calls to be recieved on the backend.

```
pip install django-cors-headers
```

In the settings.py - 

```
INSTALLED_APPS = [
    'corsheaders',
]

CORS_ORIGIN_ALLOW_ALL = True
```

### Setting Up a Live Ajax Query

Then I did some other shit and it worked...

### Dockerizing Celery with Django

As long as everything is working above locally, all you should have to do is to start the django and celery servers in parallel.

```
celery -A mysite worker -l info & python manage.py runserver
```

*Learning Links*
* [Creating a celery progress bar](https://www.youtube.com/watch?v=BbPswIqn2VI)

## User Permissioning in Django

I would recommend using the admin portal. To simply create a user.

* Demo User
  * Username - demouser 
  * Password - easymigration123

Add account links to the base urls.

```
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

Now add a login template as shown in the directory.

Add this to settings.

```
LOGIN_REDIRECT_URL = '/'
```

*Learning Links*
* [Comprehensive Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication)

## Postgres Migration from SQLite

First install the dependencies in your environment
```
sudo apt-get build-dep python-psycopg2
pip install psycopg2-binary
```

Store the data in a json object
```
python manage.py dumpdata > db.json
```

Update the `settings.py` file to have the postgres database as the default
```
------- Old -------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

------- New -------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ‘<db_name>’,
        'USER': '<db_username>',
        'PASSWORD': '<password>',
        'HOST': '<db_hostname_or_ip>',
        'PORT': '<db_port>',
    }
}
```

Make the migration
```
python manage.py migrate
```

Delete objects in the shell
```
python manage.py shell 
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
```

Finally load to postgres
```
manage.py loaddata db.json
```

## Setting Up Static and Media with AWS

**[Helpful Link](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)**

### S3 Setup

1. Create an IAM user with programmatic access
2. Create a group with access: AmazonS3FullAccess
3. Create an S3 bucket
   1. Set block permissions to allow public access
   2. Set CORS settings to allow GET requests
```
[
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```
   1. Set bucket policies to allow get request from outside people
```
{
  "Id": "Policy1609891239784",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1609891237664",
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::easy-migration-static/*",
      "Principal": "*"
    }
  ]
}
```

### Django Setup

First install the dependencies.

```
pip install boto3
pip install django-storages
```

Add a file in the base project folder called `storage_backends.py` and add the following code
```
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
```

Update `settings.py`
```
INSTALLED_APPS = [
    ...
    'storages',
]
AWS_ACCESS_KEY_ID = 'AKIAIT2Z5TDYPX3ARJBA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'sibtc-static'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite/static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

Now migrate the static files (this can take a while the first time cause its moving everything at once)
```
python manage.py collectstatic
```

```
/Users/ClayElmore/anaconda3/envs/sf/bin/python manage.py runserver & celery -A mysite worker -l INFO
docker run -it --rm -e PORT=8000 -p 8000:8000 em
/Users/ClayElmore/anaconda3/envs/sf/bin/python manage.py collectstatic
```
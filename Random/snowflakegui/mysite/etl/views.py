from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from etl.models import Functionality
from etl.forms import StorageForm, InputCSVSnowflake, InputCSVAzureSnowflake

from .tasks import *

import json
from django.http import HttpResponse
from celery.result import AsyncResult
from .backend import Progress
import pickle
import numpy as np


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def json_snowflake(request):
    if request.method == 'POST':
        etl_dict = {
            'table_type': request.POST['table_type'],
            'sf_table': request.POST['sf_table'],
            'sf_server': request.POST['sf_server'],
            'sf_user': request.POST['sf_user'],
            'sf_password': request.POST['sf_password'],
            'sf_wh': request.POST['sf_wh'],
            'sf_db': request.POST['sf_db'],
            'sf_schema': request.POST['sf_schema'],
            'sf_role': request.POST['sf_role'],
            'file_name': request.FILES['upsert_file'].name,
            'file': request.FILES['upsert_file'],
        }

        # pickle request file to send to celery
        etl_pickle = 'etl-'+str(np.random.randint(100000000))+'.pickle'
        with open(etl_pickle, 'wb') as p:
            pickle.dump(etl_dict, p)

        # turn on the celery task with the path to the request
        task = json_snowflake_task.delay(etl_pickle)

        # send the context to the html file and render
        context = {
            'storage_info': request.POST,
            'files': request.FILES,
            'task_id': task.task_id,
        }
        return render(request, 'fileupload.html', context)
    else:
        form = InputCSVSnowflake()
    return render(request, 'etl_input_forms/json-snowflake.html', {'form': form})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def parquet_snowflake(request):
    if request.method == 'POST':
        etl_dict = {
            'table_type': request.POST['table_type'],
            'sf_table': request.POST['sf_table'],
            'sf_server': request.POST['sf_server'],
            'sf_user': request.POST['sf_user'],
            'sf_password': request.POST['sf_password'],
            'sf_wh': request.POST['sf_wh'],
            'sf_db': request.POST['sf_db'],
            'sf_schema': request.POST['sf_schema'],
            'sf_role': request.POST['sf_role'],
            'file_name': request.FILES['upsert_file'].name,
            'file': request.FILES['upsert_file'],
        }

        # pickle request file to send to celery
        etl_pickle = 'etl-'+str(np.random.randint(100000000))+'.pickle'
        with open(etl_pickle, 'wb') as p:
            pickle.dump(etl_dict, p)

        # turn on the celery task with the path to the request
        task = parquet_snowflake_task.delay(etl_pickle)

        # send the context to the html file and render
        context = {
            'storage_info': request.POST,
            'files': request.FILES,
            'task_id': task.task_id,
        }
        return render(request, 'fileupload.html', context)
    else:
        form = InputCSVSnowflake()
    return render(request, 'etl_input_forms/parquet-snowflake.html', {'form': form})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def csv_snowflake(request):
    if request.method == 'POST':
        etl_dict = {
            'table_type': request.POST['table_type'],
            'sf_table': request.POST['sf_table'],
            'sf_server': request.POST['sf_server'],
            'sf_user': request.POST['sf_user'],
            'sf_password': request.POST['sf_password'],
            'sf_wh': request.POST['sf_wh'],
            'sf_db': request.POST['sf_db'],
            'sf_schema': request.POST['sf_schema'],
            'sf_role': request.POST['sf_role'],
            'file_name': request.FILES['upsert_file'].name,
            'file': request.FILES['upsert_file'],
        }

        # pickle request file to send to celery
        etl_pickle = 'etl-'+str(np.random.randint(100000000))+'.pickle'
        with open(etl_pickle, 'wb') as p:
            pickle.dump(etl_dict, p)

        # turn on the celery task with the path to the request
        task = csv_snowflake_task.delay(etl_pickle)

        # send the context to the html file and render
        context = {
            'storage_info': request.POST,
            'files': request.FILES,
            'task_id': task.task_id,
        }
        return render(request, 'fileupload.html', context)
    else:
        form = InputCSVSnowflake()
    return render(request, 'etl_input_forms/csv-snowflake.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def csv_azure_snowflake(request):
    if request.method == 'POST':
        etl_dict = {
            'table_type': request.POST['table_type'],
            'blob_account': request.POST['blob_account'],
            'container': request.POST['container'],
            'connection_str': request.POST['connection_str'],
            'sas_token': request.POST['sas_token'],
            'sf_table': request.POST['sf_table'],
            'sf_server': request.POST['sf_server'],
            'sf_user': request.POST['sf_user'],
            'sf_password': request.POST['sf_password'],
            'sf_wh': request.POST['sf_wh'],
            'sf_db': request.POST['sf_db'],
            'sf_schema': request.POST['sf_schema'],
            'sf_role': request.POST['sf_role'],
            'file_name': request.FILES['upsert_file'].name,
            'file': request.FILES['upsert_file'],
        }

        # pickle request file to send to celery
        etl_pickle = 'etl-'+str(np.random.randint(100000000))+'.pickle'
        with open(etl_pickle, 'wb') as p:
            pickle.dump(etl_dict, p)

        # turn on the celery task with the path to the request
        task = csv_azure_snowflake_task.delay(etl_pickle)

        # send the context to the html file and render
        context = {
            'storage_info': request.POST,
            'files': request.FILES,
            'task_id': task.task_id,
        }
        return render(request, 'fileupload.html', context)
    else:
        form = InputCSVAzureSnowflake()
    return render(request, 'etl_input_forms/csv-azure-snowflake.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def csv_azure_snowflake_form(request):
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/etl/upload')
    else:
        form = InputCSVSnowflake()
    return render(request, 'etl_input_forms/csv-snowflake.html', {'form': form})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def get_progress(request, task_id):
    progress = Progress(AsyncResult(task_id))
    return HttpResponse(json.dumps(progress.get_info()), content_type='application/json')


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def progress(request):
    task = go_to_sleep.delay(2)
    context = {'task_id': task.task_id, 'backend': task.backend}
    return render(request, 'progress.html', context)


def function_index(request):
    functions = Functionality.objects.all().exclude(title='CSV File with Azure Blob Staging')
    context = {
        'functions': functions
    }
    return render(request, 'functionality_index.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def storage_index(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StorageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/etl/upload')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StorageForm()

    return render(request, 'storageform.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='betauser').count() == 1, login_url='/accounts/login/')
def upload_index(request):
    """takes a request for an etl task and 1) sends the task to celery and
    2) displays live status

    Args:
        request (request): storage-information request

    Returns:
        render: html rendering
    """
    if request.method == 'POST':

        # store the etl dictionary - the "quarterback"
        etl_dict = {
            'cloud_type': request.POST['cloud_type'],
            'table_type': request.POST['table_type'],
            'blob_account': request.POST['blob_account'],
            'container': request.POST['container'],
            'connection_str': request.POST['connection_str'],
            'sas_token': request.POST['sas_token'],
            'sf_table': request.POST['sf_table'],
            'sf_server': request.POST['sf_server'],
            'sf_user': request.POST['sf_user'],
            'sf_password': request.POST['sf_password'],
            'sf_wh': request.POST['sf_wh'],
            'sf_db': request.POST['sf_db'],
            'sf_schema': request.POST['sf_schema'],
            'sf_role': request.POST['sf_role'],
            'file_name': request.FILES['upsert_file'].name,
            'file': request.FILES['upsert_file'],
        }

        # pickle request file to send to celery
        etl_pickle = 'etl-'+str(np.random.randint(1000000))+'.pickle'

        # pickle the etl request
        with open(etl_pickle, 'wb') as p:
            pickle.dump(etl_dict, p)

        # turn on the celery task with the path to the request
        task = upload_to_snowflake.delay(etl_pickle)

        # send the context to the html file and render
        context = {
            'storage_info': request.POST,
            'files': request.FILES,
            'task_id': task.task_id,
        }
        return render(request, 'fileupload.html', context)
    else:
        return HttpResponseRedirect('/')


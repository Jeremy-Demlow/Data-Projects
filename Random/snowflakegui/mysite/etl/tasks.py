from celery import shared_task
from time import sleep
import pickle
import os

from etl.blob import dj_file_to_blob
from etl.snowflake import append_list_of_files_blob, create_table_from_post, replace_table_from_post, append_table_from_post
from etl.snowflake import Json, Parquet


@shared_task(bind=True)
def go_to_sleep(self, duration):
    status_vec = ['uploading file', 'loading file to cloud storage', 'loading data to snowflake', 'complete']

    self.update_state(state='PROGRESS', meta={'description': status_vec[0]})
    sleep(duration)
    self.update_state(state='PROGRESS', meta={'description': status_vec[1]})
    sleep(duration)
    self.update_state(state='PROGRESS', meta={'description': status_vec[2]})
    sleep(duration)

    return {'description': status_vec[3]}


@shared_task(bind=True)
def upload_to_snowflake(self, etl_pickle):

    # initalize states and first status update
    status_vec = ['Bathcing Files to Cloud Storage', 'Loading Data to Snowflake', 'ETL Job Complete']
    meta = {'description': status_vec[0], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # helper for ajax query
    sleep(1)

    # open the etl request
    with open(etl_pickle, 'rb') as p:
        etl_dict = pickle.load(p)
    os.unlink(etl_pickle)

    # blob storage
    if int(etl_dict['cloud_type']) == 0:

        # send to blob
        file_list = dj_file_to_blob(etl_dict, unlink=True)
        meta = {'description': status_vec[1], 'responce': 'Load in progress'}
        self.update_state(state='PROGRESS', meta=meta)

        # existing table append (using blob)
        if int(etl_dict['table_type']) == 1:
            responce = append_list_of_files_blob(file_list, etl_dict)
        # table creation
        elif int(etl_dict['table_type']) == 0:
            responce = create_table_from_post(etl_dict)
        # table replace
        elif int(etl_dict['table_type']) == 2:
            responce = replace_table_from_post(etl_dict)

    # No storage
    elif int(etl_dict['cloud_type']) == 1:

        # skip to snowflake
        meta = {
            'description': status_vec[1],
            'responce': 'Load in progress',
        }
        self.update_state(state='PROGRESS', meta=meta)

        # existing table append (using blob)
        if int(etl_dict['table_type']) == 1:
            responce = append_table_from_post(etl_dict)
        # table creation
        elif int(etl_dict['table_type']) == 0:
            responce = create_table_from_post(etl_dict)
        # table replace
        elif int(etl_dict['table_type']) == 2:
            responce = replace_table_from_post(etl_dict)

    # alter the pandas responce from snowflake
    if responce is None:
        responce = 'No files were uploaded'
    elif type(responce) == str:
        pass
    else:
        responce = responce[['file', 'status', 'rows_parsed', 'rows_loaded', 'errors_seen']]
        responce = responce.to_html()
        responce = responce.replace('class="dataframe"', 'class="table table-bordered table-striped"')
        responce = responce.replace('<tr style="text-align: right;">', '<tr>')
        responce = responce.replace('border="1"', '')

    # final status update
    meta = {
        'description': status_vec[2],
        'responce': responce,
    }
    self.update_state(state='PROGRESS', meta=meta)
    return meta


@shared_task(bind=True)
def csv_azure_snowflake_task(self, etl_pickle):

    # initalize states and first status update
    status_vec = ['Bathcing Files to Cloud Storage', 'Loading Data to Snowflake', 'ETL Job Complete']
    meta = {'description': status_vec[0], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # helper for ajax query
    sleep(1)

    # open the etl request
    with open(etl_pickle, 'rb') as p:
        etl_dict = pickle.load(p)
    os.unlink(etl_pickle)

    # send to blob
    file_list = dj_file_to_blob(etl_dict, unlink=True)
    meta = {'description': status_vec[1], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # create replace or append
    if int(etl_dict['table_type']) == 1:
        responce = append_list_of_files_blob(file_list, etl_dict)
    elif int(etl_dict['table_type']) == 0:
        responce = create_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 2:
        responce = replace_table_from_post(etl_dict)

    # alter the pandas responce from snowflake
    if responce is None:
        responce = 'No files were uploaded'
    elif type(responce) == str:
        pass
    else:
        responce = responce[['file', 'status', 'rows_parsed', 'rows_loaded', 'errors_seen']]
        responce = responce.to_html()
        responce = responce.replace('class="dataframe"', 'class="table table-bordered table-striped"')
        responce = responce.replace('<tr style="text-align: right;">', '<tr>')
        responce = responce.replace('border="1"', '')

    # final status update
    meta = {
        'description': status_vec[2],
        'responce': responce,
    }
    self.update_state(state='PROGRESS', meta=meta)
    return meta


@shared_task(bind=True)
def csv_snowflake_task(self, etl_pickle):

    # initalize states and first status update
    print('Starting Task')
    status_vec = ['Loading Data to Snowflake', 'ETL Job Complete']
    meta = {'description': status_vec[0], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # helper for ajax query
    sleep(1)

    # open the etl request
    with open(etl_pickle, 'rb') as p:
        etl_dict = pickle.load(p)
    os.unlink(etl_pickle)

    # create replace or append
    print(etl_dict)
    if int(etl_dict['table_type']) == 1:
        responce = append_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 0:
        responce = create_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 2:
        responce = replace_table_from_post(etl_dict)

    # alter the pandas responce from snowflake
    if responce is None:
        responce = 'No files were uploaded'
    elif type(responce) == str:
        pass
    else:
        responce = responce[['file', 'status', 'rows_parsed', 'rows_loaded', 'errors_seen']]
        responce = responce.to_html()
        responce = responce.replace('class="dataframe"', 'class="table table-bordered table-striped"')
        responce = responce.replace('<tr style="text-align: right;">', '<tr>')
        responce = responce.replace('border="1"', '')

    # final status update
    meta = {
        'description': status_vec[1],
        'responce': responce,
    }
    self.update_state(state='PROGRESS', meta=meta)
    return meta


@shared_task(bind=True)
def json_snowflake_task(self, etl_pickle):

    # initalize states and first status update
    print('Starting Task')
    status_vec = ['Loading Data to Snowflake', 'ETL Job Complete']
    meta = {'description': status_vec[0], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # helper for ajax query
    sleep(1)

    # open the etl request
    with open(etl_pickle, 'rb') as p:
        etl_dict = pickle.load(p)
    os.unlink(etl_pickle)

    # create replace or append
    print(etl_dict)
    if int(etl_dict['table_type']) == 1:
        responce = Json.append_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 0:
        responce = Json.create_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 2:
        responce = Json.replace_table_from_post(etl_dict)

    # alter the pandas responce from snowflake
    if responce is None:
        responce = 'No files were uploaded'
    elif type(responce) == str:
        pass
    else:
        responce = responce[['file', 'status', 'rows_parsed', 'rows_loaded', 'errors_seen']]
        responce = responce.to_html()
        responce = responce.replace('class="dataframe"', 'class="table table-bordered table-striped"')
        responce = responce.replace('<tr style="text-align: right;">', '<tr>')
        responce = responce.replace('border="1"', '')

    # final status update
    meta = {
        'description': status_vec[1],
        'responce': responce,
    }
    self.update_state(state='PROGRESS', meta=meta)
    return meta


@shared_task(bind=True)
def parquet_snowflake_task(self, etl_pickle):

    # initalize states and first status update
    print('Starting Task')
    status_vec = ['Loading Data to Snowflake', 'ETL Job Complete']
    meta = {'description': status_vec[0], 'responce': 'Load in progress'}
    self.update_state(state='PROGRESS', meta=meta)

    # helper for ajax query
    sleep(1)

    # open the etl request
    with open(etl_pickle, 'rb') as p:
        etl_dict = pickle.load(p)
    os.unlink(etl_pickle)

    # create replace or append
    print(etl_dict)
    if int(etl_dict['table_type']) == 1:
        responce = Parquet.append_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 0:
        responce = Parquet.create_table_from_post(etl_dict)
    elif int(etl_dict['table_type']) == 2:
        responce = Parquet.replace_table_from_post(etl_dict)

    # alter the pandas responce from snowflake
    if responce is None:
        responce = 'No files were uploaded'
    elif type(responce) == str:
        pass
    else:
        responce = responce[['file', 'status', 'rows_parsed', 'rows_loaded', 'errors_seen']]
        responce = responce.to_html()
        responce = responce.replace('class="dataframe"', 'class="table table-bordered table-striped"')
        responce = responce.replace('<tr style="text-align: right;">', '<tr>')
        responce = responce.replace('border="1"', '')

    # final status update
    meta = {
        'description': status_vec[1],
        'responce': responce,
    }
    self.update_state(state='PROGRESS', meta=meta)
    return meta

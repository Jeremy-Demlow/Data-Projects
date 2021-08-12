from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    path('etl-processes/', views.function_index, name='function_index'),
    path('upload/', views.upload_index, name='upload_index'),
    path('storage-information/', views.storage_index, name='storage_index'),
    path('csv-snowflake/', views.csv_snowflake, name='csv-snowflake'),
    path('csv-azure-snowflake/', views.csv_azure_snowflake, name='csv-azure-snowflake'),
    path('parquet-snowflake/', views.parquet_snowflake, name='parquet-snowflake'),
    path('json-snowflake/', views.json_snowflake, name='json-snowflake'),
    path('progress/', views.progress, name='progress'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status')  # for checking progress of a job
]

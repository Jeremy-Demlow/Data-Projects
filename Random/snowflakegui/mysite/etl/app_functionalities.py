from etl.models import Functionality

f1 = Functionality(
    title='CSV File Direct to Snowflake',
    description='Take a local csv file and upload directly to a snowflake table.',
    form_path='csv-snowflake',
    image='img/uploadcsv.png'
)
f1.save()

f2 = Functionality(
    title='CSV File with Azure Blob Staging',
    description='Take a local csv file and upload this into a snowflake table through Azure Blob Staging.',
    form_path='csv-azure-snowflake',
    image='img/uploadcsvazure.png'
)
f2.save()

f3 = Functionality(
    title='Json File Direct to Snowflake',
    description='Take a local json file and upload directly to a snowflake table.',
    form_path='json-snowflake',
    image='img/uploadjson.png'
)
f3.save()

f4 = Functionality(
    title='Parquet File Direct to Snowflake',
    description='Take a local parquet file and upload directly to a snowflake table.',
    form_path='parquet-snowflake',
    image='img/uploadparquet.png'
)
f4.save()
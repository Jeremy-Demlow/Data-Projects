from easymigration.azure.utils import File_Handling as az

import os
import easymigration.azure.tests as t
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    # create the file
    # path = pkg_resources.resource_filename(easymigration,'azure/tests/hello_blob.sql')\
    file_name = 'hello_blob.sql'
    logger.info('loading file:')
    logger.info(t.__path__[0] + '/' + file_name)

    obj = az()
    obj.push_to_blob(
        file_name='hello_blob.txt',
        file_path=t.__path__[0] + '/' + file_name,
        account_name='snowflakedata',
        container_name='librarytest',
        account_key=os.environ['snowflake_blob_SECRET'],
    )


if __name__ == '__main__':
    main()

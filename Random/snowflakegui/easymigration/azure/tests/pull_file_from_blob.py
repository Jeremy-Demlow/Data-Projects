from easymigration.azure.utils import File_Handling as az

import os


def main():

    file_name = 'i_have_returned.txt'
    file_path = './'
    blob_name = 'hello_blob.txt'

    obj = az()
    obj.pull_from_blob(
        file_name=file_name,
        file_path=file_path,
        account_name='snowflakedata',
        container_name='librarytest',
        account_key=os.environ['snowflake_blob_SECRET'],
        blob_path=blob_name,
    )

    os.unlink(file_path + file_name)


if __name__ == '__main__':
    main()

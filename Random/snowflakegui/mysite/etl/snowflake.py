from easymigration.snowflake.copyinto import CopyInto
from easymigration.snowflake.query import SnowflakeTool
import pandas as pd
from io import StringIO
import io


def append_list_of_files_blob(file_list, etl_dict):
    conn = CopyInto(sfAccount=etl_dict['sf_server'],
                    sfUser=etl_dict['sf_user'],
                    sfPswd=etl_dict['sf_password'],
                    sfWarehouse=etl_dict['sf_wh'],
                    sfDatabase=etl_dict['sf_db'],
                    sfSchema=etl_dict['sf_schema'],
                    sfRole=etl_dict['sf_role'],)
    conn.test_connection()

    for file_name in file_list:
        responce = conn.insert_csv(blob_name=file_name,
                                   blob_path=None,
                                   storage_account=etl_dict['blob_account'],
                                   container_name=etl_dict['container'],
                                   table_name=etl_dict['sf_table'],
                                   sas_token=etl_dict['sas_token'],
                                   fail_on_no_insert=False,
                                   delimiter=',',)
    return responce


def create_table_from_post(etl_dict):

    # first get the file generator
    chunks = etl_dict['file'].chunks()

    # create a snowflake connection
    conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                         sfUser=etl_dict['sf_user'],
                         sfPswd=etl_dict['sf_password'],
                         sfWarehouse=etl_dict['sf_wh'],
                         sfDatabase=etl_dict['sf_db'],
                         sfSchema=etl_dict['sf_schema'],
                         sfRole=etl_dict['sf_role'],)
    conn.test_connection()

    # chunk out the files to dataframes
    for ind, f in enumerate(chunks):
        df = pd.read_csv(StringIO(f.decode()))

        # send the dataframe to snowflake
        if ind == 0:
            create = 'fail'
        else:
            create = 'append'
        print(df)
        responce = conn.infer_to_snowflake(df=df,
                                           table_name=etl_dict['sf_table'].lower(),
                                           if_exists=create
                                           )

    # return responce
    if responce is None:
        name = etl_dict['sf_table']
        responce = f'Table {name} successfully created'

    return responce


def replace_table_from_post(etl_dict):

    # first get the file generator
    chunks = etl_dict['file'].chunks()

    # create a snowflake connection
    conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                         sfUser=etl_dict['sf_user'],
                         sfPswd=etl_dict['sf_password'],
                         sfWarehouse=etl_dict['sf_wh'],
                         sfDatabase=etl_dict['sf_db'],
                         sfSchema=etl_dict['sf_schema'],
                         sfRole=etl_dict['sf_role'],)
    conn.test_connection()

    # chunk out the files to dataframes
    for ind, f in enumerate(chunks):
        df = pd.read_csv(StringIO(f.decode()))

        # send the dataframe to snowflake
        if ind == 0:
            create = 'replace'
        else:
            create = 'append'
        responce = conn.infer_to_snowflake(df=df,
                                           table_name=etl_dict['sf_table'].lower(),
                                           if_exists=create
                                           )

    # return responce
    if responce is None:
        name = etl_dict['sf_table']
        responce = f'Table {name} successfully replaced'

    return responce


def append_table_from_post(etl_dict):

    # first get the file generator
    chunks = etl_dict['file'].chunks()

    # create a snowflake connection
    conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                         sfUser=etl_dict['sf_user'],
                         sfPswd=etl_dict['sf_password'],
                         sfWarehouse=etl_dict['sf_wh'],
                         sfDatabase=etl_dict['sf_db'],
                         sfSchema=etl_dict['sf_schema'],
                         sfRole=etl_dict['sf_role'],)
    conn.test_connection()

    # chunk out the files to dataframes
    for ind, f in enumerate(chunks):
        df = pd.read_csv(StringIO(f.decode()))

        # send the dataframe to snowflake
        create = 'append'
        responce = conn.infer_to_snowflake(df=df,
                                           table_name=etl_dict['sf_table'].lower(),
                                           if_exists=create
                                           )

    # return responce
    if responce is None:
        name = etl_dict['sf_table']
        responce = f'Table {name} successfully appended'

    return responce


class Json:

    @staticmethod
    def append_table_from_post(etl_dict):
        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_json(StringIO(f.decode()))

            # send the dataframe to snowflake
            create = 'append'
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully appended'

        return responce
    
    @staticmethod
    def create_table_from_post(etl_dict):

        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_json(StringIO(f.decode()))

            # send the dataframe to snowflake
            if ind == 0:
                create = 'fail'
            else:
                create = 'append'
            print(df)
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully created'

        return responce

    @staticmethod
    def replace_table_from_post(etl_dict):

        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_json(StringIO(f.decode()))

            # send the dataframe to snowflake
            if ind == 0:
                create = 'replace'
            else:
                create = 'append'
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully replaced'

        return responce


class Parquet:

    @staticmethod
    def append_table_from_post(etl_dict):
        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_parquet(io.BytesIO(f))

            # send the dataframe to snowflake
            create = 'append'
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully appended'

        return responce
    
    @staticmethod
    def create_table_from_post(etl_dict):

        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_parquet(io.BytesIO(f))

            # send the dataframe to snowflake
            if ind == 0:
                create = 'fail'
            else:
                create = 'append'
            print(df)
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully created'

        return responce

    @staticmethod
    def replace_table_from_post(etl_dict):

        # first get the file generator
        chunks = etl_dict['file'].chunks()

        # create a snowflake connection
        conn = SnowflakeTool(sfAccount=etl_dict['sf_server'],
                            sfUser=etl_dict['sf_user'],
                            sfPswd=etl_dict['sf_password'],
                            sfWarehouse=etl_dict['sf_wh'],
                            sfDatabase=etl_dict['sf_db'],
                            sfSchema=etl_dict['sf_schema'],
                            sfRole=etl_dict['sf_role'],)
        conn.test_connection()

        # chunk out the files to dataframes
        for ind, f in enumerate(chunks):
            df = pd.read_parquet(io.BytesIO(f))

            # send the dataframe to snowflake
            if ind == 0:
                create = 'replace'
            else:
                create = 'append'
            responce = conn.infer_to_snowflake(df=df,
                                            table_name=etl_dict['sf_table'].lower(),
                                            if_exists=create
                                            )

        # return responce
        if responce is None:
            name = etl_dict['sf_table']
            responce = f'Table {name} successfully replaced'

        return responce

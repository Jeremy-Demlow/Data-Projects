# from easymigration import azure
from easymigration.azure import filehandling as blob
import pandas as pd
from io import StringIO
import os
import datetime as dt


def dj_file_to_blob(etl_dict, unlink=True):
    """Takes a Django request and pushes the files to blob via chunks

    Args:
        detl_dict (dict): post from previous page paresed to dict

    Returns:
        list: name of file names in blob
    """
    az = blob.FileHandling(etl_dict['connection_str'])
    file_name = etl_dict['file_name']
    chunks = etl_dict['file'].chunks()
    file_list = []
    timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")
    for ind, f in enumerate(chunks):
        chunk_name = file_name.replace('.', '-'+str(ind)+'.')
        df = pd.read_csv(StringIO(f.decode()))
        df.to_csv(chunk_name, index=False)
        dest_name = 'easymigration/' + timestamp + chunk_name
        az.upload(container_name=etl_dict['container'],
                  file_path=chunk_name,
                  dest=dest_name,
                  overwrite=True
                  )
        if unlink:
            os.unlink(chunk_name)
        file_list.append(dest_name)
    return file_list
